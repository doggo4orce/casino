from color import *
import enum
import mudlog

class tel_cmd(enum.IntEnum):
  SE      = 240      # end subnegotiation
  NOP     = 241      # null operation
  AYT     = 246      # are you there?
  GA      = 249      # go ahead
  SB      = 250      # begin subnegotiation
  WILL    = 251      # will use option
  WONT    = 252      # wont use option
  DO      = 253      # do (negotiation)
  DONT    = 254      # don't (negotiation)
  IAC     = 255      # interpret as command

class tel_opt(enum.IntEnum):
  ECHO    = 1        # local echo
  SUPPGA  = 3        # suppress go ahead
  TTYPE   = 24       # terminal type
  NAWS    = 31       # negotiate window size
  CHARSET = 42       # character set
  MSSP    = 70       # mud server status protocol
  MCCP    = 86       # mud client compression protocol
  MSP     = 90       # mud sound protocol
  MXP     = 91       # mud extension protocol
  ATCP    = 200      # achaea telnet client protocol

class ttype_code(enum.IntEnum):
  IS      = 0        # client tells us what ttype is
  SEND    = 1        # we ask client what ttype is

class charset_code(enum.IntEnum):
  REQUEST = 1        # ask for list of supported charsets
  ACCEPT  = 2        # accept proposed charset
  REJECT  = 3        # reject proposed charset

# tell client to negotiate terminal type
do_ttype = bytes([tel_cmd.IAC, tel_cmd.DO, tel_opt.TTYPE])

# tell client to negotiate window size
do_naws = bytes([tel_cmd.IAC, tel_cmd.DO, tel_opt.NAWS])

# tell client to turn off local echo (for passwords)
will_echo = bytes([tel_cmd.IAC, tel_cmd.WILL, tel_opt.ECHO])

# tell client to turn local echo back on
wont_echo = bytes([tel_cmd.IAC, tel_cmd.WONT, tel_opt.ECHO])

# ask client to send terminal type (client name)
sb_ttype_send = bytes([tel_cmd.IAC, tel_cmd.SB, tel_opt.TTYPE, ttype_code.SEND, tel_cmd.IAC, tel_cmd.SE])

class telnet_parse_state(enum.IntEnum):
  GET_COMMAND     = 0 # just saw IAC
  GET_OPTION      = 1 # just received command
  GET_PAYLOAD     = 2 # just began SB
  GET_PAYLOAD_IAC = 3 # probable end of SB
  IS_COMPLETE     = 4 # parsing complete

class tel_msg:
  def __init__(self, *bytes):
    """Class designed to handle telnet negotiation messages, which will take
       one of the three forms:
         (1) IAC cmd                         - most of these will be processed but ignored
         (2) IAC cmd                         - if cmd is a verb
         (3) IAC SB option payload IAC SE    - subnegotiation format
       Note that we don't store the initial or terminating IAC.

       cmd     = command (eg, WILL, DONT, or SB)
       opt     = option (eg, TTYPE, NAWS or CHARSET)
       code    = code (eg, IS for TTYPE option or REQUEST for CHARSET option)
       payload = subnegotiation data (eg, client name for TTYPE)
       state   = keeps track of how to interpret next byte"""
    self.cmd     = None
    self.opt     = None
    self.payload = bytearray(0)
    self.state   = telnet_parse_state.GET_COMMAND

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
        self.state = telnet_parse_state.GET_PAYLOAD
    elif self.state == telnet_parse_state.GET_PAYLOAD:
      if b == tel_cmd.IAC:
        # probable end of subnegotiation
        self.state = telnet_parse_state.GET_PAYLOAD_IAC
      else:
        self.payload.append(b)
    elif self.state == telnet_parse_state.GET_PAYLOAD_IAC:
      # payload contained escaped IAC, subnegotiation continues
      if b == tel_cmd.IAC:
        self.payload.append(b)
        self.state = telnet_parse_state.GET_PAYLOAD
      elif b == tel_cmd.SE:
        self.state = telnet_parse_state.IS_COMPLETE
      else:
        mudlog.warning(f"Expecting IAC or SE but received byte {b}.")
    else:
      # if in state IS_COMPLETE or GET_PAYLOAD this shouldn't
      # have been called
      mudlog.error(f"Found invalid state {self.state.name}.")

  def parse_bytestream(self, stream):
    for b in stream:
      self.parse_byte(b)

  def complete(self):
    return self.state == telnet_parse_state.IS_COMPLETE

  def debug(self):
    ret_val = f"Command: {CYAN}"
    if not self.cmd:
      ret_val += "None"
    elif self.cmd in tel_cmd:
      ret_val += tel_cmd(self.cmd).name
    else:
      ret_val += f"{self.cmd} (unknown)"
    ret_val += f"{NORMAL}\r\n"

    ret_val += f"Option: {CYAN}"
    if not self.opt:
      ret_val += "None"
    elif self.opt in tel_opt:
      ret_val += tel_opt(self.opt).name
    else:
      ret_val += f"{self.opt} (unknown)"
    ret_val += f"{NORMAL}\r\n"

    ret_val += f"Payload: {CYAN}"
    if not self.payload:
      ret_val += "None"
    else:
      ret_val += ", ".join([str(b) for b in self.payload])
    ret_val += f"{NORMAL}\r\n"

    ret_val += f"State: {CYAN}{self.state.name}{NORMAL}"

    return ret_val

  def __str__(self):
    incomplete = "(incomplete)"
    ret_val = "IAC "

    if not self.cmd:
      return "(blank)"

    if self.cmd in tel_cmd:
      ret_val += tel_cmd(self.cmd).name
    else:
      ret_val += f"{self.cmd}"

    if not self.opt and self.complete():
      # IAC CMD format
      return ret_val

    ret_val += " "

    if not self.opt:
      return ret_val + incomplete

    if self.opt in tel_opt:
      ret_val += tel_opt(self.opt).name
    else:
      ret_val += str(self.opt)
    
    if not self.payload and self.complete():
      # IAC CMD OPT format
      return ret_val

    # if we got this far it must be subnegotiation
    ret_val += " "

    # we haven't received payload yet
    if not self.payload:
      return ret_val + incomplete

    if self.opt in tel_opt and tel_opt(self.opt) == tel_opt.TTYPE:
      # TTYPE negotiation: IAC SB TTYPE <code> <data> IAC SE
      if len(self.payload) == 0:
        # haven't received code yet
        return ret_val + incomplete

      if self.payload[0] in ttype_code:
        # code is IS or SEND
        ret_val += ttype_code(self.payload[0]).name
      else:
        # unrecognized code
        ret_val += str(self.payload[0])

      # peel code from payload and interpret the rest as data
      ret_val += f" \"{self.payload[1:].decode("utf-8")}\""

    elif self.opt in tel_opt and tel_opt(self.opt) == tel_opt.NAWS:
      # NAWS negotiation: IAC SB NAWS <width_high> <width_low> <length_high> <length_low> IAC SE
      if len(self.payload) < 4:
        return ret_val + " ".join([str(b) for b in self.payload]) + " " + incomplete

      ret_val += f"{self.payload[0]*256 + self.payload[1]}x{self.payload[2]*256 + self.payload[3]}"
    else:
      # we either don't recognize self.opt or don't have a special way to handle it
      ret_val += " ".join([str(b) for b in self.payload])

    if self.state == telnet_parse_state.GET_PAYLOAD:
      return ret_val + " " + incomplete

    ret_val += " IAC"

    if self.state == telnet_parse_state.GET_PAYLOAD_IAC:
      return ret_val + " " + incomplete

    return ret_val + " SE"
