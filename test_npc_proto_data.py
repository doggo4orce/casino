import cmd_trig_data
import entity_proto_data
import hbeat_proc_data
import npc_proto_data
import unittest

class TestNPCProtoData(unittest.TestCase):
  def test_npc_proto_data(self):
    npc_p = npc_proto_data.npc_proto_data()

    npc_p.id = 'happy_npc'
    npc_p.zone_id = 'test_zone'

    npc_p.name = "a happy npc"
    npc_p.remove_all_aliases()
    npc_p.add_alias("happy")
    npc_p.add_alias("npc")
    npc_p.ldesc = "a happy npc wanders here"
    npc_p.desc = "it looks happy"

    self.assertEqual(npc_p.name, "a happy npc")
    self.assertTrue(npc_p.has_alias("happy"))
    self.assertTrue(npc_p.has_alias("npc"))
    self.assertEqual(npc_p.ldesc, "a happy npc wanders here")
    self.assertEqual(npc_p.desc, "it looks happy")

    def f(x,y):
      return x + y

    def g(x,y,z):
      return x - y
    
    hbeat_proc_data.hbeat_proc_data.expected_args = ["x", "y"]
    cmd_trig_data.cmd_trig_data.expected_args = ["x", "y", "z"]

    proc_f = hbeat_proc_data.hbeat_proc_data("heartbeat f", f)
    proc_g = cmd_trig_data.prefix_cmd_trig_data("command g", g)
    
    npc_p.assign_spec_proc(proc_f)
    npc_p.assign_spec_proc(proc_g)

    print(npc_p.debug())

if __name__ == "__main__":
  unittest.main()