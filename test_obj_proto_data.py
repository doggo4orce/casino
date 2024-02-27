import cmd_trig_data
import entity_proto_data
import hbeat_proc_data
import obj_proto_data
import unittest

class TestNPCProtoData(unittest.TestCase):
  def test_constructor(self):
    ent_p = entity_proto_data.entity_proto_data()
    obj_p = obj_proto_data.obj_proto_data()

    ent_p.name = "an entity proto"
    ent_p.namelist = ["entity", "proto"]
    ent_p.ldesc = "an entity proto exists here"
    ent_p.desc = "<p>It looks like an entity proto.</p>"

    obj_p.entity_proto = ent_p
    self.assertEqual(obj_p.ldesc, "an entity proto exists here")
    obj_p.ldesc = "change it using wrapped setter"
    self.assertEqual(obj_p.ldesc, "change it using wrapped setter")

  def test_assign_spec_procs(self):
    def f(x,y):
      return x + y

    def g(x,y,z):
      return x - y
    
    hbeat_proc_data.hbeat_proc_data.set_expected_args("x", "y")
    cmd_trig_data.cmd_trig_data.set_expected_args("x", "y", "z")

    proc_f = hbeat_proc_data.hbeat_proc_data("heartbeat f", f)
    proc_g = cmd_trig_data.prefix_cmd_trig_data("command g", g)

    obj_p = obj_proto_data.obj_proto_data()
    obj_p.entity_proto = entity_proto_data.entity_proto_data()
    
    obj_p.assign_spec_proc(proc_f)
    obj_p.assign_spec_proc(proc_g)

  def test_id(self):
    obj_p = obj_proto_data.obj_proto_data()
    obj_p.entity_proto = entity_proto_data.entity_proto_data()

    obj_p.id = "bob"
    obj_p.zone_id = "general"

    self.assertEqual(obj_p.id, "bob")
    self.assertEqual(obj_p.zone_id, "general")

    print(str(obj_p))

if __name__ == "__main__":
  unittest.main()