import collections
import config
import enum
import telnet

class input_state(enum.IntEnum):
  NORMAL = 0 # expecting normal input or IAC
  TELNET = 1 # expecting telnet code

class input_stream:
  """Used by descriptors to handle input polled from sockets.
    buffer   =
    telnet   =
    input    =
    state    =
    telnet_q =
    input_q  ="""

  def __init__(self):
    self.buffer   = bytes(0)
    self.telnet   = None
    self.input    = ""
    self.state    = input_state.NORMAL
    self.telnet_q = collections.deque()
    self.input_q  = collections.deque()

  def parse_buffer(self):
    for b in self.buffer:
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

  def next_input(self):
    return self.input_q.popleft()

  def next_telnet(self):
    return self.telnet_q.popleft()