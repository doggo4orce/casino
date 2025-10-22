import enum
import logging

class tel_cmd(enum.IntEnum):
  SE   = 240 # end subnegotiation
  NOP  = 241 # null operation
  AYT  = 246 # are you there?
  GA   = 249 # go ahead
  SB   = 250 # begin subnegotiation
  WILL = 251 # will use option
  WONT = 252 # wont use option
  DO   = 253 # do (negotiation)
  DONT = 254 # don't (negotiation)
  IAC  = 255 # interpret as command

class tel_opt(enum.IntEnum):
  ECHO    = 1   # local echo
  SUPPGA  = 3   # suppress go ahead
  TTYPE   = 24  # terminal type
  NAWS    = 31  # negotiate window size
  CHARSET = 42  # character set
  MSSP    = 70  # mud server status protocol
  MCCP    = 86  # mud client compression protocol
  MSP     = 90  # mud sound protocol
  MXP     = 91  # mud extension protocol
  ATCP    = 200 # achaea telnet client protocol

class ttype_code(enum.IntEnum):
  IS   = 0 # client tells us what ttype is
  SEND = 1 # we ask client what ttype is

class charset_code(enum.IntEnum):
  REQUEST    = 1 # ask for list of supported charsets
  ACCEPT     = 2 # accept proposed charset
  REJECT     = 3 # reject proposed charset

# messages sent to clients
do_ttype = bytes([tel_cmd.IAC, tel_cmd.DO, tel_opt.TTYPE])

# tell client to negotiate window size
do_naws = bytes([tel_cmd.IAC, tel_cmd.DO, tel_opt.NAWS])

# tell client to turn off local echo (for passwords)
will_echo = bytes([tel_cmd.IAC, tel_cmd.WILL, tel_opt.ECHO])

# tell client to turn local echo back on
wont_echo = bytes([tel_cmd.IAC, tel_cmd.WONT, tel_opt.ECHO])

# ask client to send terminal type (client name)
sb_ttype_send = bytes([tel_cmd.IAC, tel_cmd.SB, tel_opt.TTYPE,
  ttype_code.SEND, tel_cmd.IAC, tel_cmd.SE])

class telnet_parse_state(enum.IntEnum):
  GET_COMMAND   = 0 # just saw IAC
  GET_OPTION    = 1 # just received command
  GET_VALUE     = 2 # just began SB
  GET_VALUE_IAC = 3 # probable end of SB
  IS_COMPLETE  = 4  # parsing complete

class tel_msg:
  def __init__(self, bytestream=bytes(0)):
    # telnet negotiation takes one of two forms:
    # 1) IAC CMD OPT
    # 2) IAC SB VALUE IAC SE
    self.cmd        = None
    self.opt        = None
    self.code       = None
    self.value      = bytearray(0)
    self.state      = None

    # possible initialization parameter
    self.parse_bytestream(bytestream)

  def parse_byte(self, b):
    if self.state == telnet_parse_state.GET_COMMAND:
      # we should expect handshake or subnegotiation
      self.cmd = b
      if self.cmd in [ tel_cmd.DO, tel_cmd.DONT, tel_cmd.WILL, tel_cmd.WONT, tel_cmd.SB ]:
        self.state = telnet_parse_state.GET_OPTION
      else:
        self.state = telnet_parse_state.IS_COMPLETE
    # this is the second step, get the option
    elif self.state == telnet_parse_state.GET_OPTION:
      self.opt = b
      # now, we might be complete, but not if negotiating
      if self.cmd != tel_cmd.SB:
        self.state = telnet_parse_state.GET_COMPLETE
      else:
        self.state = telnet_parse_state.GET_VALUE
    elif self.state == tel_msg.GET_VALUE:
      if b == tel_cmd.IAC:
        self.state = telnet_parse_state.GET_VALUE_IAC
      else:
        self.value.append(b)
    elif self.state == telnet_parse_state.GET_VALUE_IAC:
      # this is how a value string may contain IAC
      if b == tel_cmd.IAC:
        self.value.append(b)
        self.state = telnet_parse_state.GET_VALUE
      elif b == tel_cmd.SE:
        self.state = telnet_parse_state.GET_COMPLETE
      else:
        logging.warning(f"Expecting IAC or SE but received byte {b}.")
    else:
      # if in state IS_COMPLETE or GET_VALUE this shouldn't
      # have been called
      logging.error(f"Found invalid state {self.state}.")

  def parse_bytestream(self, stream):
    for b in stream:
      self.parse_byte(b)

  def complete(self):
    return self.state == tel_msg.GET_COMPLETE

  def __str__(self):
    if self.opt:
      return f"IAC {tel_cmd(self.cmd).name}"
    elif self.cmd in [ tel_cmd.DO, tel_cmd.DONT, tel_cmd.WILL, tel_cmd.WONT ]:
      return f"IAC {tel_cmd(self.cmd).name} {tel_opt(self.opt).name}"
    elif self.cmd == tel_cmd.SB and self.opt == tel_opt.TTYPE:
      if ttype_code(self.value[0]) == ttype_code.SEND:
        return f"IAC {tel_cmd(self.cmd).name} {tel_opt(self.opt).name} {ttype_code(self.value[0]).name} IAC SE"
      elif ttype_code(self.value[0]) == ttype_code.IS:
        return f"IAC {tel_cmd(self.cmd).name} {tel_opt(self.opt).name} {ttype_code(self.value[0]).name} \"{self.value[1:].decode('utf-8')}\" IAC SE"
    elif self.cmd == tel_cmd.SB and self.opt == tel_opt.NAWS:
      return f"IAC {tel_cmd(self.cmd).name} {tel_opt(self.opt).name} {self.value[0]} {self.value[1]} {self.value[2]} {self.value[3]} IAC SE"
    else: # this doesn't look right
      return 'IAC {} {} {} IAC SE'.format(tel_cmd(self.cmd).name, tel_opt(self.opt).name, self.code, self.value)
