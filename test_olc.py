import buffer_data
import config
import descriptor_data
import database
import editor
import game_data
import nanny
import olc
import olc_data
import pc_data
import redit
import socket
import unittest
import unique_id_data
import zedit

class TestOLC(unittest.TestCase):
  def test_redit_quit(self):
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
    player.descriptor = d
    d.character = player

    # test redit command
    olc.do_redit(player, None, "", None, mud, db)

    # immediately quit
    olc.handle_input(player.descriptor, 'q', None, mud, db)

  def test_redit_change_room_name(self):
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
    player.descriptor = d
    d.character = player

    # test redit command
    olc.do_redit(player, None, "", None, mud, db)

    self.assertEqual(player.descriptor.olc.mode, olc_data.olc_mode.OLC_MODE_REDIT)
    self.assertEqual(player.descriptor.olc.state, redit.redit_state.REDIT_MAIN_MENU)

    # select change room name
    olc.handle_input(player.descriptor, '1', None, mud, db)

    self.assertEqual(player.descriptor.olc.state, redit.redit_state.REDIT_EDIT_NAME)

    # choose new room name
    olc.handle_input(player.descriptor, 'new room name', None, mud, db)

    self.assertEqual(player.descriptor.olc.state, redit.redit_state.REDIT_MAIN_MENU)

    # quit
    olc.handle_input(player.descriptor, 'q', None, mud, db)

    self.assertEqual(player.descriptor.olc.state, redit.redit_state.REDIT_CONFIRM_SAVE)

    # save internally
    olc.handle_input(player.descriptor, 'y', None, mud, db)

  def test_redit_change_room_desc(self):
    mud = game_data.game_data()
    db = database.database(":memory:")
    db.connect()
    db.create_tables()
    db.load_stock() # hard codes content into DB, eventually this won't be here
    mud.load_world(db)
    mud.startup()

    # add player to starting room
    player = pc_data.pc_data()
    player.name = "test_char"
    room = mud.room_by_uid(unique_id_data.unique_id_data.from_string(config.STARTING_ROOM))
    mud.add_character_to_room(player, room)
    room.desc.text = "first line"

    # give them a descriptor because olc relies on it
    client, host = socket.socketpair()
    d = descriptor_data.descriptor_data(host, "localhost")
    d.state = descriptor_data.descriptor_state.CHATTING
    player.descriptor = d
    d.character = player

    # initiate nanny.  I'm basically initiating global variables here.  nanny should be a class to avoid this
    cmd_dict = dict()
    nanny.init_commands()

    # have the user enter redit command
    d.input_stream.input_q.append("redit")
    nanny.handle_next_input(d, None, mud, db)

    # they should be in the main menu
    self.assertEqual(player.descriptor.olc.state, redit.redit_state.REDIT_MAIN_MENU)

    # select change room desc
    d.input_stream.input_q.append("2")
    nanny.handle_next_input(d, None, mud, db)

    # they should be editing the description
    self.assertTrue(d.writing)
    self.assertEqual(d.olc.state, redit.redit_state.REDIT_EDIT_DESC)

    # edit new room description, editor takes over handling input since player is writing
    d.input_stream.input_q.append("new line")
    nanny.handle_next_input(d, None, mud, db)

    # they should still be editing
    self.assertTrue(d.writing)
    self.assertEqual(d.olc.state, redit.redit_state.REDIT_EDIT_DESC)

    # save new description
    d.input_stream.input_q.append("/s")
    nanny.handle_next_input(d, None, mud, db)

    # user should be back to main menu and no longer writing
    self.assertEqual(d.olc.state, redit.redit_state.REDIT_MAIN_MENU)
    self.assertFalse(d.writing)

    # quit, olc takes over handling input since player is done writing
    d.input_stream.input_q.append("q")
    nanny.handle_next_input(d, None, mud, db)
    self.assertEqual(d.olc.state, redit.redit_state.REDIT_CONFIRM_SAVE)

    # save
    d.input_stream.input_q.append("y")
    nanny.handle_next_input(d, None, mud, db)

    # check to make sure the change was saved
    self.assertEqual(room.desc.text, "first line\r\nnew line")

    # olc data should be gone and player back to normal game
    self.assertIsNone(d.olc)
    self.assertEqual(d.state, descriptor_data.descriptor_state.CHATTING)

    # teardown
    host.close()
    client.close()

  def test_redit_create_new_room(self):
    mud = game_data.game_data()
    db = database.database(":memory:")
    db.connect()
    db.create_tables()
    db.load_stock() # hard codes content into DB, eventually this won't be here
    mud.load_world(db)
    mud.startup()

    # add player to starting room
    player = pc_data.pc_data()
    player.name = "test_char"
    room = mud.room_by_uid(unique_id_data.unique_id_data.from_string(config.STARTING_ROOM))
    mud.add_character_to_room(player, room)

    # give them a descriptor because olc relies on it
    client, host = socket.socketpair()
    d = descriptor_data.descriptor_data(host, "localhost")
    d.state = descriptor_data.descriptor_state.CHATTING
    player.descriptor = d
    d.character = player

    # initiate nanny.  I'm basically initiating global variables here.  nanny should be a class to avoid this
    cmd_dict = dict()
    nanny.init_commands()

    # have the user enter redit command
    d.input_stream.input_q.append("zedit new_zone")
    nanny.handle_next_input(d, None, mud, db)

    print(d.out_buf)
    # # they should be in the main menu
    # self.assertEqual(player.descriptor.olc.state, redit.redit_state.REDIT_MAIN_MENU)
    # nanny.handle_next_input(d, None, mud, db)

    # # select change room desc
    # d.input_stream.input_q.append("2")
    # nanny.handle_next_input(d, None, mud, db)

    # # they should be editing the description
    # self.assertTrue(d.writing)
    # self.assertEqual(d.olc.state, redit.redit_state.REDIT_EDIT_DESC)

    # # edit new room description, editor takes over handling input since player is writing
    # d.input_stream.input_q.append("new line")
    # nanny.handle_next_input(d, None, mud, db)

    # # they should still be editing
    # self.assertTrue(d.writing)
    # self.assertEqual(d.olc.state, redit.redit_state.REDIT_EDIT_DESC)

    # # save new description
    # d.input_stream.input_q.append("/s")
    # nanny.handle_next_input(d, None, mud, db)

    # # user should be back to main menu and no longer writing
    # self.assertEqual(d.olc.state, redit.redit_state.REDIT_MAIN_MENU)
    # self.assertFalse(d.writing)

    # # quit, olc takes over handling input since player is done writing
    # d.input_stream.input_q.append("q")
    # nanny.handle_next_input(d, None, mud, db)
    # self.assertEqual(d.olc.state, redit.redit_state.REDIT_CONFIRM_SAVE)

    # # save
    # d.input_stream.input_q.append("y")
    # nanny.handle_next_input(d, None, mud, db)

    # # check to make sure the change was saved
    # self.assertEqual(room.desc.text, "first line\r\nnew line")

    # # olc data should be gone and player back to normal game
    # self.assertIsNone(d.olc)
    # self.assertEqual(d.state, descriptor_data.descriptor_state.CHATTING)

    # teardown
    host.close()
    client.close()

  def test_zedit_create_new_zone(self):
    mud = game_data.game_data()
    db = database.database(":memory:")
    db.connect()
    db.create_tables()
    db.load_stock() # hard codes content into DB, eventually this won't be here
    mud.load_world(db)
    mud.startup()

    # add player to starting room
    player = pc_data.pc_data()
    player.name = "TestChar"
    room = mud.room_by_uid(unique_id_data.unique_id_data.from_string(config.STARTING_ROOM))
    mud.add_character_to_room(player, room)

    # give them a descriptor because olc relies on it
    client, host = socket.socketpair()
    d = descriptor_data.descriptor_data(host, "localhost")
    d.state = descriptor_data.descriptor_state.CHATTING
    player.descriptor = d
    d.character = player

    # initiate nanny.  I'm basically initiating global variables here.  nanny should be a class to avoid this
    cmd_dict = dict()
    nanny.init_commands()

    # enter zedit command
    d.input_stream.input_q.append("zedit haunted_castle")
    nanny.handle_next_input(d, None, mud, db)

    self.assertEqual(d.olc.state, zedit.zedit_state.ZEDIT_MAIN_MENU)
    
    # change the author
    d.input_stream.input_q.append("1")
    nanny.handle_next_input(d, None, mud, db)

    # choose a new author
    d.input_stream.input_q.append("Charles Dickens")
    nanny.handle_next_input(d, None, mud, db)

    # change the name
    d.input_stream.input_q.append("2")
    nanny.handle_next_input(d, None, mud, db)

    # choose a new name
    d.input_stream.input_q.append("The Haunted Castle")
    nanny.handle_next_input(d, None, mud, db)

    # quit
    d.input_stream.input_q.append("q")
    nanny.handle_next_input(d, None, mud, db)

    # save internally
    d.input_stream.input_q.append("y")
    nanny.handle_next_input(d, None, mud, db)

    print(d.out_buf)

    client.close()
    host.close()
if __name__ == "__main__":
  unittest.main(defaultTest="TestOLC.test_zedit_create_new_zone")