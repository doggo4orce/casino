import cmd_trig_data
import object_data

import unittest

class TestObjectData(unittest.TestCase):
  def test_constructor(self):
    
    cmd_trig_data.cmd_trig_data.expected_args = ["me", "targ", "vict", "other"]
    def trig1(me, targ, vict, other):
      return 3
    ct = cmd_trig_data.prefix_cmd_trig_data("command_trigger", trig1)
    
    obj = object_data.object_data()
    obj.name = "a sharp knife"
    obj.desc = "This knife looks extra sharp -- be careful!"
    obj.ldesc = "A sharp knife has been stuck into the ground here."
    obj.remove_all_aliases()
    obj.add_alias("sharp")
    obj.add_alias("knife")
    
    obj.assign_spec_proc(ct)

    print(obj.debug())

  def test_from_proto(self):
    import obj_proto_data
    opd = obj_proto_data.obj_proto_data()

    obj = object_data.object_data(opd)

    self.assertEqual(obj.name, opd.name)
    self.assertEqual(obj.desc, opd.desc)
    self.assertEqual()
    
    print(obj.debug())
    


if __name__ == '__main__':
  unittest.main()