# python modules
import fcntl
import select
import socket
import telnet

# local modules
import buffer_data
from color import *
import client_data
import collections
import config
import dataclasses
import enum
import input_stream_data
import mudlog

@dataclasses.dataclass
class login_data:
  """Keeps track of player's login credentials.  Used to look up character upon login.
     name     = name typed at login
     password = password typed when prompted"""
  name: str = ""
  password: str = ""

class descriptor_state(enum.IntEnum):
  """Different states a descriptor can take, encoded as integers."""
  HANDSHAKE           = 0 # resolving connection
  CHATTING            = 1 # input processed by interpreter
  GET_NAME            = 2 # entering name at login
  CONFIRM_NAME        = 3 # confirming name upon character creation
  GET_NEW_PASS        = 4 # creating password for new character
  CONFIRM_PASS        = 5 # confirming password for new character
  GET_PASSWORD        = 6 # entering password for existing character
  GET_CONFIRM_REPLACE = 7 # asked to kick off previous connection
  OLC                 = 8 # using OLC

class descriptor_data:
  def __init__(self, socket, host):
    """Creates a new descriptor which holds data relevant to the connection
      socket       = socket to communicate with user
      id           = unique id assigned by server
      out_buf      = output buffer (stored as a string)
      state        = descriptor_state of user
      overflow     = used to detect if input exceeds MAX_INPUT_LENGTH
      has_prompt   = set to False if they've sent a command since the last time we showed them their prompt
      client_info  = stores all connection information and telnet negotiation
      login_info   = login information supplied by player before char is assigned
      disconnected = the connection on the other end of the socket has been lost
      char         = character that this connection is controlling
      olc_state    = used in olc.handle_input to parse input and determine menus
      write_buffer = a buffer to store player editing: descriptions, messages, etc
      write_target = keep track of what user is editing, so we know where to save afterwards
      writing      = flag used in nanny to determine if editor should handle input"""
    self._socket       = socket
    self.id           = None
    self.out_buf      = ""
    self.state        = None
    self.overflow     = False # currently unimplemented
    self.has_prompt   = False
    self.client       = client_data.client_data(None, None, None, host)
    self.login_info   = login_data(None, None)
    self.disconnected = False
    self.character    = None
    self.olc          = None
    self.write_buffer = None
    self.write_target = None
    self.input_stream = input_stream_data.input_stream_data()
    self.writing      = False

    """When copyover is called, the mud calls itself as a child process.  If sockets are still
       open when that happens, clients cannot be attached to new sockets, and their connections
       will hang indefinitely.  The following ensures that sockets close automatically during copyovers."""
    try:
      flags = fcntl.fcntl(self._socket, fcntl.F_GETFD, 0)
      fcntl.fcntl(self._socket, fcntl.F_SETFD, flags & ~fcntl.FD_CLOEXEC)
    except Exception as e:
      mudlog.error(e)

  @property
  def type(self):
    return self._socket.type

  """close()                       <- closes socket
     shutdown(how)                 <- shutdown socket
     detach()                      <- detaches socket
     send(bytes)                   <- calls corresponding socket function send
     recv(size)                    <- calls corresponding socket function recv
     poll_for_input(timeout)       <- sends pending input to input_stream
     flush_output()                <- sends any pending output in out_buf
     fileno()                      <- returns file descriptor ID of socket
     write_prompt()                <- appends prompt to out_buf
     write(msg)                    <- appends msg to out_buf
     process_telnet_cmd()          <- process next telnet command
     process_telnet_q()            <- process all telnet commands
     pop_input()                   <- calls input_stream.pop_input()
     pop_telnet()                  <- calls input_stream.pop_telnet()
     start_writing(source)         <- start editing source
     stop_writing(save)            <- save changes if save=True
     debug()                       <- return string of debugging info"""

  def close(self):
    self._socket.close()

  def shutdown(self, how):
    self._socket.shutdown(how)

  def detach(self):
    self._socket.detach()

  def send(self, bytes):
    try:
      self._socket.send(bytes)
    except socket.error:
      mudlog.warning("Trying to write to disconnected socket: {}.".format(self.addr))
      self.disconnected = True

  def recv(self, size):
    try:
      ret_val = self._socket.recv(size)
    except Exception as e:
      mudlog.error(e)
    return ret_val

  def poll_for_input(self, timeout=0):
    rlist, wlist, elist = select.select([ self._socket ], [ ], [ ], timeout)
    if self._socket in rlist:
      read = self.recv(config.PACKET_SIZE)
      # if the socket is in rlist but has no input, then the client closed the connection
      if len(read) == 0:
        self.disconnected = True
      self.input_stream.parse_bytestream(read)

  def flush_output(self):
    if self.out_buf == "":
      return
    self.send(bytes(self.out_buf, "utf-8"))
    self.out_buf = ""

  def fileno(self):
    return self._socket.fileno()

  def write_prompt(self):
    if self.writing:
      if self.out_buf != "":
        self.write("\r\n" + "] ")
      else:
        self.write("] ")
      self.has_prompt = True

    elif self.state == descriptor_state.CHATTING:
      if self.out_buf != "":
        self.write("\r\n" + config.PLAYER_PROMPT)
      else:
        self.write(config.PLAYER_PROMPT)
      self.has_prompt = True

  def write(self, msg):
    if self.has_prompt:
      self.out_buf += "\r\n"
      self.has_prompt = False
    self.out_buf += msg

  def process_telnet_cmd(self):
    message = self.input_stream.pop_telnet()
    if message.cmd == telnet.tel_cmd.WILL:
      if message.opt == telnet.tel_opt.TTYPE:
        self.send(telnet.sb_ttype_send)
    elif message.cmd == telnet.tel_cmd.SB:
      if message.opt == telnet.tel_opt.TTYPE:
        if telnet.ttype_code(message.payload[0]) in telnet.ttype_code and telnet.ttype_code(message.payload[0]) == telnet.ttype_code.IS:
          self.client.term_type = message.payload[1:].decode("utf-8")
      elif message.opt == telnet.tel_opt.NAWS:
        self.client.term_width = 256 * int(message.payload[0]) + int(message.payload[1])
        self.client.term_length = 256 * int(message.payload[2]) + int(message.payload[3])

  def process_telnet_q(self):
    while self.input_stream.num_telnets > 0:
      self.process_telnet_cmd()

  def pop_input(self):
    if self.input_stream.input_q:
      return self.input_stream.pop_input()

  def pop_telnet(self):
    if self.input_stream.telnet_q:
      return self.input_stream.pop_telnet()

  def start_writing(self, source, target):
    self.write_buffer = buffer_data.buffer_data(source)
    self.write_target = target
    self.writing = True

  def stop_writing(self, save):
    self.writing = False

    if save:
      self.write_target.text = self.write_buffer.str(numbers=False)

    # can't delete this because we need to remember it in olc_writing_follow_up
    # and save the write_buffer to the appropriate place.  the alternative is
    # handling that here, but I don't want this class to have to know about all
    # the different OLC states.....
 
    # self.write_buffer = None

  def debug(self):
    ret_val = f"Fileno: {CYAN}{self.fileno()}{NORMAL}\r\n"
    ret_val += f"ID: {CYAN}{self.id}{NORMAL}\r\n"
    ret_val += f"Type: {CYAN}{self.type}{NORMAL}\r\n"
    if self.client == None:
      ret_val += f"Client: {CYAN}None{NORMAL}\r\n"
    else:
      ret_val += self.client.debug()

    ret_val += f"State: {CYAN}{self.state}{NORMAL}\r\n"

    ret_val += f"OutBuf: {CYAN}{self.out_buf}{NORMAL}\r\n"

    if self.input_stream == None:
      ret_val += f"IStream: {CYAN}None{NORMAL}\r\n"
    else:
      ret_val += self.input_stream.debug()

    return ret_val
