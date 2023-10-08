import config
import pc
import structs
import unittest


class TestPC(unittest.TestCase):

  def test_entity(self):
    ent = structs.entity()

    assertTrue(ent.has_alias("unfinished"))
    assertTrue(ent.has_alias("entity"))
    assertEqual(len(ent.namelist), 2)
    assertEqual(ent.room, structs.unique_identifier.from_string(config.VOID_ROOM))
    
  def test_character(self):
    char = pc.character()

  def test_npc(self):
    pass

  def test_pc(self):
    pass

