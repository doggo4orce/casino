from color import *
import collections
import config
import enum
import telnet

class input_state(enum.IntEnum):
  NORMAL = 0 # expecting normal input or IAC
  TELNET = 1 # expecting telnet code

class input_stream_data:
  """Used by descriptors to handle input polled from sockets.
    buffer   = storage for incoming normal bytes which have yet to be processed
    telnet   = next telnet command currently being built
    input    = next input currently being built
    state    = determines how to interpret next byte
    telnet_q = queue for fully processed telnet messages
    input_q  = queue for fully processed inputs"""
  def __init__(self):
    self.buffer   = bytes(0)
    self.telnet   = None
    self.input    = ""
    self.state    = input_state.NORMAL
    self.telnet_q = collections.deque()
    self.input_q  = collections.deque()

  @property
  def num_inputs(self):
    return len(self.input_q)
  @property
  def num_telnets(self):
    return len(self.telnet_q)

  def parse_bytestream(self, stream):
    for b in stream:
      self.parse_byte(b)

  def parse_byte(self, b):
    if self.state == input_state.NORMAL:
      if b == telnet.tel_cmd.IAC:
        self.state = input_state.TELNET
        self.telnet = telnet.tel_msg()
      elif chr(b) == '\r':
        pass
      elif chr(b) == '\n':
        self.input_q.append(self.input)
        self.input = ""    
      elif chr(b).isprintable():
        self.input += chr(b)
    elif self.state == input_state.TELNET:
      self.telnet.parse_byte(b)
      if self.telnet.complete():
        self.state = input_state.NORMAL
        self.telnet_q.append(self.telnet)
        self.telnet = None

  def pop_input(self):
    if not self.input_q:
      return None
    return self.input_q.popleft()

  def pop_telnet(self):
    return self.telnet_q.popleft()

  def debug(self):
    ret_val = f"Buffer: {CYAN}{self.buffer.decode('utf-8')}{NORMAL}\r\n"
    ret_val += f"Telnet: {CYAN}"
    if self.telnet:
      rete_val += str(self.telnet)
    else:
      ret_val += "None"
    ret_val += NORMAL + "\r\n"
    ret_val += f"Input: {CYAN}{self.input}{NORMAL}\r\n"
    ret_val += f"State: {CYAN}{self.state.name}{NORMAL}\r\n"
    ret_val += f"TELNET_Q: {CYAN}"
    if not self.telnet_q:
      ret_val += "empty"
    else:
      ret_val += "\r\n  " + "\r\n  ".join([str(telnet) for telnet in self.telnet_q])
    ret_val += f"{NORMAL}\r\n"
    ret_val += f"INPUT_Q: {CYAN}"
    if not self.input_q:
      ret_val += "empty"
    else:
      ret_val += "\r\n  " + "\r\n  ".join([input for input in self.input_q])
    ret_val += f"{NORMAL}\r\n"
    return ret_val