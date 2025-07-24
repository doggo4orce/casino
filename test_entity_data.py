import entity_data
import entity_proto_data
import namelist_data
import unique_id_data

import unittest

class TestEntity(unittest.TestCase):
  def test_entity(self):
    ent = entity_data.entity_data()

    ent.name = "a young dog"
    ent.remove_all_aliases()
    ent.add_alias("dog")
    ent.add_alias("young")
    ent.add_alias("puppy")
    ent.ldesc = "A young dog chases after a ball."
    ent.desc = "<p>It looks like a young puppy.</p>"

    self.assertTrue(ent.has_alias("young"))
    self.assertTrue(ent.has_alias("dog"))
    self.assertTrue(ent.has_alias("puppy"))
    self.assertFalse(ent.has_alias("cat"))
    self.assertEqual(ent.num_aliases, 3)

    self.assertEqual(ent.Name, "A young dog")
    self.assertEqual(ent.ldesc, "A young dog chases after a ball.")
    self.assertEqual(ent.desc, "<p>It looks like a young puppy.</p>")
    self.assertEqual(ent.room, None)

    print(ent.debug())

  def test_namelist(self):
    ent = entity_data.entity_data()
    ent.name = "a goblin"
    ent.remove_all_aliases()
    ent.add_alias("goblin")
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

  def test_alias_list(self):
    ent = entity_data.entity_data()
    ent.reset_aliases("goblin", "thief")
    
    names = ent.aliases()

    self.assertIn("goblin", names)
    self.assertIn("thief", names)
    self.assertEqual(len(names), 2)

  def test_copy(self):
    ent = entity_data.entity_data()
    ent.name = "a young dog"
    ent.remove_all_aliases()
    ent.add_alias("dog")
    ent.add_alias("young")
    ent.add_alias("puppy")
    ent.ldesc = "A young dog chases after a ball."
    ent.desc = "<p>It looks like a young puppy.</p>"
    ent.room = unique_id_data.unique_id_data("casino", "bathroom")


    ent2 = entity_data.entity_data()
    ent2.copy_from(ent)

    self.assertEqual(ent.name, ent2.name)
    self.assertEqual(ent.desc, ent2.desc)

    self.assertEqual(ent.aliases(), ent2.aliases())

    ent.remove_alias("young")
    self.assertFalse(ent.has_alias("young"))
    self.assertTrue(ent2.has_alias("young"))
    
if __name__ == "__main__":
  unittest.main()