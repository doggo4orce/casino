import unittest
import medit
import test_utilities

class TestZeditSave(unittest.TestCase):
  def test_create_npc(self):
    # create tiny test world
    mud, zone, room = test_utilities.create_single_room_test_world()

    