import exit_data
import room_attribute_data

import unittest

class TestRoomAttribute(unittest.TestCase):
  def test_getters(self):
    r_att = room_attribute_data.room_attribute_data("zone_id", "id", "name", "description")

    self.assertEqual(r_att.name, "name")
    self.assertEqual(r_att.desc, "description")
    self.assertEqual(r_att.id, "id")
    self.assertEqual(r_att.zone_id, "zone_id")

  def test_setters(self):
    r_att = room_attribute_data.room_attribute_data()

    r_att.name = "name"
    r_att.desc = "description"
    r_att.id = "id"
    r_att.zone_id = "zone_id"

    self.assertEqual(r_att.name, "name")
    self.assertEqual(r_att.desc, "description")
    self.assertEqual(r_att.id, "id")
    self.assertEqual(r_att.zone_id, "zone_id")

  def test_connections(self):
    r_att = room_attribute_data.room_attribute_data("name", "description")

    # connect a room
    r_att.connect(exit_data.direction.NORTH, "casino", "elevator07")

    # test has_exit(dir)
    self.assertTrue(r_att.has_exit(exit_data.direction.NORTH))

    # test exit(dir)
    ex = r_att.exit(exit_data.direction.NORTH)

    # make sure fields were copied properly to the exit
    self.assertEqual(ex.direction, exit_data.direction.NORTH)
    self.assertEqual(ex.zone_id, "casino")
    self.assertEqual(ex.id, "elevator07")

    # test destination(dir)
    dest = r_att.destination(exit_data.direction.NORTH)

    # destination returned as a unique_id_data
    self.assertEqual(dest.zone_id, "casino")
    self.assertEqual(dest.id, "elevator07")

    print(r_att.debug())

    # test disconnect(dir)
    r_att.disconnect(exit_data.direction.NORTH)
    ex = r_att.exit(exit_data.direction.NORTH)
    dest = r_att.destination(exit_data.direction.NORTH)
    self.assertFalse(r_att.has_exit(exit_data.direction.NORTH))
    self.assertIsNone(ex)
    self.assertIsNone(dest)

  def test_exit_letters(self):
    r_att = room_attribute_data.room_attribute_data("name", "description")

    r_att.connect(exit_data.direction.EAST, None, "elevator08")
    r_att.connect(exit_data.direction.NORTH, None, "elevator07")
    r_att.connect(exit_data.direction.UP, None, "elevator09")

    # test num_exits
    self.assertEqual(r_att.num_exits, 3)

    # test exit_letters
    self.assertEqual(r_att.exit_letters, "n e u ")

    # test disply_exists
    self.assertEqual(r_att.display_exits, "[ Exits: n e u ]")

if __name__ == "__main__":
  unittest.main()