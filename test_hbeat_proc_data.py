import hbeat_proc_data
import unittest

class TestHBeatProcData(unittest.TestCase):

  def test_hbeat_proc_data(self):

    hbeat_proc_data.hbeat_proc_data.expected_args = ["hbeat", "proc", "data"]

    def hb_bad(arg1, arg2):
      return arg1 + arg2

    def hb_good(hbeat, proc, data):
      return hbeat + proc + data

    hbeat_bad = hbeat_proc_data.hbeat_proc_data("hbeat trig bad", hb_bad)
    hbeat_good = hbeat_proc_data.hbeat_proc_data("hbeat trig good", hb_good)

    self.assertFalse(hbeat_bad.check("x", "y"))
    self.assertTrue(hbeat_bad.check("arg1", "arg2"))

    self.assertFalse(hbeat_good.check("x", "y"))
    self.assertTrue(hbeat_good.check("hbeat", "proc", "data"))

    self.assertFalse(hbeat_bad.consistent)
    self.assertTrue(hbeat_good.consistent)

    self.assertEqual(hbeat_bad.call(1,2), hb_bad(1,2))
    self.assertEqual(hbeat_good.call(1,2,3), hb_good(1,2,3))

if __name__ == "__main__":
  unittest.main()