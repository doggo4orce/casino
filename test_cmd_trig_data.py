import cmd_trig_data
import unittest

class TestCmdTrigData(unittest.TestCase):

  def test_cmd_trig_data(self):

    cmd_trig_data.cmd_trig_data.expected_args = ["cmd", "trig"]

    def ct_bad(arg1, arg2):
      return arg1 + arg2

    def ct_good(cmd, trig):
      return cmd + trig

    cmd_bad = cmd_trig_data.cmd_trig_data("cmd trig bad", ct_bad)
    cmd_good = cmd_trig_data.cmd_trig_data("cmd trig good", ct_good)

    self.assertFalse(cmd_bad.check("x", "y"))
    self.assertTrue(cmd_bad.check("arg1", "arg2"))

    self.assertFalse(cmd_good.check("x", "y"))
    self.assertTrue(cmd_good.check("cmd", "trig"))

    self.assertFalse(cmd_bad.consistent)
    self.assertTrue(cmd_good.consistent)

    self.assertEqual(cmd_bad.call(1,2), ct_bad(1,2))
    self.assertEqual(cmd_good.call(1,2), ct_good(1,2))

if __name__ == "__main__":
  unittest.main()