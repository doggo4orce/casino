import cmd_trigger_data
import unittest

class TestCmdTrigger(unittest.TestCase):
  def test_cmd_trigger(self):

    # a well-defined spec_proc function, blocks command interpreter afterwards
    def good_func1(mud, me, ch, command, argument, db):
      return cmd_trigger_data.prefix_command_trigger_messages.BLOCK_INTERPRETER

    # an ill-defined spec_proc function (arguments are out of order)
    def bad_func2(me, mud, argument, db, command):
      return cmd_trigger_data.prefix_command_trigger_messages.BLOCK_INTERPRETER

    # a well-defined spec_proc function, runs command interpreter afterwards
    def good_func3(mud, me, ch, command, argument, db):
      return cmd_trigger_data.prefix_command_trigger_messages.RUN_INTERPRETER

    # this should not cause any warning log
    spec1 = cmd_trigger_data.cmd_trigger_data("good trigger", good_func1)

    # this should cause a warning but not an error
    spec2 = cmd_trigger_data.cmd_trigger_data("bad trigger", bad_func2)

    # this should not cause any warning log
    spec3 = cmd_trigger_data.cmd_trigger_data("good trigger", good_func3)

    # catch the fact that arguments are out of order
    self.assertFalse(spec2.consistent)

    # this should not cause any error log
    ret_val1 = spec1.call("mud", "me", "ch", "command", "argument", "db")

    # this should cause an error log but not raise an exception
    ret_val2 = spec2.call("mud", "me")

    # this should not cause any error log
    ret_val3 = spec3.call("mud", "me", "ch", "command", "argument", "db")

    # make sure appropriate messages to command interpreter were sent    
    self.assertEqual(ret_val1, cmd_trigger_data.prefix_command_trigger_messages.BLOCK_INTERPRETER)
    self.assertEqual(ret_val2, None)
    self.assertEqual(ret_val3, cmd_trigger_data.prefix_command_trigger_messages.RUN_INTERPRETER)

if __name__ == "__main__":
  unittest.main()