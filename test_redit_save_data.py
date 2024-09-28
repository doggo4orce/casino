import exit_data

import redit_save_data

import unittest

class TestReditSaveData(unittest.TestCase):
  def test_redit_save_data(self):
    rsd = redit_save_data.redit_save_data("zone_id", "id")

    self.assertEqual(rsd.r_attr.zone_id, "zone_id")
    self.assertEqual(rsd.r_attr.id, "id")

    rsd.dir_edit = exit_data.direction.NORTH
    rsd.r_attr.name = "a new room"
    rsd.r_attr.desc = "some description"

    self.assertEqual(rsd.dir_edit, exit_data.direction.NORTH)
    self.assertEqual(rsd.r_attr.name, "a new room")
    self.assertEqual(rsd.r_attr.desc, "some description")

if __name__ == '__main__':
  unittest.main()