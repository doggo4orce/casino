import entity_data
import entity_proto_data
import namelist_data
import unittest

class TestEntity(unittest.TestCase):
  def test_entity(self):
    ent = entity_data.entity_data()

    ent.name = "a young dog"
    ent.namelist = namelist_data.namelist_data("dog", "young", "puppy")
    ent.ldesc = "A young dog chases after a ball."
    ent.desc = "<p>It looks like a young puppy.</p>"

    self.assertTrue(ent.namelist.has_alias("young"))
    self.assertTrue(ent.namelist.has_alias("dog"))
    self.assertTrue(ent.namelist.has_alias("puppy"))
    self.assertFalse(ent.namelist.has_alias("cat"))
    self.assertEqual(ent.namelist.num_aliases, 3)

    self.assertEqual(ent.Name, "A young dog")
    self.assertEqual(ent.ldesc, "A young dog chases after a ball.")
    self.assertEqual(ent.desc, "<p>It looks like a young puppy.</p>")
    self.assertEqual(ent.room, None)

    print(ent.debug())

  def test_namelist(self):
    ent = entity_data.entity_data()
    ent.name = "a goblin"
    ent.namelist = namelist_data.namelist_data("goblin")
    ent.ldesc = "A goblin stands here, smiling mischievously."
    ent.desc = "<p>It looks like it has something up its sleeve.</p>"

    ent.add_alias("smelly")
    ent.add_alias("tiny")
    ent.add_alias("ugly")

    self.assertEqual(ent.num_aliases, 4)
    ent.remove_alias("tiny")
    self.assertEqual(ent.num_aliases, 3)
    ent.remove_all_aliases()
    self.assertEqual(ent.num_aliases, 0)

if __name__ == "__main__":
  unittest.main()