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

def test_tedit_parse(d, input, db, verbose):
  if verbose:
    print(d.out_buf, input)
    d.out_buf = ""

  tedit.tedit_parse(d, input, db)

class TestTEDIT(unittest.TestCase):
  def test_new_table(self):
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

    # must be in room to use tedit command
    mud.add_character_to_room(player, room)

    # make a new table and change its name    
    olc.do_tedit(player, None, "test_table", None, mud, db, None)

    verbose = False

    input_q = [
      "2",           # select edit schema
      "1",           # select add column
      "1",           # select edit name
      "id",          # set name to id
      "2",           # select edit type
      "1",           # choose type int
      "3",           # set primary flag
      "q",           # save column changes
      "y",           # confirm save
      "1",           # select add column
      "1",           # select edit name
      "name",        # choose name to be name
      "2",           # choose edit type
      "2",           # select str
      "q",           # save column changes
      "y",           # confirm save
      "q",           # back to main menu
      "q",           # save table changes
      "y"            # confirm save
    ]

    for input in input_q:
      test_tedit_parse(d, input, db, verbose)

    self.assertTrue(db.table_exists("test_table"))

    self.assertTrue(db.has_column("test_table", "id", int, True))
    self.assertTrue(db.has_column("test_table", "name", str, False))
    self.assertEqual(db.num_columns("test_table"), 2)

    db.close()

  def test_new_table_name_change(self):
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
    olc.do_tedit(player, None, "test_table", None, mud, db, None)

    verbose = False

    input_q = [
      "1",           # select edit name
      "new_table",   # choose new name
      "2",           # select edit schema
      "1",           # select add column
      "1",           # select edit name
      "id",          # set name to id
      "2",           # select edit type
      "1",           # choose type int
      "3",           # set primary flag
      "q",           # save column changes
      "y",           # confirm save
      "1",           # select add column
      "1",           # select edit name
      "name",        # choose name to be name
      "2",           # choose edit type
      "2",           # select str
      "q",           # save column changes
      "y",           # confirm save
      "q",           # back to main menu
      "q",           # save table changes
      "y"            # confirm save
    ]

    for input in input_q:
      test_tedit_parse(d, input, db, verbose)

    self.assertFalse(db.table_exists("test_table"))
    self.assertTrue(db.table_exists("new_table"))

    self.assertTrue(db.has_column("new_table", "id", int, True))
    self.assertTrue(db.has_column("new_table", "name", str, False))
    self.assertEqual(db.num_columns("new_table"), 2)

    db.close()
  
  def test_existing_table_name_change(self):
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

    table = db.table_by_name("test_table")

    table.insert_many(
      [
        {"id":13, "name":"kyle", "last_name":"roobiki"},
        {"id":14, "name":"dylan", "last_name":"pianta"}
      ]
    )

    # now edit it   
    olc.do_tedit(player, None, "test_table", None, mud, db, None)

    verbose = False

    input_q = [
      "1",           # select edit name
      "new_table",   # choose new name
      "q",           # save
      "y"            # confirm
    ]

    for input in input_q:
      test_tedit_parse(d, input, db, verbose)

    table = db.table_by_name("new_table")

    self.assertFalse(db.has_table("test_table"))
    self.assertTrue(db.has_table("new_table"))

    self.assertEqual(table.search(id=13, name="kyle", last_name="roobiki").num_results, 1)
    self.assertEqual(table.search(id=14, name="dylan", last_name="pianta").num_results, 1)
    self.assertEqual(table.num_records(), 2)

  def test_drop_table(self):
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

    table = db.table_by_name("test_table")

    table.insert_many(
      [
        {"id":13, "name":"kyle", "last_name":"roobiki"},
        {"id":14, "name":"dylan", "last_name":"pianta"}
      ]
    )

    # now edit it   
    olc.do_tedit(player, None, "test_table", None, mud, db, None)

    verbose = False

    input_q = [
      "X",           # select drop table
      "y"            # confirm
    ]

    for input in input_q:
      test_tedit_parse(d, input, db, verbose)

    self.assertFalse(db.has_table("test_table"))

  def test_edit_existing_table_add_drop_columns(self):
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

    test_table = db.table_by_name("test_table")

    test_table.insert_many(
      [
        {"id":13, "name":"kyle", "last_name":"roobiki"},
        {"id":14, "name":"dylan", "last_name":"pianta"}
      ]
    )

    # now edit it   
    olc.do_tedit(player, None, "test_table", None, mud, db, None)

    verbose = False

    input_q = [
      "2",           # select edit schema
      "2",           # select drop column
      "id",          # choose to drop id
      "1",           # select add column
      "1",           # select choose name
      "first_name",  # add column first_name
      "2",           # edit type
      "2",           # select type as str
      "3",           # set primary flag
      "q",           # save changes to column
      "y",           # confirm save
      "q",           # back to main menu
      "q",           # save
      "y"            # confirm
    ]

    for input in input_q:
      test_tedit_parse(d, input, db, verbose)

    table = db.table_by_name("test_table")

    self.assertTrue(table.has_column('name', str, False))
    self.assertTrue(table.has_column('last_name', str, False))
    self.assertTrue(table.has_column('first_name', str, True))
    self.assertEqual(table.num_columns(), 3)

    kyle_search = table.search(name="kyle")
    dylan_search = table.search(name="dylan")

    self.assertEqual(kyle_search.num_results, 1)
    self.assertEqual(dylan_search.num_results, 1)

    kyle = kyle_search[0]
    dylan = dylan_search[0]

    self.assertEqual(kyle.fields, ["name", "last_name", "first_name"])
    self.assertEqual(dylan.fields, ["name", "last_name", "first_name"])

    self.assertIsNone(kyle["first_name"])
    self.assertIsNone(dylan["first_name"])

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

    table = db.table_by_name("test_table")

    table.insert_many(
      [
        {"id":13, "name":"kyle", "last_name":"roobiki"},
        {"id":14, "name":"dylan", "last_name":"pianta"}
      ]
    )

    # now edit it   
    olc.do_tedit(player, None, "test_table", None, mud, db, None)

    verbose = False

    input_q = [
      "2",           # select edit schema
      "3",           # select rename column
      "id",          # choose id column to rename
      "new_id",      # rename it to new_id
      "3",           # select rename column
      "last_name",   # choose last_name column to rename
      "id",          # rename it to id
      "q",           # save changes to column
      "q",           # save changes to table
      "y"            # confirm save
    ]

    for input in input_q:
      test_tedit_parse(d, input, db, verbose)

    table = db.table_by_name("test_table")

    self.assertTrue(table.has_column("new_id", int, True))
    self.assertTrue(table.has_column("name", str, False))
    self.assertTrue(table.has_column("id", str, False))
    self.assertEqual(table.num_columns(), 3)

    self.assertEqual(table.search(new_id=13, name="kyle", id="roobiki").num_results, 1)
    self.assertEqual(table.search(new_id=14, name="dylan", id="pianta").num_results, 1)

if __name__ == "__main__":
  config.DEBUG_MODE = False
  unittest.main()
  #unittest.main(defaultTest="TestTEDIT.test_create_new_table_name_change")