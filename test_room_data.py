import character_data
import object_data
import exit_data
import room_attribute_data
import room_data
import text_data
import unittest

class TestRoomData(unittest.TestCase):
  def test_room_data(self):
    rm = room_data.room_data()

    rm.name = "A Long Dark Hallway"
    rm.desc = text_data.text_data("<p>It is cold, dark, and damp, and miserable.</p>")
    rm.id = "cold_hallway"
    rm.zone_id = "newbie_zone"

    self.assertEqual(rm.name, "A Long Dark Hallway")
    self.assertEqual(rm.desc.text, "<p>It is cold, dark, and damp, and miserable.</p>")
    self.assertEqual(rm.id, "cold_hallway")
    self.assertEqual(rm.zone_id, "newbie_zone")

    rm.connect(exit_data.direction.NORTH, "newbie_zone", "cold_hallway2")

    print(rm.debug())

  def test_load_attributes(self):
    rad = room_attribute_data.room_attribute_data()

    rad.name = "a new room"
    rad.desc = text_data.text_data("this room looks new")
    rad.id = "new_room"
    rad.zone_id = "new_zone"

    rm = room_data.room_data()
    rm.load_attributes(rad)

    self.assertEqual(rm.name, "a new room")
    self.assertEqual(rm.desc.text, "this room looks new")
    self.assertEqual(rm.id, "new_room")
    self.assertEqual(rm.zone_id, "new_zone")

  def test_add_remove_chars(self):
    rm = room_data.room_data()

    rm.name = "A Long Dark Hallway"
    rm.desc = text_data.text_data("<p>It is cold, dark, and damp, and miserable.</p>")
    rm.id = "cold_hallway"
    rm.zone_id = "newbie_zone"

    dummy = character_data.character_data()
    obj = object_data.object_data()

    rm.add_char(dummy)
    rm.add_obj(obj)

    self.assertTrue(rm.has_char(dummy))
    self.assertTrue(rm.has_object(obj))

    rm.remove_char(dummy)
    rm.remove_object(obj)

    self.assertFalse(rm.has_char(dummy))
    self.assertFalse(rm.has_object(obj))

  def test_char_by_alias(self):
    rm = room_data.room_data()

    dummy = character_data.character_data()
    dummy.add_alias("dummy")

    rm.add_char(dummy)

    self.assertIs(rm.char_by_alias("dummy"), dummy)
    print(rm.debug())
if __name__ == "__main__":
  unittest.main()