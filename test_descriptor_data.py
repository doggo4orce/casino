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
    d.close()

  def test_write_and_flush(self):
    client, host = socket.socketpair()
    d = descriptor_data.descriptor_data(host, "foreignhost")

    d.write("Welcome!")
    d.flush_output()

    self.assertEqual(client.recv(1024).decode("utf-8"), "Welcome!")

    client.close()
    d.close()

  def test_poll_for_input(self):
    # simulate a connection with client
    client, host = socket.socketpair()
    d = descriptor_data.descriptor_data(host, "foreignhost")

    # client starts sending a command
    client.send(b"get a")

    # but then is interupted by a telnet message IAC WILL TTYPE
    client.send(bytearray([telnet.tel_cmd.IAC, telnet.tel_cmd.WILL, telnet.tel_opt.TTYPE]))

    # client resumes command and terminates it with \r\n
    client.send(b"pple\r\n")

    # client starts sending new command
    client.send(b"drop a")

    # but is interupted again, this time with IAC SB TTYPE IS "tt++" IAC SE
    client.send(bytearray([telnet.tel_cmd.IAC, telnet.tel_cmd.SB, telnet.tel_opt.TTYPE, telnet.ttype_code.IS, ord('t'), ord('t'), ord('+'), ord('+'), telnet.tel_cmd.IAC, telnet.tel_cmd.SE]))    

    # client finishes second command, but doesn't terminate with \r\n
    client.send(b"pple")

    # input is polled (which sends to input stream)
    d.poll_for_input(1)

    # check first input
    self.assertEqual(d.pop_input(), "get apple")

    # check first telnet command
    self.assertEqual(d.pop_telnet(), telnet.tel_msg(telnet.tel_cmd.WILL, telnet.tel_opt.TTYPE))

    # check second telnet command
    self.assertEqual(d.pop_telnet(), telnet.tel_msg(telnet.tel_cmd.SB, telnet.tel_opt.TTYPE, telnet.ttype_code.IS, ord('t'), ord('t'), ord('+'), ord('+'), telnet.tel_cmd.IAC, telnet.tel_cmd.SE))

    # second input should not have gone through yet
    self.assertIsNone(d.pop_input())

    # but now the client follows up with terminating \r\n
    client.send(b"\r\n")
    d.poll_for_input(1)

    # now second command shoul go through
    self.assertEqual(d.pop_input(), "drop apple")

    client.close()
    d.close()

  def test_ttype_negotiation(self):
    client, host = socket.socketpair()
    d = descriptor_data.descriptor_data(host, "12.4.4.19")

    # client sends IAC WILL TTYPE
    client.send(bytearray([telnet.tel_cmd.IAC, telnet.tel_cmd.WILL, telnet.tel_opt.TTYPE]))

    # host receives IAC WILL TTYPE
    d.poll_for_input(1)

    # host processes IAC WILL TTYPE, will automatically send IAC SB TTYPE SEND IAC SE
    d.process_telnet_cmd()

    # make sure it did
    self.assertEqual(client.recv(1024), bytearray([telnet.tel_cmd.IAC, telnet.tel_cmd.SB, telnet.tel_opt.TTYPE, telnet.ttype_code.SEND, telnet.tel_cmd.IAC, telnet.tel_cmd.SE ]))

    # now similate the client responding with IAC SB TTYPE IS "tt++" IAC SE
    client.send(bytearray([telnet.tel_cmd.IAC, telnet.tel_cmd.SB, telnet.tel_opt.TTYPE, telnet.ttype_code.IS, ord('t'), ord('t'), ord('+'), ord('+'), telnet.tel_cmd.IAC, telnet.tel_cmd.SE ]))

    # host receives IAC SB TTYPE IS "tt++" IAC SE
    d.poll_for_input(1)

    # host processes IAC SB TTYPE IS "tt++" IAC SE, will store this information
    d.process_telnet_cmd()

    # make sure it did
    self.assertEqual(d.client.term_type, "tt++")

    client.close()
    d.close()

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
  unittest.main(verbosity=2)