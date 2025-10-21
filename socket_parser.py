import collections
import config

class input_state(enum.IntEnum):
  NORMAL         = 0 # expecting normal input or IAC
  COMMAND        = 1 # expecting command
  SUBNEGOTIATION = 2 # expecting subnegotiation parameters

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
    self.input    = None
    self.state    = input_state.NORMAL
    self.telnet_q = collections.deque()
    self.input_q  = collections.deque()

  def process_buffer(self):
    for b in self.buffer:
      if self.state == input_state.NORMAL:
        if self.telnet != None:
          pass
        elif self.input != None:

        if len(self.buffer) < config.MAX_INPUT_LENGTH:
          # first check if newline, otherwise...
          self.input += b
        elif chr(b) == '\r':
          pass
        elif chr(b) == '\n':
          self.input_q.append(self.input.decode("utf-8"))
          self.input = bytes(0)


    # next_input = ""
    # for b in self.in_buf:
    #   print(int(b))
    #   if self.in_state == input_state.NORMAL:
    #     if self.w_i < config.MAX_INPUT_LENGTH:
    #       if 
    #       self.input[self.w_i] = b
    #     elif chr(b) == '\n':
    #       print("found newline")
    #       self.input_q.append(self.input)
    #       self.input = ""
    #       self.w_i = 0
    #       break
    #     else:
    #       self.overflow = True
    #       pass # overflow discarded
    #   self.w_i += 1