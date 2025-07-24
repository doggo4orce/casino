import cmd_trig_data
import hbeat_proc_data
import obj_proto_data
import unittest

class TestNPCProtoData(unittest.TestCase):

  def test_constructor(self):
    obj_p = obj_proto_data.obj_proto_data()

    obj_p.name = "a new object"
    obj_p.remove_all_aliases()
    obj_p.add_alias("new")
    obj_p.add_alias("object")
    obj_p.ldesc = "a new object sits here"
    obj_p.desc = "it looks new"
    obj_p.id = "new_object"
    obj_p.zone_id = "new_zone"

    self.assertEqual(obj_p.name, "a new object")
    self.assertTrue(obj_p.has_alias("new"))
    self.assertTrue(obj_p.has_alias("object"))
    self.assertEqual(obj_p.ldesc, "a new object sits here")
    self.assertEqual(obj_p.desc, "it looks new")
    self.assertEqual(obj_p.id, "new_object")
    self.assertEqual(obj_p.zone_id, "new_zone")

    def f(x,y):
      return x + y

    def g(x,y,z):
      return x - y
    
    hbeat_proc_data.hbeat_proc_data.expected_args = ["x", "y"]
    cmd_trig_data.cmd_trig_data.expected_args = ["x", "y", "z"]

    proc_f = hbeat_proc_data.hbeat_proc_data("heartbeat_f", f)
    proc_g = cmd_trig_data.prefix_cmd_trig_data("command_g", g)
    
    obj_p.assign_spec_proc(proc_f)
    obj_p.assign_spec_proc(proc_g)

    print(obj_p.debug())

if __name__ == "__main__":
  unittest.main()