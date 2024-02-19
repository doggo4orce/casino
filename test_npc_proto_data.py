import entity_proto_data
import npc_proto_data
import unittest

class TestNPCProtoData(unittest.TestCase):
  def test_constructor(self):
    ent_p = entity_proto_data.entity_proto_data()
    npc_p = npc_proto_data.npc_proto_data()

    ent_p.name = "an entity proto"
    ent_p.namelist = ["entity", "proto"]
    ent_p.ldesc = "an entity proto exists here"
    ent_p.desc = "<p>It looks like an entity proto.</p>"

    npc_p.entity_proto = ent_p
    self.assertEqual(npc_p.ldesc, "an entity proto exists here")
    npc_p.ldesc = "change it using wrapped setter"
    self.assertEqual(npc_p.ldesc, "change it using wrapped setter")

if __name__ == "__main__":
  unittest.main()