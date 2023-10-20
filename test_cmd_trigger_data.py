import cmd_trigger_data
import unittest

class TestCmdTrigger(unittest.TestCase):
  def test_cmd_trigger(self):

    def good_func(mud, me, ch, command, argument, db):
      return cmd_trigger_data.prefix_command_trigger_messages.BLOCK_INTERPRETER

    def bad_func(me, mud, argument, db, command):
      return cmd_trigger_data.prefix_command_trigger_messages.BLOCK_INTERPRETER

    spec1 = cmd_trigger_data.cmd_trigger_data("good trigger", good_func)
    spec2 = cmd_trigger_data.cmd_trigger_data("bad trigger", bad_func)

    assertFalse(spec2.check)

    spec1.call("mud", "me", "ch", "command", "argument", "db")
    spec2.call("mud", "me")


if __name__ == "__main__":
  unittest.main()