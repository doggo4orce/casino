import buffer_data
import config
import descriptor_data
import database
import editor
import game_data
import olc
import olc_data
import pc_data
import redit
import unittest
import unique_id_data

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
    room = mud.room_by_uid(unique_id_data.unique_id_data.from_string(config.STARTING_ROOM))
    mud.add_character_to_room(player, room)

    # give them a descriptor because olc relies on it
    d = descriptor_data.descriptor_data(None, "localhost")
    player.descriptor = d
    d.character = player

    # test redit command
    olc.do_redit(player, None, "", None, mud, db)

    # select change room desc
    olc.handle_input(player.descriptor, '2', None, mud, db)

    self.assertTrue(player.descriptor.writing)
    self.assertEqual(player.descriptor.olc.state, redit.redit_state.REDIT_EDIT_DESC)

    # show existing new room description
    editor.editor_handle_input(player.descriptor, '/l')

    # self.assertFalse(player.descriptor.writing)

    # self.assertEqual(str(d.write_buffer), str(buffer_data.buffer_data(room.desc)))

    # # edit new room description
    # olc.handle_input(player.descriptor, 'new line', None, mud, db)

    # # save new description
    # olc.handle_input(player.descriptor, '/s', None, mud, db)

    # # quit
    # olc.handle_input(player.descriptor, 'q', None, mud, db)

if __name__ == "__main__":
  unittest.main()