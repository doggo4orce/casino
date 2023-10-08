import config
import pc
import unittest

class TestPC(unittest.TestCase):
    
  def test_20_character(self):
    print("test_character")
    char = pc.character()

    print("\n---\n", char.debug(), "---\n")

    print(vars(char))

  def test_npc(self):
    pass

  def test_pc(self):
    pass

