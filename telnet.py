from color import *
import enum
import mudlog

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
  IS_COMPLETE   = 4 # parsing complete

class tel_msg:
  def __init__(self, *bytes):
    """Class designed to handle telnet negotiation messages, which will take
       one of the three forms:
         (1) IAC CMD
         (2) IAC CMD OPT -- if CMD in [DO, DONT, WILL, WONT]
         (3) IAC SB OPT VALUE IAC SE
       cmd   = command (eg, WILL, DONT, or SB)
       opt   = option (eg, TTYPE, NAWS or CHARSET)
       code  = code (eg, IS for TTYPE option or REQUEST for CHARSET option)
       value = value to hold subnegotiation data (eg, client name for TTYPE)
       state = keeps track of how to interpret next byte"""
    self.cmd        = None
    self.opt        = None
    self.value      = bytearray(0)
    self.state      = telnet_parse_state.GET_COMMAND

    # possible initialization
    for b in bytes:
      self.parse_byte(b)

  def parse_byte(self, b):
    if self.state == telnet_parse_state.GET_COMMAND:
      self.cmd = b
      if self.cmd in [ tel_cmd.DO, tel_cmd.DONT, tel_cmd.WILL, tel_cmd.WONT, tel_cmd.SB ]:
        # we are in format (2) or (3)
        self.state = telnet_parse_state.GET_OPTION
      else:
        # we are in format (1)
        self.state = telnet_parse_state.IS_COMPLETE
    elif self.state == telnet_parse_state.GET_OPTION:
      self.opt = b
      if self.cmd != tel_cmd.SB:
        # format (2)
        self.state = telnet_parse_state.IS_COMPLETE
      else:
        # format (3)
        self.state = telnet_parse_state.GET_VALUE
    elif self.state == telnet_parse_state.GET_VALUE:
      if b == tel_cmd.IAC:
        # probable end of subnegotiation
        self.state = telnet_parse_state.GET_VALUE_IAC
      else:
        self.value.append(b)
    elif self.state == telnet_parse_state.GET_VALUE_IAC:
      # value contained escaped IAC, subnegotiation continues
      if b == tel_cmd.IAC:
        self.value.append(b)
        self.state = telnet_parse_state.GET_VALUE
      elif b == tel_cmd.SE:
        self.state = telnet_parse_state.IS_COMPLETE
      else:
        mudlog.warning(f"Expecting IAC or SE but received byte {b}.")
    else:
      # if in state IS_COMPLETE or GET_VALUE this shouldn't
      # have been called
      mudlog.error(f"Found invalid state {self.state.name}.")

  def parse_bytestream(self, stream):
    for b in stream:
      self.parse_byte(b)

  def complete(self):
    return self.state == telnet_parse_state.IS_COMPLETE

  def debug(self):
    ret_val = f"Command: {CYAN}{self.cmd.name if self.cmd else 'None'}{NORMAL}\r\n"
    ret_val += f"Option: {CYAN}{self.opt.name if self.opt else 'None'}{NORMAL}\r\n"
    ret_val += f"Value: {CYAN}{self.value.decode('utf-8')}{NORMAL}\r\n"
    ret_val += f"State: {CYAN}{self.state.name}{NORMAL}"
    return ret_val

  def __str__(self):
    if not self.opt:
      return f"IAC {tel_cmd(self.cmd).name}"
    elif self.cmd != tel_cmd.SB:
      return f"IAC {tel_cmd(self.cmd).name} {tel_opt(self.opt).name}"
    elif self.opt == tel_opt.TTYPE:
      if ttype_code(self.value[0]) == ttype_code.SEND:
        return f"IAC {tel_cmd(self.cmd).name} {tel_opt(self.opt).name} {ttype_code(self.value[0]).name} IAC SE"
      elif ttype_code(self.value[0]) == ttype_code.IS:
        return f"IAC {tel_cmd(self.cmd).name} {tel_opt(self.opt).name} {ttype_code(self.value[0]).name} \"{self.value[1:].decode('utf-8')}\" IAC SE"
    elif self.opt == tel_opt.NAWS:
      return f"IAC {tel_cmd(self.cmd).name} {tel_opt(self.opt).name} {self.value[0]} {self.value[1]} {self.value[2]} {self.value[3]} IAC SE"
    else: # this doesn't look right
      return 'IAC {} {} {} IAC SE'.format(tel_cmd(self.cmd).name, tel_opt(self.opt).name, self.code, self.value)
