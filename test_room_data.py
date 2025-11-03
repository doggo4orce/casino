import character_data
import object_data
import exit_data
import room_data

import unittest

class TestRoomData(unittest.TestCase):
  def test_room_data(self):
    rm = room_data.room_data()

    rm.name = "A Long Dark Hallway"
    rm.desc = "<p>It is cold, dark, and damp, and miserable.</p>"
    rm.id = "cold_hallway"
    rm.zone_id = "newbie_zone"

    self.assertEqual(rm.name, "A Long Dark Hallway")
    self.assertEqual(rm.desc, "<p>It is cold, dark, and damp, and miserable.</p>")
    self.assertEqual(rm.id, "cold_hallway")
    self.assertEqual(rm.zone_id, "newbie_zone")

    rm.connect(exit_data.direction.NORTH, "newbie_zone", "cold_hallway2")

    print(rm.debug())

  def test_add_remove_chars(self):
    rm = room_data.room_data()

    rm.name = "A Long Dark Hallway"
    rm.desc = "<p>It is cold, dark, and damp, and miserable.</p>"
    rm.id = "cold_hallway"
    rm.zone_id = "newbie_zone"

    dummy = character_data.character_data()
    obj = object_data.object_data()

    rm.add_char(dummy)
    rm.add_obj(obj)

    self.assertTrue(rm.has_char(dummy))
    self.assertTrue(rm.has_obj(obj))

    rm.remove_char(dummy)
    rm.remove_obj(obj)

    self.assertFalse(rm.has_char(dummy))
    self.assertFalse(rm.has_obj(obj))

if __name__ == "__main__":
  unittest.main()