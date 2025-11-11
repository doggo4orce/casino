import unittest

# local modules
import character_data
import commands
import config
import database
import descriptor_data
import exit_data
import game_data
import nanny
import npc_data
import object_data
import pc_data
import room_data
import server
import test_utilities
import unique_id_data
import zone_data

class TestCommands(unittest.TestCase):
  def test_colors(self):
    # create a character
    ch = character_data.character_data()

    commands.do_colors(ch, None, None, None, None, None)

  def test_look(self):
    # create tiny test world
    mud, zone, room = test_utilities.create_single_room_test_world()

    # add a player to the room
    player = pc_data.pc_data()
    mud.add_character_to_room(player, room)

    # add an object as well
    obj = object_data.object_data()
    obj.add_alias("object")
    mud.add_obj_to_room(obj, room)

    # and an npc
    npc = npc_data.npc_data()
    npc.add_alias("npc")
    mud.add_character_to_room(npc, room)

    commands.do_look(player, None, "", None, mud, None)
    commands.do_look(player, None, "object", None, mud, None)
    commands.do_look(player, None, "npc", None, mud, None)

  def test_get_drop_inventory(self):
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

    commands.do_inventory(ch, None, "", None, mud, None)

    # character drops the item
    commands.do_drop(ch, None, alias, None, mud, None)

    self.assertFalse(ch.has_object(obj))

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

  def test_help(self):
    debug_mode = config.DEBUG_MODE
    config.DEBUG_MODE = False
    mud = game_data.game_data()
    db = database.database(":memory:")
    db.connect()
    db.create_tables()
    db.load_stock() # hard codes content into DB, eventually this won't be here
    mud.load_world(db)
    mud.startup()

    # add player to starting room
    player = pc_data.pc_data()
    mud.add_character_to_room(player, mud.room_by_uid(unique_id_data.unique_id_data.from_string(config.STARTING_ROOM)))

    # give them a descriptor because olc relies on it
    d = descriptor_data.descriptor_data(None, "localhost")
    d.state = descriptor_data.descriptor_state.CHATTING
    player.descriptor = d
    d.character = player

    # initiate nanny.  I'm basically initiating global variables here.  nanny should be a class to avoid this
    cmd_dict = dict()
    nanny.init_commands()

    n = 150

    while n > 1:
      # test redit command with page_width n
      commands.do_prefs(player, None, f"set page_width {n}", None, mud, None)
      d.input_stream.input_q.append("help")
      nanny.handle_next_input(d, None, mud, db)
      # print(f"{'-'*n}")
      # print(d.out_buf)
      # d.out_buf = ""
      n -= 1

    config.DEBUG_MODE = debug_mode

  def test_db(self):
    debug_mode = config.DEBUG_MODE
    config.DEBUG_MODE = True

    # create tiny test world
    mud = game_data.game_data()

    # load the stock world into a database, we want lots of tables to test
    db = database.database(":memory:")
    db.connect()
    db.create_tables()
    db.load_stock() # hard codes content into DB, eventually this won't be here
    mud.load_world(db)
    mud.startup()

    # add a player to the room
    player = pc_data.pc_data()
    mud.add_character_to_room(player, mud.room_by_uid(unique_id_data.unique_id_data.from_string(config.STARTING_ROOM)))

    # give them a descriptor because we need to see their output
    d = descriptor_data.descriptor_data(None, "localhost")
    d.state = descriptor_data.descriptor_state.CHATTING
    player.descriptor, d.character = d, player

    # initiate nanny.  I'm basically initiating global variables here.  nanny should be a class to avoid this
    cmd_dict = dict()
    nanny.init_commands()

    d.input_stream.input_q.append("db show tables")
    nanny.handle_next_input(d, None, mud, db)

    options = ['columns', 'records']

    tables = [
      'ex_table',
      'pref_table_numeric',
      'pref_table_text',
      'pref_table_flags',
      'npc_proto_table',
      'obj_proto_table',
      'wld_proto_table',
      'p_table',
      'z_table',
      'alias_table',
      'wrong_table'           # one table doesn't exist
    ]

    for opt in options:
      for table in tables:
        d.input_stream.input_q.append(f"db {opt} {table}")
        nanny.handle_next_input(d, None, mud, db)

    print(d.out_buf)

    config.DEBUG_MODE = debug_mode

    # teardown
    db.close()


  def test_prefs(self):
    # create tiny test world
    mud, zone, room = test_utilities.create_single_room_test_world()

    # add a player to the room
    player = pc_data.pc_data()

    commands.do_prefs(player, None, "", None, mud, None)

  def test_give(self):
    mud, zone, room = test_utilities.create_single_room_test_world()

    # create characters to test the action
    giver = character_data.character_data()
    receiver = npc_data.npc_data()
    giver.add_alias("generous")
    receiver.add_alias("greedy")
    mud.add_character_to_room(giver, room)
    mud.add_character_to_room(receiver, room)

    self.assertIs(room.char_by_alias("greedy"), receiver)

    # giver needs an object to give
    gift = object_data.object_data()
    giver.give_object(gift)
    gift.add_alias("toy")

    # look around
    commands.do_look(giver, None, "", None, mud, None)

    # perform the give
    commands.do_give(giver, None, "toy greedy", None, mud, None)

    self.assertFalse(giver.has_object(gift))
    self.assertTrue(receiver.has_object(gift))

if __name__ == '__main__':
  config.DEBUG_MODE = False
  unittest.main()