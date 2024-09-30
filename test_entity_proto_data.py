import entity_data
import entity_proto_data
import namelist_data
import cmd_trig_data
import hbeat_proc_data
import unittest

class TestEntityProtoData(unittest.TestCase):

  def test_proto(self):
    proto = entity_proto_data.entity_proto_data()
    proto.name = "a goblin"
    proto.namelist = namelist_data.namelist_data("goblin")
    proto.ldesc = "A goblin stands here, smiling mischievously."
    proto.desc = "<p>It looks like it has something up its sleeve.</p>"

    ent = entity_data.entity_data(proto)
    self.assertEqual(ent.name, "a goblin")
    self.assertIn("goblin", ent.namelist)
    self.assertEqual(ent.Name, "A goblin")
    self.assertEqual(ent.ldesc, "A goblin stands here, smiling mischievously.")
    self.assertEqual(ent.desc, "<p>It looks like it has something up its sleeve.</p>")
    self.assertEqual(ent.room, None)

  def test_namelist(self):
    proto = entity_proto_data.entity_proto_data()
    proto.name = "a goblin"
    proto.namelist = namelist_data.namelist_data("goblin")
    proto.ldesc = "A goblin stands here, smiling mischievously."
    proto.desc = "<p>It looks like it has something up its sleeve.</p>"

    proto.add_alias("smelly")
    proto.add_alias("tiny")
    proto.add_alias("ugly")

    self.assertEqual(proto.num_aliases, 4)
    proto.remove_alias("tiny")
    self.assertEqual(proto.num_aliases, 3)
    proto.remove_all_aliases()
    self.assertEqual(proto.num_aliases, 0)

  def test_assign_spec_procs(self):
    def f(x,y):
      return x + y

    def g(x,y,z):
      return x - y
    
    hbeat_proc_data.hbeat_proc_data.set_expected_args("x", "y")
    cmd_trig_data.cmd_trig_data.set_expected_args("x", "y", "z")

    proc_f = hbeat_proc_data.hbeat_proc_data("heartbeat f", f)
    proc_g = cmd_trig_data.prefix_cmd_trig_data("command g", g)

    ent_p = entity_proto_data.entity_proto_data()
    
    ent_p.assign_spec_proc(proc_f)
    ent_p.assign_spec_proc(proc_g)

    print(ent_p.debug())

if __name__ == '__main__':
  unittest.main()