import unittest
import zedit_save_data

class TestZeditSave(unittest.TestCase):
  def test_zedit_save(self):
    zsd = zedit_save_data.zedit_save_data("goblin_forest", "Goblin Forest", "Jack", "Goblin Folder")
    self.assertEqual(zsd.id, "goblin_forest")
    self.assertEqual(zsd.name, "Goblin Forest")
    self.assertEqual(zsd.author, "Jack")
    self.assertEqual(zsd.folder, "Goblin Folder")

  def test_setters_getters(self):
    zsd = zedit_save_data.zedit_save_data()
    zsd.id = "goblin_forest"
    zsd.name = "Goblin Forest"
    zsd.author = "Jack"
    zsd.folder = "Goblin Folder"

    self.assertEqual(zsd.id, "goblin_forest")
    self.assertEqual(zsd.name, "Goblin Forest")
    self.assertEqual(zsd.author, "Jack")
    self.assertEqual(zsd.folder, "Goblin Folder")

if __name__ == "__main__":
  unittest.main()