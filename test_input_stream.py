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
    print(stream.state.name)
    print(str(stream.next_telnet()))
    
if __name__ == "__main__":
  unittest.main()