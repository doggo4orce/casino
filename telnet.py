import enum
import logging

class tel_cmd(enum.IntEnum):
  SE   = 240 # end subnegotiation
  NOP  = 241
  DM   = 242
  BRK  = 243
  IP   = 244
  AO   = 245
  AYT  = 246
  EC   = 247
  EL   = 248
  GA   = 249 # go ahead
  SB   = 250 # begin subnegotiation
  WILL = 251 # will (negotiation)
  WONT = 252 # won't (negotiation)
  DO   = 253 # do (negotiation)
  DONT = 254 # don't (negotiation)
  IAC  = 255 # interpret as command

class tel_opt(enum.IntEnum):
  TRNSBIN = 0
  ECHO    = 1
  RECONCT = 2
  SUPPGA  = 3
  AMSN    = 4
  STATUS  = 5
  TMARK   = 6
  RCTE    = 7
  OLWIDTH = 8
  OPSIZE  = 9
  NAOCRD  = 10
  NAOHT   = 11
  NAOFD   = 13
  NAVT    = 14
  NAOVTD  = 15
  NAOLD   = 16
  EXASCII = 17
  LOGOUT  = 18
  BYTMCRO = 19
  DATATRM = 20
  SUPDUP  = 21
  SUPDUPO = 22
  SENDLOC = 23
  TTYPE   = 24
  EORCRD  = 25
  TACACS  = 26
  OUTMRK  = 27
  TTYLOC  = 28
  T3270R  = 29
  X3PAD   = 30
  NAWS    = 31
  TRMSPD  = 32
  RFCNTRL = 33
  LINEMD  = 34
  XDSPLC  = 35
  ENVRMT  = 36
  AUTH    = 37
  CRYPT   = 38
  NEWENV  = 39
  TN3270E = 40
  XAUTH   = 41
  CHARSET = 42
  TRSP    = 43
  CPRTCON = 44
  TSUPLEC = 45
  TSTLS   = 46
  SENDURL = 48
  FWDX    = 49
  MSDP    = 69
  MSSP    = 70
  MCCP    = 86
  MSP     = 90
  MXP     = 91
  TOPLOG  = 138
  TSPILOG = 139
  TPRGHB  = 140
  ATCP    = 200
  OPT_GA  = 249
  XOPTLST = 255

class ttype_code(enum.IntEnum):
  IS   = 0
  SEND = 1

class charset_code(enum.IntEnum):
  REQUEST    = 1
  ACCEPT     = 2
  REJECT     = 3
  TTABLE_IS  = 4
  TTABLE_REJ = 5
  TTABLE_ACK = 6
  TTABLE_NAK = 7

# messages sent to clients
do_ttype = bytes([
  tel_cmd.IAC,
  tel_cmd.DO,
  tel_opt.TTYPE
])

do_naws = bytes([
  tel_cmd.IAC,
  tel_cmd.DO,
  tel_opt.NAWS
])

will_echo = bytes([
  tel_cmd.IAC,
  tel_cmd.WILL,
  tel_opt.ECHO
])

wont_echo = bytes([
  tel_cmd.IAC,
  tel_cmd.WONT,
  tel_opt.ECHO
])

sb_ttype_send = bytes([
  tel_cmd.IAC,
  tel_cmd.SB,
  tel_opt.TTYPE,
  ttype_code.SEND,
  tel_cmd.IAC,
  tel_cmd.SE
])

class tel_msg:
  # states for parse_byte, parse_bytestream
  GET_COMMAND   = 0
  GET_OPTION    = 1
  GET_VALUE     = 2
  GET_VALUE_IAC = 3
  GET_COMPLETE  = 4

  def __init__(self, cmd = -1, opt = -1, code = -1, vals = bytes(0)):
    # telnet negotiation takes one of two forms:
    # 1) IAC CMD OPT
    # 2) IAC SB VALUE IAC SE
    self.cmd        = cmd
    self.opt        = opt
    self.code       = code
    self.value      = vals
    self.state      = tel_msg.GET_COMMAND

  def parse_byte(self, b):
    if self.state == tel_msg.GET_COMMAND:
      # we should expect handshake or subnegotiation
      self.cmd = b
      if self.cmd in [ tel_cmd.DO, tel_cmd.DONT, tel_cmd.WILL, tel_cmd.WONT, tel_cmd.SB ]:
        self.state = tel_msg.GET_OPTION
      else:
        self.state = tel_msg.GET_COMPLETE
    # this is the second step, get the option
    elif self.state == tel_msg.GET_OPTION:
      self.opt = b
      # now, we might be complete, but not if negotiating
      if self.cmd != tel_cmd.SB:
        self.state = tel_msg.GET_COMPLETE
      else:
        self.state = tel_msg.GET_VALUE
    elif self.state == tel_msg.GET_VALUE:
      if b == tel_cmd.IAC:
        self.state = tel_msg.GET_VALUE_IAC
      else:
        self.value += bytes([b])
    elif self.state == tel_msg.GET_VALUE_IAC:
      # this is how a value string may contain IAC
      if b == tel_cmd.IAC:
        self.value += bytes([tel_cmd.IAC])
        self.state = tel_msg.GET_VALUE
      elif b == tel_cmd.SE:
        self.state = tel_msg.GET_COMPLETE
      else:
        logging.warning(f"Expecting IAC or SE but received byte {b}.")
    else:
      # if in state GET_COMPLETE or GET_VALUE this shouldn't
      # have been called
      logging.error(f"Found invalid state {self.state}.")

  def parse_bytestream(self, b_str):
    r_i = 0
    iac_i = -1
    while r_i < len(b_str) and self.state != tel_msg.GET_COMPLETE:
      if self.state != tel_msg.GET_VALUE:
        self.parse_byte(b_str[r_i])
        r_i += 1
      else:
        iac_i = b_str[r_i:].find(tel_cmd.IAC)
        if iac_i == -1:
          self.value += b_str[r_i:]
          return bytes(0)
        else:
          self.value += b_str[r_i:r_i + iac_i]
          self.parse_byte(b_str[r_i + iac_i])
          r_i += iac_i + 1
    return b_str[r_i:]

  def complete(self):
    return self.state == tel_msg.GET_COMPLETE

  def ascii_values(self):
    return self.value.isascii()

  def __str__(self):
    if self.opt == -1:
      return 'IAC {}'.format(tel_cmd(self.cmd).name)
    elif self.cmd in [ tel_cmd.DO, tel_cmd.DONT, tel_cmd.WILL, tel_cmd.WONT ]:
      return 'IAC {} {}'.format(tel_cmd(self.cmd).name, tel_opt(self.opt).name)
    elif self.cmd == tel_cmd.SB and self.opt == tel_opt.TTYPE:
      return 'IAC {} {} {} "{}" IAC SE'.format(tel_cmd(self.cmd).name,
        tel_opt(self.opt).name, self.value[0], self.value[1:].decode("utf-8"))
    elif self.cmd == tel_cmd.SB and self.opt == tel_opt.NAWS:
      return 'IAC {} {} {} {} {} {} IAC SE'.format(tel_cmd(self.cmd).name,
        tel_opt(self.opt).name, self.value[0], self.value[1], self.value[2], self.value[3])
    else:
      return 'IAC {} {} {} IAC SE'.format(tel_cmd(self.cmd).name, tel_opt(self.opt).name, self.code, self.value)
