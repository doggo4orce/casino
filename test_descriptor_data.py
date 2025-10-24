import descriptor_data
import select
import socket
import telnet
import unittest

class TestDescriptorData(unittest.TestCase):
  def test_debug(self):
    s = socket.socket()
    d = descriptor_data.descriptor_data(s, "localhost")
    print(d.debug())
    d.close()

  def test_send_recv(self):
    client, host = socket.socketpair()
    d = descriptor_data.descriptor_data(host, "client.dyn.dns.org")

    client.send(b"get apple")
    self.assertEqual(d.recv(1024).decode("utf-8"), "get apple")

    host.send(b"drop apple")
    self.assertEqual(client.recv(1024).decode("utf-8"), "drop apple")

    client.close()
    host.close()

  def test_write_and_flush(self):
    mother = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    mother.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    mother.bind(("0.0.0.0", 1234))
    mother.listen(1)
  
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("0.0.0.0", 1234))

    host, addr = mother.accept()

    d_client = descriptor_data.descriptor_data(client, "client.dyn.dns.org")
    d_host = descriptor_data.descriptor_data(host, "host.dyn.dns.org")

    d_client.write("get apple\r\n")
    d_client.flush_output()

    self.assertEqual(d_host.recv(1024).decode("utf-8"), "get apple\r\n")

    mother.close()
    client.close()
    host.close()

  def test_input_stream(self):
    mother = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    mother.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    mother.bind(("0.0.0.0", 1234))
    mother.listen(1)
  
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("0.0.0.0", 1234))

    host, addr = mother.accept()

    d_client = descriptor_data.descriptor_data(client, "client.dyn.dns.org")
    d_host = descriptor_data.descriptor_data(host, "host.dyn.dns.org")

    d_client.write("get a")
    d_client.flush_output()
    d_client.send(telnet.do_ttype)
    d_client.write("pple\r\n")
    d_client.flush_output()

    d_host.poll_for_input(1)

    self.assertEqual(d_host.pop_input(), "get apple")

    self.assertEqual(d_host.pop_telnet(), telnet.tel_msg(telnet.tel_cmd.DO, telnet.tel_opt.TTYPE))
    
    mother.close()
    client.close()
    host.close()

  def test_telnet_parsing(self):
    mother = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    mother.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    mother.bind(("0.0.0.0", 1234))
    mother.listen(1)
  
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("0.0.0.0", 1234))

    host, addr = mother.accept()

    d_client = descriptor_data.descriptor_data(client, "client.dyn.dns.org")
    d_host = descriptor_data.descriptor_data(host, "host.dyn.dns.org")

    d_host.send(telnet.do_naws)
    d_client.poll_for_input(1)

    self.assertEqual(d_client.pop_telnet(), telnet.tel_msg(telnet.tel_cmd.DO, telnet.tel_opt.NAWS))

    d_client.send(bytearray([telnet.tel_cmd.IAC, telnet.tel_cmd.WILL, telnet.tel_opt.NAWS]))
    d_host.poll_for_input(1)

    self.assertEqual(d_host.pop_telnet(), telnet.tel_msg(telnet.tel_cmd.WILL, telnet.tel_opt.NAWS))
    
    mother.close()
    client.close()
    host.close()

  def test_process_telnet_cmd(self):
    mother = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    mother.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    mother.bind(("0.0.0.0", 1234))
    mother.listen(1)
  
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("0.0.0.0", 1234))

    host, addr = mother.accept()

    d_client = descriptor_data.descriptor_data(client, "client.dyn.dns.org")
    d_host = descriptor_data.descriptor_data(host, "host.dyn.dns.org")

    # TTYPE negotiation
    d_client.send(bytearray([telnet.tel_cmd.IAC, telnet.tel_cmd.WILL, telnet.tel_opt.TTYPE]))
    d_host.poll_for_input(1)
    d_host.process_telnet_cmd()
    d_client.poll_for_input(1)

    self.assertEqual(d_client.pop_telnet(), telnet.tel_msg(telnet.tel_cmd.SB, telnet.tel_opt.TTYPE, telnet.ttype_code.SEND, telnet.tel_cmd.IAC, telnet.tel_cmd.SE))

    # TTYPE subnegotiation
    d_client.send(bytearray([telnet.tel_cmd.IAC, telnet.tel_cmd.SB, telnet.tel_opt.TTYPE, telnet.ttype_code.IS, ord('t'), ord('t'), ord('+'), ord('+'), telnet.tel_cmd.IAC, telnet.tel_cmd.SE]))
    d_host.poll_for_input(1)
    d_host.process_telnet_cmd()
    self.assertEqual(d_host.client.term_type, "tt++")

    # NAWS subnegotiation
    d_client.send(bytearray([telnet.tel_cmd.IAC, telnet.tel_cmd.SB, telnet.tel_opt.NAWS, 4, 3, 2, 5, telnet.tel_cmd.IAC, telnet.tel_cmd.SE]))
    d_host.poll_for_input(1)    
    d_host.process_telnet_cmd()
    self.assertEqual(d_host.client.term_width, 256*4 + 3)
    self.assertEqual(d_host.client.term_length, 256*2 + 5)
    
    mother.close()
    client.close()
    host.close()

if __name__ == "__main__":
  unittest.main()