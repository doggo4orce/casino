import config
import pc
import structs
import unittest

class TestPC(unittest.TestCase):

  def test_10_entity_aaa(self):
    print("test_entity")
    ent = structs.entity_data()
    ent.name = "a young dog"
    ent.namelist = ["dog", "young"]
    ent.ldesc = "A young dog chases after a ball."
    ent.desc = "<p>It looks like a young puppy.</p>"
    print("\n---\n", ent.debug(), "---\n")
    self.assertTrue(ent.has_alias("young"))
    self.assertTrue(ent.has_alias("dog"))
    self.assertFalse(ent.has_alias("cat"))
    self.assertEqual(ent.Name, "A young dog")
    self.assertEqual(ent.room, None)

    print(vars(ent))
    
  def test_20_character(self):
    print("test_character")
    char = pc.character()

    print("\n---\n", char.debug(), "---\n")

    print(vars(char))

  def test_npc(self):
    pass

  def test_pc(self):
    pass

