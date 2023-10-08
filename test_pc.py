import config
import pc
import structs
import unittest

class TestPC(unittest.TestCase):

  def test_entity(self):
    ent = structs.entity_data()
    ent.name = "a young dog"
    ent.namelist = ["dog", "young"]
    ent.ldesc = "A young dog chases after a ball."
    ent.desc = "<p>It looks like a young puppy.</p>"

    self.assertTrue(ent.has_alias("young"))
    self.assertTrue(ent.has_alias("dog"))
    self.assertFalse(ent.has_alias("cat"))
    self.assertEqual(ent.Name, "A young dog")
    self.assertEqual(ent.room, structs.unique_identifier.from_string(config.VOID_ROOM))
    
  def test_character(self):
    char = pc.character()

  def test_npc(self):
    pass

  def test_pc(self):
    pass

