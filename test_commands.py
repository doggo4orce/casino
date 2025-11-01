import unittest

# local modules
import character_data
import commands
import database
import exit_data
import game_data
import npc_data
import object_data
import pc_data
import room_data
import server
import test_utilities
import zone_data

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

  def test_move(self):
    # create rooms to walk around in
    n_room = room_data.room_data()
    n_room.id = "n_room"
    n_room.zone_id = "test_zone"
    w_room = room_data.room_data()
    w_room.id = "w_room"
    w_room.zone_id = "test_zone"
    u_room = room_data.room_data()
    u_room.id = "u_room"
    u_room.zone_id = "test_zone"
    c_room = room_data.room_data()
    c_room.id = "c_room"
    c_room.zone_id = "test_zone"

    # connect the rooms
    n_room.connect(exit_data.direction.SOUTH, "test_zone", "c_room")
    c_room.connect(exit_data.direction.NORTH, "test_zone", "n_room")
    w_room.connect(exit_data.direction.EAST, "test_zone", "c_room")
    c_room.connect(exit_data.direction.WEST, "test_zone", "w_room")
    u_room.connect(exit_data.direction.DOWN, "test_zone", "c_room")
    c_room.connect(exit_data.direction.UP, "test_zone", "u_room")

    # create a zone to hold them
    zone = zone_data.zone_data()
    zone.id = "test_zone"
    zone.add_room(n_room)
    zone.add_room(w_room)
    zone.add_room(u_room)
    zone.add_room(c_room)

    # create a game with just this zone
    mud = game_data.game_data()
    mud.add_zone(zone)

    # create a character to walk around
    ch = character_data.character_data()

    mud.add_character_to_room(ch, c_room)

    # go north
    commands.do_move(ch, exit_data.direction.NORTH, None, None, mud, None)
    self.assertIn(ch, n_room.people)
    self.assertNotIn(ch, c_room.people)

    # go south
    commands.do_move(ch, exit_data.direction.SOUTH, None, None, mud, None)
    self.assertIn(ch, c_room.people)
    self.assertNotIn(ch, n_room.people)

    # go west
    commands.do_move(ch, exit_data.direction.WEST, None, None, mud, None)
    self.assertIn(ch, w_room.people)
    self.assertNotIn(ch, c_room.people)

    # go east
    commands.do_move(ch, exit_data.direction.EAST, None, None, mud, None)
    self.assertIn(ch, c_room.people)
    self.assertNotIn(ch, w_room.people)

    # go up
    commands.do_move(ch, exit_data.direction.UP, None, None, mud, None)
    self.assertIn(ch, u_room.people)
    self.assertNotIn(ch, c_room.people)

    # go down
    commands.do_move(ch, exit_data.direction.DOWN, None, None, mud, None)
    self.assertIn(ch, c_room.people)
    self.assertNotIn(ch, u_room.people)

  def test_move_away_from_mob_with_scripts(self):
    
if __name__ == '__main__':
  unittest.main()