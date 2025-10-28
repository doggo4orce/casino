import unittest

# local modules
import character_data
import commands
import database
import npc_data
import object_data
import pc_data
import server
import test_utilities

class TestCommands(unittest.TestCase):
  def test_colors(self):
    # create a character
    ch = character_data.character_data()

    commands.do_colors(ch, None, None, None, None, None)

  def test_look(self):
    # create tiny test world
    mud, zone, room = test_utilities.create_single_room_test_world()

    room.desc = "<p>This is the recall point of Stockville City.  You should be able to get here by typing <c11>RECALL<c0> at <c6>a<c2>n<c5>y<c0> time.</p>"
    # add a player to the room
    player = pc_data.pc_data()
    mud.add_character_to_room(player, room)

    # add an object as well
    obj = object_data.object_data()
    mud.add_obj_to_room(obj, room)

    # and an npc
    npc = npc_data.npc_data()
    mud.add_character_to_room(npc, room)

    commands.do_look(player, None, "", None, mud, None)
    
  def test_get(self):
    # create tiny test world
    mud, zone, room = test_utilities.create_single_room_test_world()

    # add a character to the room
    ch = character_data.character_data()
    mud.add_character_to_room(ch, room)

    # put object in the room
    obj = object_data.object_data()
    mud.add_obj_to_room(obj, room)

    # get the object's first alias
    alias = obj.aliases()[0]

    # character picks up the item
    commands.do_get(ch, None, alias, None, mud, None)

    self.assertTrue(ch.has_object(obj))

if __name__ == '__main__':
  unittest.main()