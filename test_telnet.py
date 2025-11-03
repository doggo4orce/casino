import telnet

import unittest

class TestTelnet(unittest.TestCase):
  def test_parse_byte_and_str(self):
    t = telnet.tel_msg()
    t.parse_byte(int(telnet.tel_cmd.WILL))

    self.assertEqual(t.cmd, telnet.tel_cmd.WILL)
    self.assertEqual(t.state, telnet.telnet_parse_state.GET_OPTION)

    self.assertEqual(str(t), "IAC WILL (incomplete)")

    t.parse_byte(int(telnet.tel_opt.NAWS))

    self.assertEqual(str(t), "IAC WILL NAWS")

    self.assertEqual(t.opt, telnet.tel_opt.NAWS)
    self.assertEqual(t.state, telnet.telnet_parse_state.IS_COMPLETE)
    
    t = telnet.tel_msg()
    t.parse_byte(int(telnet.tel_cmd.SB))

    self.assertEqual(str(t), "IAC SB (incomplete)")
    self.assertEqual(t.cmd, telnet.tel_cmd.SB)
    self.assertEqual(t.state, telnet.telnet_parse_state.GET_OPTION)

    t.parse_byte(int(telnet.tel_opt.NAWS))

    self.assertEqual(str(t), "IAC SB NAWS (incomplete)")

    self.assertEqual(t.opt, telnet.tel_opt.NAWS)
    self.assertEqual(t.state, telnet.telnet_parse_state.GET_PAYLOAD)

    t.parse_byte(0)

    self.assertEqual(str(t), "IAC SB NAWS 0 (incomplete)")
    self.assertEqual(t.payload, bytes([0]))

    t.parse_byte(80)

    self.assertEqual(str(t), "IAC SB NAWS 0 80 (incomplete)")
    self.assertEqual(t.payload, bytes([0, 80]))

    t.parse_byte(0)

    self.assertEqual(str(t), "IAC SB NAWS 0 80 0 (incomplete)")
    self.assertEqual(t.payload, bytes([0, 80, 0]))

    t.parse_byte(30)

    self.assertEqual(str(t), "IAC SB NAWS 80x30 (incomplete)")
    self.assertEqual(t.payload, bytes([0, 80, 0, 30]))

    t.parse_byte(int(telnet.tel_cmd.IAC))

    self.assertEqual(str(t), "IAC SB NAWS 80x30 IAC (incomplete)")
    self.assertEqual(t.state, telnet.telnet_parse_state.GET_PAYLOAD_IAC)

    t.parse_byte(int(telnet.tel_cmd.SE))

    self.assertEqual(t.state, telnet.telnet_parse_state.IS_COMPLETE)

    self.assertEqual(str(t), "IAC SB NAWS 80x30 IAC SE")

    t = telnet.tel_msg()

    t.parse_byte(telnet.tel_cmd.SB)
    self.assertEqual(str(t), "IAC SB (incomplete)")

    t.parse_byte(telnet.tel_opt.TTYPE)
    self.assertEqual(str(t), "IAC SB TTYPE (incomplete)")

    t.parse_byte(telnet.ttype_code.IS)
    self.assertEqual(str(t), "IAC SB TTYPE IS \"\" (incomplete)")

    t.parse_byte(ord('t'))
    self.assertEqual(str(t), "IAC SB TTYPE IS \"t\" (incomplete)")

    t.parse_byte(ord('i'))
    self.assertEqual(str(t), "IAC SB TTYPE IS \"ti\" (incomplete)")

    t.parse_byte(ord('n'))
    self.assertEqual(str(t), "IAC SB TTYPE IS \"tin\" (incomplete)")

    t.parse_byte(ord('t'))
    self.assertEqual(str(t), "IAC SB TTYPE IS \"tint\" (incomplete)")

    t.parse_byte(ord('i'))
    self.assertEqual(str(t), "IAC SB TTYPE IS \"tinti\" (incomplete)")

    t.parse_byte(ord('n'))
    self.assertEqual(str(t), "IAC SB TTYPE IS \"tintin\" (incomplete)")

    t.parse_byte(ord('+'))
    self.assertEqual(str(t), "IAC SB TTYPE IS \"tintin+\" (incomplete)")

    t.parse_byte(ord('+'))
    self.assertEqual(str(t), "IAC SB TTYPE IS \"tintin++\" (incomplete)")

    t.parse_byte(telnet.tel_cmd.IAC)
    self.assertEqual(str(t), "IAC SB TTYPE IS \"tintin++\" IAC (incomplete)")

    t.parse_byte(telnet.tel_cmd.SE)
    self.assertEqual(str(t), "IAC SB TTYPE IS \"tintin++\" IAC SE")

    t = telnet.tel_msg()
    t.parse_byte(telnet.tel_cmd.SB)
    t.parse_byte(242) # DM (which is not defined in telnet.py so will be unrecognized)
    self.assertEqual(str(t), "IAC SB 242 (incomplete)")
    
    t.parse_byte(13)
    self.assertEqual(str(t), "IAC SB 242 13 (incomplete)")

    t.parse_byte(15)
    self.assertEqual(str(t), "IAC SB 242 13 15 (incomplete)")

    t.parse_byte(91)
    self.assertEqual(str(t), "IAC SB 242 13 15 91 (incomplete)")

  def test_parse_bytestream(self):
    t = telnet.tel_msg()
    b_str = [
      telnet.tel_cmd.SB,
      telnet.tel_opt.TTYPE,
      telnet.ttype_code.IS,
      ord('m'), ord('m'), ord('2'), ord('K'),
      telnet.tel_cmd.IAC,
      telnet.tel_cmd.SE
    ]

    t.parse_bytestream(b_str)

    self.assertEqual(str(t), "IAC SB TTYPE IS \"mm2K\" IAC SE")
  
    t = telnet.tel_msg()
    b_str = [
      telnet.tel_cmd.SB,
      telnet.tel_opt.TTYPE,
      telnet.ttype_code.IS,
      ord('X')
    ]

    t.parse_bytestream(b_str)

    self.assertEqual(str(t), "IAC SB TTYPE IS \"X\" (incomplete)")

    t = telnet.tel_msg()

    b_str = [
      242, # DM (which is not defined in telnet.py so will be unrecognized)
    ]

    self.assertEqual(str(t), "(blank)")
    t.parse_bytestream(b_str)
    self.assertEqual(str(t), "IAC 242")

if __name__ == "__main__":
  unittest.main()