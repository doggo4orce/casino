import telnet

import unittest

class TestTelnet(unittest.TestCase):
  def test_parse_byte(self):
    t = telnet.tel_msg(telnet.tel_cmd.WILL, telnet.tel_opt.NAWS)
    print(t.debug())

if __name__ == "__main__":
  unittest.main()