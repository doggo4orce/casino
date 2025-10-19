import descriptor_data
import socket
import unittest

class TestDescriptorData(unittest.TestCase):
  def test_debug(self):
    s = socket.socket()
    d = descriptor_data.descriptor_data(s, "localhost", 1337)
    d.input = "I'm not finis-"
    d.input_q.append("I've typed this command already.")
    d.input_q.append("But it hasn't been processed yet.")
    print(d.debug())
    d.close()

if __name__ == "__main__":
  unittest.main()