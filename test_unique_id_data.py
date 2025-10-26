import unittest
import unique_id_data

class TestUniqueID(unittest.TestCase):
  def test_unique_id_data(self):
    """Testing the constructor, getters, and setters"""
    uid = unique_id_data.unique_id_data("newbie_zone", "newbie_dagger")
    self.assertEqual(uid.zone_id, "newbie_zone")
    self.assertEqual(uid.id, "newbie_dagger")

    uid.zone_id = "dwarf_fortress"
    uid.id = "battle_axe"
    self.assertEqual(uid.zone_id, "dwarf_fortress")
    self.assertEqual(uid.id, "battle_axe")

    uid.zone_id = "dwarf!fortress"
    self.assertIsNone(uid.zone_id, None)
    self.assertEqual(uid.id, "battle_axe")

    uid = unique_id_data.unique_id_data("bad zone name", "bad local id")
    self.assertIsNone(uid.zone_id)
    self.assertIsNone(uid.id)

    uid = unique_id_data.unique_id_data.from_string("casino@stockville")
    self.assertEqual(uid.zone_id, "stockville")
    self.assertEqual(uid.id, "casino")

    uid.zone_id = None
    self.assertEqual(uid.zone_id, None)

    self.assertEqual(str(uid), "casino")

    uid.id = None
    self.assertEqual(uid.id, None)

    uid2 = unique_id_data.unique_id_data(uid.zone_id, uid.id)
    self.assertEqual(uid, uid2)

if __name__ == "__main__":
  unittest.main()