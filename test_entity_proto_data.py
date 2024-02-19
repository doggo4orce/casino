import entity_data
import entity_proto_data
import namelist_data
import unittest

class TestEntityProtoData(unittest.TestCase):

  def test_proto(self):
    proto = entity_proto_data.entity_proto_data()
    proto.name="a goblin"
    proto.namelist= namelist_data.namelist_data("goblin")
    proto.ldesc="A goblin stands here, smiling mischievously."
    proto.desc = "<p>It looks like it has something up its sleeve.</p>"

    ent = entity_data.entity_data(proto)
    self.assertEqual(ent.name, "a goblin")
    self.assertIn("goblin", ent.namelist)
    self.assertEqual(ent.Name, "A goblin")
    self.assertEqual(ent.ldesc, "A goblin stands here, smiling mischievously.")
    self.assertEqual(ent.desc, "<p>It looks like it has something up its sleeve.</p>")
    self.assertEqual(ent.room, None)

if __name__ == '__main__':
  unittest.main()