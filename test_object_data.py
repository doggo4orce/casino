import object_data
import cmd_trig_data
import unittest

class TestObjectData(unittest.TestCase):
  def test_constructor(self):
    obj = object_data.object_data()
    obj.name = "a sharp knife"
    obj.desc = "This knife looks extra sharp -- be careful!"
    obj.ldesc = "A sharp knife has been stuck into the ground here."
    obj.remove_all_alias()
    obj.add_alias("sharp")
    obj.add_alias("knife")
    cmd_trig_data.cmd_trig_data.expected_args = ["me", "targ", "vict", "other"]

    def trig1(me, targ, vict, other):
      return 3

    ct = cmd_trig_data.prefix_cmd_trig_data("command trigger", trig1)
    obj.assign_spec_proc(ct)

    print(obj.debug())

if __name__ == '__main__':
  unittest.main()