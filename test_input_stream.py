import input_stream
import telnet

import unittest

class TestInputStream(unittest.TestCase):
  def test_parse_byte(self):
    stream = input_stream.input_stream()
    self.assertEqual(stream.state, input_stream.input_state.NORMAL)
    stream.parse_byte(ord('g'))
    stream.parse_byte(ord('e'))
    stream.parse_byte(ord('t'))
    self.assertEqual(stream.state, input_stream.input_state.NORMAL)

    stream.parse_byte(telnet.tel_cmd.IAC)
    self.assertEqual(stream.state, input_stream.input_state.TELNET)
    stream.parse_byte(telnet.tel_cmd.DO)
    stream.parse_byte(telnet.tel_opt.NAWS)
    self.assertEqual(stream.state, input_stream.input_state.NORMAL)

    stream.parse_byte(ord(' '))
    stream.parse_byte(ord('a'))
    stream.parse_byte(ord('p'))
    self.assertEqual(stream.state, input_stream.input_state.NORMAL)
    stream.parse_byte(ord('p'))

    stream.parse_byte(telnet.tel_cmd.IAC)
    stream.parse_byte(telnet.tel_cmd.DO)
    self.assertEqual(stream.state, input_stream.input_state.TELNET)
    stream.parse_byte(telnet.tel_opt.TTYPE)

    stream.parse_byte(ord('l'))
    stream.parse_byte(ord('e'))
    stream.parse_byte(ord('\r'))
    stream.parse_byte(ord('\n'))

    self.assertEqual(stream.num_inputs, 1)
    self.assertEqual(stream.pop_input(), "get apple")
    self.assertEqual(stream.num_inputs, 0)
    
    stream.parse_byte(ord('d'))
    stream.parse_byte(ord('r'))
    stream.parse_byte(ord('o'))

    stream.parse_byte(telnet.tel_cmd.IAC)
    stream.parse_byte(telnet.tel_cmd.WILL)
    stream.parse_byte(telnet.tel_opt.TTYPE)

    stream.parse_byte(ord('p'))
    stream.parse_byte(ord(' '))

    stream.parse_byte(telnet.tel_cmd.IAC)
    stream.parse_byte(telnet.tel_cmd.SB)
    stream.parse_byte(telnet.tel_opt.TTYPE)
    stream.parse_byte(telnet.ttype_code.IS)

    stream.parse_byte(ord('t')) # part of telnet message
    stream.parse_byte(ord('i')) # part of telnet message
    stream.parse_byte(ord('n')) # part of telnet message
    stream.parse_byte(ord('t')) # part of telnet message
    stream.parse_byte(ord('i')) # part of telnet message
    stream.parse_byte(ord('n')) # part of telnet message
    stream.parse_byte(ord('+')) # part of telnet message
    stream.parse_byte(ord('+')) # part of telnet message

    stream.parse_byte(telnet.tel_cmd.IAC)
    stream.parse_byte(telnet.tel_cmd.SE)

    stream.parse_byte(ord('a'))
    stream.parse_byte(ord('p'))

    stream.parse_byte(telnet.tel_cmd.IAC)
    stream.parse_byte(telnet.tel_cmd.SB)
    stream.parse_byte(telnet.tel_opt.TTYPE)
    stream.parse_byte(telnet.ttype_code.SEND)
    stream.parse_byte(telnet.tel_cmd.IAC)
    stream.parse_byte(telnet.tel_cmd.SE)

    stream.parse_byte(ord('p'))
    stream.parse_byte(ord('l'))
    stream.parse_byte(ord('e'))

    self.assertEqual(stream.input, "drop apple")

    self.assertEqual(stream.num_telnets, 5)
      
    self.assertEqual(stream.pop_telnet(), telnet.tel_msg(telnet.tel_cmd.DO, telnet.tel_opt.NAWS))
    self.assertEqual(stream.pop_telnet(), telnet.tel_msg(telnet.tel_cmd.DO, telnet.tel_opt.TTYPE))
    self.assertEqual(stream.pop_telnet(), telnet.tel_msg(telnet.tel_cmd.WILL, telnet.tel_opt.TTYPE))

    self.assertEqual(str(stream.pop_telnet()), "IAC SB TTYPE IS \"tintin++\" IAC SE")

    self.assertEqual(stream.pop_telnet(),
      telnet.tel_msg(telnet.tel_cmd.SB, telnet.tel_opt.TTYPE, telnet.ttype_code.SEND,
        telnet.tel_cmd.IAC, telnet.tel_cmd.SE))

    
if __name__ == "__main__":
  unittest.main()