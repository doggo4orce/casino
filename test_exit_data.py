import exit_data
import unittest

class TestExit(unittest.TestCase):
  def test_exit(self):
    ex = exit_data.exit_data(exit_data.direction.NORTH, "goblin_cave", "small_hole")
    self.assertEqual(ex.direction, exit_data.direction.NORTH)
    self.assertEqual(ex.id, "small_hole")
    self.assertEqual(ex.zone_id, "goblin_cave")

  def test_setters(self):
    ex = exit_data.exit_data()

    ex.direction = exit_data.direction.EAST
    ex.id = "cozy_cottage"
    ex.zone_id = "village"

    self.assertEqual(ex.direction, exit_data.direction.EAST)
    self.assertEqual(ex.id, "cozy_cottage")
    self.assertEqual(ex.zone_id, "village")

  def test_internal(self):
    ex = exit_data.exit_data()

    ex.direction = exit_data.direction.UP
    ex.id = "local"
    ex.zone_id = None

    self.assertTrue(ex.internal)

    ex.zone_id = "global"
    self.assertFalse(ex.internal)

    # if no destination, exit is neither internal nor external
    ex.id = None
    ex.zone_id = None
    self.assertFalse(ex.internal)

if __name__ == "__main__":
  unittest.main()
