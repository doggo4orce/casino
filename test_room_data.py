import database
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

  def test_save_exit(self):
    db = database.database(":memory:",test=True)
    db.create_tables()

    rm = room_data.room_data()
    rm.id = "hallway"
    rm.zone_id = "newbie_zone"

    ex = exit_data.exit_data(exit_data.direction.EAST, "newbie_zone", "hallway2")

    db.save_exit(rm, ex)

    self.assertTrue(db.contains_exit(rm, exit_data.direction.EAST))

  # def test_save_room(self):
  #   db = database.database(":memory:",test=True)
  #   db.create_tables()

  #   db.save_room(rm)

if __name__ == "__main__":
  unittest.main()