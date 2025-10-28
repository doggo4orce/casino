import unittest

# local modules
import commands
import npc_data
import object_data
import pc_data
import test_utilities

class TestCommands(unittest.TestCase):
  def test_look(self):
    mud, zone, room = test_utilities.create_single_room_test_world()

    # add a player to the room
    player = pc_data.pc_data()
    mud.add_character_to_room(player, room)

    # add an object as well
    obj = object_data.object_data()
    mud.add_obj_to_room(obj, room)

    # and an npc
    npc = npc_data.npc_data()
    mud.add_character_to_room(npc, room)

    commands.show_room_to_char(player, room)

if __name__ == '__main__':
  unittest.main()