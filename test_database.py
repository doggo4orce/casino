import database
import exit_data
import game_data
import pc_data
import namelist_data
import npc_proto_data
import obj_proto_data
import pref_data
import room_data
import text_data
import unittest
import zone_data

  # check this against database.schemas property
  #
  # ALIAS_TABLE        = "alias_table"
  # EXIT_TABLE         = "ex_table"
  # PREF_NUMERIC_TABLE = "pref_table_numeric"
  # PREF_TEXT_TABLE    = "pref_table_text"
  # PREF_FLAG_TABLE    = "pref_table_flags"
  # NPC_PROTO_TABLE    = "npc_proto_table"
  # OBJ_PROTO_TABLE    = "obj_proto_table"
  # WORLD_TABLE        = "wld_table"
  # PLAYER_TABLE       = "p_table"
  # ZONE_TABLE         = "z_table"

class TestDatabase(unittest.TestCase):

  def test_create_tables(self):
    db = database.database(":memory:")
    db.connect()
    db.create_tables()

    # these are the tables our schema defines
    tables_in_schema = [
      database.database.ALIAS_TABLE,
      database.database.EXIT_TABLE,
      database.database.PREF_NUMERIC_TABLE,
      database.database.PREF_TEXT_TABLE,
      database.database.PREF_FLAG_TABLE,
      database.database.NPC_PROTO_TABLE,
      database.database.OBJ_PROTO_TABLE,
      database.database.WORLD_TABLE,
      database.database.PLAYER_TABLE,
      database.database.ZONE_TABLE
    ]

    # make sure all these exist
    for name in tables_in_schema:
      self.assertTrue(db.table_exists(name))

    # and no others
    self.assertEqual(db.num_tables(), len(tables_in_schema))

    # load the tables as table objects
    alias_table = db.table_by_name(database.database.ALIAS_TABLE)
    ex_table = db.table_by_name(database.database.EXIT_TABLE)
    pref_numeric_table = db.table_by_name(database.database.PREF_NUMERIC_TABLE)
    pref_text_table = db.table_by_name(database.database.PREF_TEXT_TABLE)
    pref_flag_table = db.table_by_name(database.database.PREF_FLAG_TABLE)
    npc_proto_table = db.table_by_name(database.database.NPC_PROTO_TABLE)
    obj_proto_table = db.table_by_name(database.database.OBJ_PROTO_TABLE)
    wld_table = db.table_by_name(database.database.WORLD_TABLE)
    p_table = db.table_by_name(database.database.PLAYER_TABLE)
    z_table = db.table_by_name(database.database.ZONE_TABLE)

    # alias_table has correct columns
    for tuple in db.schemas[database.database.ALIAS_TABLE]:
      self.assertTrue(alias_table.has_column(tuple[0], tuple[1], tuple[2]))

    self.assertEqual(alias_table.num_columns(), len(db.schemas[database.database.ALIAS_TABLE]))

    # exit_table has correct columns
    for tuple in db.schemas[database.database.EXIT_TABLE]:
      self.assertTrue(ex_table.has_column(tuple[0], tuple[1], tuple[2]))

    self.assertEqual(ex_table.num_columns(), len(db.schemas[database.database.EXIT_TABLE]))

    # pref_numeric_table has correct columns
    for tuple in db.schemas[database.database.PREF_NUMERIC_TABLE]:
      self.assertTrue(pref_numeric_table.has_column(tuple[0], tuple[1], tuple[2]))

    self.assertEqual(pref_numeric_table.num_columns(), len(db.schemas[database.database.PREF_NUMERIC_TABLE]))

    # pref_text_table has correct columns
    for tuple in db.schemas[database.database.PREF_TEXT_TABLE]:
      self.assertTrue(pref_text_table.has_column(tuple[0], tuple[1], tuple[2]))

    self.assertEqual(pref_text_table.num_columns(), len(db.schemas[database.database.PREF_TEXT_TABLE]))

    # pref_flag_table has correct columns
    for tuple in db.schemas[database.database.PREF_FLAG_TABLE]:
      self.assertTrue(pref_flag_table.has_column(tuple[0], tuple[1], tuple[2]))

    self.assertEqual(pref_flag_table.num_columns(), len(db.schemas[database.database.PREF_FLAG_TABLE]))

    # npc_proto_table has correct columns
    for tuple in db.schemas[database.database.NPC_PROTO_TABLE]:
      self.assertTrue(npc_proto_table.has_column(tuple[0], tuple[1], tuple[2]))

    self.assertEqual(npc_proto_table.num_columns(), len(db.schemas[database.database.NPC_PROTO_TABLE]))

    # obj_proto_table has correct columns
    for tuple in db.schemas[database.database.OBJ_PROTO_TABLE]:
      self.assertTrue(obj_proto_table.has_column(tuple[0], tuple[1], tuple[2]))

    self.assertEqual(obj_proto_table.num_columns(), len(db.schemas[database.database.OBJ_PROTO_TABLE]))

    # wld_table has correct columns
    for tuple in db.schemas[database.database.WORLD_TABLE]:
      self.assertTrue(wld_table.has_column(tuple[0], tuple[1], tuple[2]))

    self.assertEqual(wld_table.num_columns(), len(db.schemas[database.database.WORLD_TABLE]))

    # p_table has correct columns
    for tuple in db.schemas[database.database.PLAYER_TABLE]:
      self.assertTrue(p_table.has_column(tuple[0], tuple[1], tuple[2]))

    self.assertEqual(p_table.num_columns(), len(db.schemas[database.database.PLAYER_TABLE]))

    # z_table has correct columns
    for tuple in db.schemas[database.database.ZONE_TABLE]:
      self.assertTrue(z_table.has_column(tuple[0], tuple[1], tuple[2]))

    self.assertEqual(z_table.num_columns(), len(db.schemas[database.database.ZONE_TABLE]))

    # we just verified them manually, now check that the the verify_tables function works
    self.assertTrue(db.verify_tables())

    # drop a table so it doesn't work
    db.drop_table(database.database.NPC_PROTO_TABLE)

    # now verify should fail
    self.assertFalse(db.verify_tables())

    # teardown
    db.close()

  def test_aliases(self):
    # setup
    db = database.database(":memory:")
    db.connect()
    db.create_tables()

    # add a few aliases
    db.save_alias("castle_black", "jon_snow", "npc", "jon")
    db.save_alias("winterfell", "eddard_stark", "npc", "ned")
    db.save_alias("kings_landing", "the_hound", "npc", "hound")
    db.save_alias("sapphire_isles", "brienne_of_fucking_tarth", "npc", "brienne")
    db.save_alias("winterfell", "two_handed_sword", "obj", "ice")

    alias_table = db.table_by_name(database.database.ALIAS_TABLE)

    # test to make sure one is there
    self.assertTrue(db.has_alias("castle_black", "jon_snow", "npc", "jon")) # assertion failing

    # make sure table count is correct
    self.assertEqual(db.table_by_name(database.database.ALIAS_TABLE).num_records(), 5)

    # delete jon snow alias
    db.delete_alias("castle_black", "jon_snow", "npc", "jon")

    # make sure it's not there
    self.assertFalse(db.has_alias("castle_black", "jon_snow", "npc", "jon"))

    # only one remains
    self.assertEqual(db.table_by_name(database.database.ALIAS_TABLE).num_records(), 4)

    # teardown
    db.close()

  def test_exits(self):
    db = database.database(":memory:")
    db.connect()
    db.create_tables()

    # add a few exits
    db.save_exit("stockville", "recall", exit_data.exit_data(exit_data.direction.NORTH, "castle_black", "ice_wall01"))
    db.save_exit("castle_black", "ice_wall01", exit_data.exit_data(exit_data.direction.SOUTH, "stockville", "recall"))
    db.save_exit("stockville", "recall", exit_data.exit_data(exit_data.direction.EAST, "stockville", "casino"))
    db.save_exit("stockville", "casino", exit_data.exit_data(exit_data.direction.WEST, "stockville", "recall"))

    # test to make sure one is there
    self.assertTrue(db.has_exit("stockville", "recall", exit_data.direction.NORTH))

    # make sure table count is correct
    self.assertEqual(db.table_by_name(database.database.EXIT_TABLE).num_records(), 4)

    # delete the castle black ones
    db.delete_exit("stockville", "recall", exit_data.direction.NORTH)
    db.delete_exit("castle_black", "ice_wall01", exit_data.direction.SOUTH)

    # make sure they aren't there
    self.assertFalse(db.has_exit("stockville", "recall", exit_data.direction.NORTH))
    self.assertFalse(db.has_exit("castle_black", "ice_wall01", exit_data.direction.SOUTH))

    # only two left
    self.assertEqual(db.table_by_name(database.database.EXIT_TABLE).num_records(), 2)

  def test_numeric_preferences(self):
    pass

  def test_text_preferences(self):
    pass

  def test_flag_preferences(self):
    pass

  def test_npc_proto(self):
    pass

  def test_obj_proto(self):
    pass

  def test_room(self):
    pass

  def test_players(self):
    pass

  def test_zones(self):
    pass

  def test_load_world(self):
    pass

  def test_load_stock(self):
    pass

if __name__ == "__main__":
  unittest.main()