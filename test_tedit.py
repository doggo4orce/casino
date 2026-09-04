import config
import descriptor_data
import database
import db_column
import db_table
import olc
import pc_data
import redit
import tedit
import test_utilities
import unittest

class TestTEDIT(unittest.TestCase):
  def test_create_new_table_and_change_its_name(self):
    db = database.database(":memory:")
    db.connect()

    # create player/descriptor combo
    player = pc_data.pc_data()
    d = descriptor_data.descriptor_data(None, "localhost")

    # connect them
    player.descriptor = d
    d.character = player
    d.state = descriptor_data.descriptor_state.CHATTING

    # create a single room so they can perform tedit command
    mud, zone, room = test_utilities.create_single_room_test_world()

    mud.add_character_to_room(player, room)

    # make a new table and change its name    
    olc.do_tedit(player, None, "table", None, mud, db, None)

    # select edit name
    tedit.tedit_parse(d, "1", db)

    # choose new name
    tedit.tedit_parse(d, "new_table", db)

    # select edit schema
    tedit.tedit_parse(d, "2", db)

    # select add column
    tedit.tedit_parse(d, "1", db)

    # select edit name
    tedit.tedit_parse(d, "1", db)

    # choose new name
    tedit.tedit_parse(d, "id", db)

    # choose edit type
    tedit.tedit_parse(d, "2", db)

    # select type
    tedit.tedit_parse(d, "1", db)

    # toggle is_primary
    tedit.tedit_parse(d, "3", db)

    # save
    tedit.tedit_parse(d, "q", db)

    # confirm
    tedit.tedit_parse(d, "y", db)

    # select add column
    tedit.tedit_parse(d, "1", db)

    # select edit name
    tedit.tedit_parse(d, "1", db)

    # choose new name
    tedit.tedit_parse(d, "name", db)

    # choose edit type
    tedit.tedit_parse(d, "2", db)

    # select type
    tedit.tedit_parse(d, "2", db)

    # save
    tedit.tedit_parse(d, "q", db)

    # confirm
    tedit.tedit_parse(d, "y", db)

    # back to main menu
    tedit.tedit_parse(d, "q", db)

    # save changes
    tedit.tedit_parse(d, "q", db)

    # confirm
    tedit.tedit_parse(d, "y", db)

    self.assertFalse(db.table_exists("table"))
    self.assertTrue(db.table_exists("new_table"))

    self.assertEqual(table.num_columns(), 2)

    self.assertTrue(table.has_column('id', int, True))
    self.assertTrue(table.has_column('name', str, False))

  def test_edit_existing_table(self):
    db = database.database(":memory:")
    db.connect()

    # create player/descriptor combo
    player = pc_data.pc_data()
    d = descriptor_data.descriptor_data(None, "localhost")

    # connect them
    player.descriptor = d
    d.character = player
    d.state = descriptor_data.descriptor_state.CHATTING

    # create a single room so they can perform tedit command
    mud, zone, room = test_utilities.create_single_room_test_world()

    mud.add_character_to_room(player, room)

    # setup table
    db.create_table("test_table",
      ("id", int, True),
      ("name", str, False),
      ("last_name", str, False)
    )

    # now edit it   
    olc.do_tedit(player, None, "test_table", None, mud, db, None)

    # select edit name
    tedit.tedit_parse(d, "1", db)

    # choose new name
    tedit.tedit_parse(d, "new_table", db)

    # select edit schema
    tedit.tedit_parse(d, "2", db)

    # select drop column
    tedit.tedit_parse(d, "2", db)

    # choose which column to drop
    tedit.tedit_parse(d, "id", db)

    # select add column
    tedit.tedit_parse(d, "1", db)

    # select choose column
    tedit.tedit_parse(d, "1", db)

    # choose new name
    tedit.tedit_parse(d, "first_name", db)

    # choose edit type
    tedit.tedit_parse(d, "2", db)

    # select type
    tedit.tedit_parse(d, "2", db)

    # set primary
    tedit.tedit_parse(d, "3", db)

    # save
    tedit.tedit_parse(d, "q", db)

    # confirm
    tedit.tedit_parse(d, "y", db)

    # back to main menu
    tedit.tedit_parse(d, "q", db)

    # save
    tedit.tedit_parse(d, "q", db)

    # confirm
    tedit.tedit_parse(d, "y", db)

    self.assertFalse(db.table_exists("test_table"))
    self.assertTrue(db.table_exists("new_table"))

    table = db.table_by_name("new_table")

    self.assertEqual(table.num_columns(), 3)

    self.assertTrue(table.has_column('name', str, False))
    self.assertTrue(table.has_column('last_name', str, False))
    self.assertTrue(table.has_column('first_name', str, True))

  def test_rename_columns(self):
    db = database.database(":memory:")
    db.connect()

    # create player/descriptor combo
    player = pc_data.pc_data()
    d = descriptor_data.descriptor_data(None, "localhost")

    # connect them
    player.descriptor = d
    d.character = player
    d.state = descriptor_data.descriptor_state.CHATTING

    # create a single room so they can perform tedit command
    mud, zone, room = test_utilities.create_single_room_test_world()

    mud.add_character_to_room(player, room)

    # setup table
    db.create_table("test_table",
      ("id", int, True),
      ("name", str, False),
      ("last_name", str, False)
    )

    # now edit it   
    olc.do_tedit(player, None, "test_table", None, mud, db, None)

    # select edit schema
    tedit.tedit_parse(d, "2", db)

    # select rename column
    tedit.tedit_parse(d, "3", db)

    # choose column to rename
    tedit.tedit_parse(d, "id", db)

    # select new name
    tedit.tedit_parse(d, "new_id", db)

    # back to main menu
    tedit.tedit_parse(d, "q", db)

    # save changes
    tedit.tedit_parse(d, "q", db)

    # confirm save
    tedit.tedit_parse(d, "y", db)

    print(db.table_by_name("test_table").debug())

if __name__ == "__main__":
  config.DEBUG_MODE = False
  unittest.main()
  #unittest.main(defaultTest="TestTEDIT.test_rename_columns")