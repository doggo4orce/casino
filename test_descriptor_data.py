import descriptor_data
import select
import socket
import unittest

class TestDescriptorData(unittest.TestCase):
  def test_debug(self):
    s = socket.socket()
    d = descriptor_data.descriptor_data(s, "localhost")
    d.input = "I'm not finis-"
    d.input_q.append("I've typed this command already.")
    d.input_q.append("But it hasn't been processed yet.")
    print(d.debug())
    d.close()

  def test_send_recv(self):
    mother = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    mother.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    mother.bind(("0.0.0.0", 1234))
    mother.listen(1)
  
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("0.0.0.0", 1234))

    host, addr = mother.accept()

    d_client = descriptor_data.descriptor_data(client, "client.dyn.dns.org")
    d_host = descriptor_data.descriptor_data(host, "host.dyn.dns.org")

    d_client.send(b"get apple\r\n")
    self.assertEqual(d_host.recv(1024).decode("utf-8"), "get apple\r\n")

    mother.close()
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

  def test_input_q(self):
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
    d_host.poll_for_input(1)
    print(d_host.in_buf)
    print(d_host.input_q)    
    d_host.parse_input_revised()

    print(d_host.in_buf)
    print(d_host.input_q)
    
    mother.close()
    client.close()
    host.close()

if __name__ == "__main__":
  unittest.main()