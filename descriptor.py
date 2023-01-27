import collections
import config
import enum
import fcntl
import logging
import nanny
import select
import socket
import structs
import telnet

"""name     = name used to login
   password = password used to log in"""
login_data = collections.namedtuple('login_data', [
  'name',
  'password'
])

class input:
  def __init__(self, data, unread = 0):
    self._data   = data
    self._unread = unread

  # getters
  @property
  def data(self):
    return self._data
  @property
  def unread(self):
    return self._unread

  @property
  def overflow(self):
    return self._unread > 0

class descriptor_state(enum.IntEnum):
  HANDSHAKE           = 0
  CHATTING            = 1
  GET_NAME            = 2
  CONFIRM_NAME        = 3
  GET_NEW_PASS        = 4
  CONFIRM_PASS        = 5
  GET_PASSWORD        = 6
  GET_CONFIRM_REPLACE = 7
  OLC                 = 8

class descriptor:
  # Special Characters, probably belong somewhere else
  LINE_FEED            = 10
  CARRIAGE_RETURN      = 13

  def __init__(self, socket, host):
    """Creates a new descriptor which holds data relevant to the connection
      socket       = self explanatory
      id           = unique id assigned by server (used to look up client)
      in_buf       = input buffer
      out_buf      = output buffer (stored as a string)
      w_i          = index for writing messages for input_q
      input        = buffer for holding incomplete messages before passing to input_q
      input_q      = messages ready to be passed to the command interpreter
      telnet       = storage for partially read telnet command, set to False when not used
      telnet_q     = telnet commands received from client
      state        = what state the user is in
      has_prompt   = set to False if they've sent a command since the last time we showed them their prompt
      client_info  = stores all connection information and telnet negotiation
      login_info   = login information supplied by player before char is assigned
      disconnected = the connection on the other end of the socket has been lost
      char         = character that this connection is controlling
      olc_state    = used in olc.handle_input to parse input and determine menus
      write_buffer = a buffer to store player editing: descriptions, messages, etc
      write_target = where the buffer will be saved to upon completion"""
    self.socket       = socket
    self.id           = id
    self.in_buf       = bytes(0)
    self.out_buf      = ""
    self.w_i          = 0
    self.input        = bytearray(config.MAX_INPUT_LENGTH)
    self.input_q      = collections.deque()
    self.telnet       = False
    self.telnet_q     = collections.deque()
    self.state        = -1
    self.has_prompt   = False
    self.client_info  = structs.client(None, None, None, host)
    self.login_info   = login_data(None, None)
    self.disconnected = False
    self.char         = None
    self.olc          = None
    self.write_buffer = None
    self.write_target = None
    # These two lines ensure that the socket is not automatically closed when oMUD
    # calls itself as a child process (which is what copyover does).
    flags = fcntl.fcntl(self.socket, fcntl.F_GETFD, 0)
    fcntl.fcntl(self.socket, fcntl.F_SETFD, flags & ~fcntl.FD_CLOEXEC)
    # If they are removed, copyover will not recover the existing connections, and
    # is hence pointless.

  """poll_for_input()     <- transfers any pending input into in_buf
     parse_input()        <- organizes input in_buf into a input_q 
     send(bytes)          <- immediately sends raw bytestream to socket
     flush_output()       <- sends any pending output in out_buf
     write_prompt()       <- appends prompt to out_buf
     write(msg)           <- appends msg to out_buf
     process_telnet_cmd() <- organizes telnet commands in in_buf into telnet_q
     process_telnet_q()   <- parses any telnet commands which have been fully read
     next_input()         <- returns next complete command in input_q
     start_writing(source, target) <- start editting source and save to target
     stop_writing(save)   <- save to write_target if save=True"""
    
  @property
  def writing(self):
    return self.write_buffer != None

  def poll_for_input(self):
    rlist, wlist, elist = select.select([ self.socket ], [ ], [ ], 0)
    if self.socket in rlist:
      read = self.socket.recv(config.PACKET_SIZE)
      if len(read) == 0:
        self.disconnected = True
      self.in_buf += read

  def parse_input(self):
    r_i = 0
    finished_input = ""
    parsed_msg = ""
    unread_chars = 0
    # if we're still in the middle of processing a telnet command, pass
    # the buffer to the command (not a typo) to grab what it needs
    if self.telnet:
      # it sends the rest back to us to continue parsing
      self.in_buf = self.telnet.parse_bytestream(self.in_buf[r_i:])
      # if this fails, then that means the entire buffer was consumed
      # by the command, but still didn't complete it, so we should return
      if self.telnet.complete():
        self.telnet_q.append(self.telnet)
        self.telnet = False
      else:
        self.in_buf = bytes(0)
        return
    # by now we've finished the partial command if we had one, or we're
    # starting at the beginning of the buffer and never had a partial
    # command at all
    while r_i < len(self.in_buf):
      # if a command is detected, fire the remaining buffer to a new telnet msg
      if self.in_buf[r_i] == telnet.tel_cmd.IAC:
        self.telnet = telnet.tel_msg()
        self.in_buf = self.telnet.parse_bytestream(self.in_buf[r_i+1:])
        if self.telnet.complete():
          self.telnet_q.append(self.telnet)
          self.telnet = False
        # command sends us back only what wasn't processed, so the index
        # must be reset, continue immediately so it isn't incremented
        r_i = 0
        continue
      # for now we will just completely ignore carriage returns
      elif self.in_buf[r_i] == descriptor.CARRIAGE_RETURN:
        pass
      # a LINE_FEED means we have a new input
      elif self.in_buf[r_i] == descriptor.LINE_FEED:
        parsed_msg =  self.input[:self.w_i].decode("utf-8")
        unread_chars = max(0, self.w_i - config.MAX_INPUT_LENGTH)
        finished_input = input(parsed_msg, unread_chars)
        self.input_q.append(finished_input)
        self.w_i = 0
      # ignore non-printable characters
      elif not str(self.in_buf[r_i]).isprintable():
        pass
      else:
        # if the buffer is full, stop writing, but increment w_i
        # regardless so we know later that too much data was given
        if self.w_i < config.MAX_INPUT_LENGTH:
          self.input[self.w_i] = self.in_buf[r_i]
        self.w_i += 1
      r_i += 1
    self.in_buf = bytes(0)

  def send(self, bytes):
    try:
      self.socket.send(bytes)
    except socket.error:
      logging.warning("Trying to write to disconnected socket: {}.".format(self.addr))
      self.disconnected = True

  def flush_output(self):
    if self.out_buf == "":
      return
    self.send(bytes(self.out_buf, "utf-8"))
    self.out_buf = ""

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
    cmd = self.telnet_q.popleft()
    if cmd.cmd == telnet.tel_cmd.WILL:
      if cmd.opt == telnet.tel_opt.TTYPE:
        self.socket.send(telnet.sb_ttype_send)
    elif cmd.cmd == telnet.tel_cmd.SB:
      if cmd.opt == telnet.tel_opt.TTYPE:
        self.client_info.term_type = cmd.value.decode("utf-8")
      elif cmd.opt == telnet.tel_opt.NAWS:
        self.client_info.term_width = 256 * int(cmd.value[0]) + int(cmd.value[1])
        self.client_info.term_length = 256 * int(cmd.value[2]) + int(cmd.value[3])

  def process_telnet_q(self):
    while self.telnet_q:
      self.process_telnet_cmd()

  def next_input(self):
    if self.input_q:
      return self.input_q.popleft()

  def start_writing(self, source, target):
    self.write_buffer = source.make_copy()
    self.write_target = target

  def stop_writing(self, save):
    if save:
      self.write_target.copy_from(self.write_buffer)
  
    self.write_buffer = None
    self.write_target = None

