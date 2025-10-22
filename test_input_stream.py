import input_stream
import telnet

import unittest

class TestInputStream(unittest.TestCase):
  def test_parse_byte(self):
    stream = input_stream.input_stream()
    stream.parse_byte(ord('g'))
    stream.parse_byte(ord('e'))
    stream.parse_byte(ord('t'))
    stream.parse_byte(telnet.tel_cmd.IAC)
    stream.parse_byte(telnet.tel_cmd.DO)
    stream.parse_byte(telnet.tel_opt.NAWS)
    stream.parse_byte(ord(' '))
    stream.parse_byte(ord('a'))
    stream.parse_byte(ord('p'))
    stream.parse_byte(ord('p'))
    stream.parse_byte(telnet.tel_cmd.IAC)
    stream.parse_byte(telnet.tel_cmd.DO)
    stream.parse_byte(telnet.tel_opt.TTYPE)
    stream.parse_byte(ord('l'))
    stream.parse_byte(ord('e'))
    stream.parse_byte(ord('\r'))
    stream.parse_byte(ord('\n'))
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
<<<<<<< Updated upstream
    stream.parse_byte(ord('t')) # part of telnet command
    stream.parse_byte(ord('i')) # part of telnet command
    stream.parse_byte(ord('n')) # part of telnet command
    stream.parse_byte(ord('t')) # part of telnet command
    stream.parse_byte(ord('i')) # part of telnet command
    stream.parse_byte(ord('n')) # part of telnet command
    stream.parse_byte(ord('+')) # part of telnet command
    stream.parse_byte(ord('+')) # part of telnet command
=======
    stream.parse_byte(ord('t')) # part of telnet sequence
    stream.parse_byte(ord('i')) # part of telnet sequence
    stream.parse_byte(ord('n')) # part of telnet sequence
    stream.parse_byte(ord('t')) # part of telnet sequence
    stream.parse_byte(ord('i')) # part of telnet sequence
    stream.parse_byte(ord('n')) # part of telnet sequence
    stream.parse_byte(ord('+')) # part of telnet sequence
    stream.parse_byte(ord('+')) # part of telnet sequence
>>>>>>> Stashed changes
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
    self.assertEqual(stream.num_inputs, 1)
    self.assertEqual(stream.num_telnets, 5)
    self.assertEqual(stream.pop_input(), "get apple")

    t = stream.pop_telnet()
    t_comparison = telnet.tel_msg()
    
    t_comparison.parse_bytestream([
      telnet.tel_cmd.IAC,
      telnet.tel_cmd.DO,
      telnet.tel_opt.NAWS
      ])

    print(str(t_comparison))
    # self.assertEqual(str(t), str(t_comparison))

    # t = stream.pop_telnet()
    # self.assertEqual(str(t), "IAC DO TTYPE")

    # t = stream.pop_telnet()
    # self.assertEqual(str(t), "IAC WILL TTYPE")

    # t = stream.pop_telnet()
    # self.assertEqual(str(t), "IAC SB TTYPE IS \"tintin++\" IAC SE")

    # t = stream.pop_telnet()
    # self.assertEqual(str(t), "IAC SB TTYPE SEND IAC SE")
    
if __name__ == "__main__":
  unittest.main()