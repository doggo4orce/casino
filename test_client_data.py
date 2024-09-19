import client_data
import unittest

class TestClient(unittest.TestCase):

  def test_client(self):
    c = client_data.client_data("tintin++", 80, 50, "localhost")

    self.assertEqual(c.term_type, "tintin++")
    self.assertEqual(c.term_width, 80)
    self.assertEqual(c.term_length, 50)
    self.assertEqual(c.term_host, "localhost")

  def test_setters_and_getters(self):
    c = client_data.client_data()

    c.term_type = "mudmaster2000"
    c.term_width = 30
    c.term_length = 50
    c.term_host = "127.0.0.1"

    self.assertEqual(c.term_type, "mudmaster2000")
    self.assertEqual(c.term_width, 30)
    self.assertEqual(c.term_length, 50)
    self.assertEqual(c.term_host, "127.0.0.1")
    
if __name__ == "__main__":
  unittest.main()