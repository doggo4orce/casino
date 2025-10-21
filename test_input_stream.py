import input_stream
import telnet

import unittest

class TestInputStream(unittest.TestCase):
  def test_parse_byte(self):
    stream = input_stream.input_stream()

    buffer = b"get ap" + bytes([telnet.tel_cmd.IAC, telnet.tel_cmd.WILL, telnet.tel_opt.NAWS]) + b"ple\r\n"

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

    print(stream.debug())
    
if __name__ == "__main__":
  unittest.main()