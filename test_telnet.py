import telnet

import unittest

class TestTelnet(unittest.TestCase):
  def test_parse_byte(self):
    t = telnet.tel_msg(telnet.tel_cmd.WILL, telnet.tel_opt.NAWS)
    print(f"{t.debug()}\n")
    
    t = telnet.tel_msg(telnet.tel_cmd.SB, telnet.tel_opt.NAWS, 0, 80, 0, 30,
      telnet.tel_cmd.IAC, telnet.tel_cmd.SE)
    print(f"{t.debug()}\n")
    
    t = telnet.tel_msg(244)
    print(f"{t.debug()}\n")

    t = telnet.tel_msg(telnet.tel_cmd.SB, telnet.tel_opt.TTYPE, telnet.ttype_code.IS,
      ord('t'), ord('t'),ord('+'),ord('+'), telnet.tel_cmd.IAC, telnet.tel_cmd.SE)
    print(f"{t.debug()}\n")

if __name__ == "__main__":
  unittest.main()