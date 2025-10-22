import telnet

import unittest

class TestTelnet(unittest.TestCase):
  def test_parse_byte(self):
    t = telnet.tel_msg()
    t.parse_byte(int(telnet.tel_cmd.WILL))

    self.assertEqual(t.cmd, telnet.tel_cmd.WILL)
    self.assertEqual(t.state, telnet.telnet_parse_state.GET_OPTION)

    t.parse_byte(int(telnet.tel_opt.NAWS))
    self.assertEqual(t.opt, telnet.tel_opt.NAWS)
    self.assertEqual(t.state, telnet.telnet_parse_state.IS_COMPLETE)
    
    t = telnet.tel_msg()
    t.parse_byte(int(telnet.tel_cmd.SB))

    self.assertEqual(t.cmd, telnet.tel_cmd.SB)
    self.assertEqual(t.state, telnet.telnet_parse_state.GET_OPTION)

    t.parse_byte(int(telnet.tel_opt.NAWS))

    self.assertEqual(t.opt, telnet.tel_opt.NAWS)
    self.assertEqual(t.state, telnet.telnet_parse_state.GET_PAYLOAD)

    t.parse_byte(0)

    self.assertEqual(t.payload, bytes([0]))

    t.parse_byte(30)

    self.assertEqual(t.payload, bytes([0, 30]))

    t.parse_byte(0)

    self.assertEqual(t.payload, bytes([0, 30, 0]))

    t.parse_byte(80)

    self.assertEqual(t.payload, bytes([0, 30, 0, 80]))

    t.parse_byte(int(telnet.tel_cmd.IAC))

    self.assertEqual(t.state, telnet.telnet_parse_state.GET_PAYLOAD_IAC)

    t.parse_byte(int(telnet.tel_cmd.SE))

    self.assertEqual(t.state, telnet.telnet_parse_state.IS_COMPLETE)

  def test_parse_bytestream(self):
    t = telnet.tel_msg()
    b_str = [ telnet.tel_cmd.SB, telnet.tel_opt.TTYPE, ord('m'), ord('m'), ord('2'), ord('K'), telnet.tel_cmd.IAC, telnet.tel_cmd.SE]

    t.parse_bytestream(b_str)

    print(t.debug())

if __name__ == "__main__":
  unittest.main()