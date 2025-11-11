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

    # make sure all the game tables exist
    self.assertTrue(db.table_exists(database.database.ALIAS_TABLE))
    self.assertTrue(db.table_exists(database.database.EXIT_TABLE))
    self.assertTrue(db.table_exists(database.database.PREF_NUMERIC_TABLE))
    self.assertTrue(db.table_exists(database.database.PREF_TEXT_TABLE))
    self.assertTrue(db.table_exists(database.database.PREF_FLAG_TABLE))
    self.assertTrue(db.table_exists(database.database.NPC_PROTO_TABLE))
    self.assertTrue(db.table_exists(database.database.OBJ_PROTO_TABLE))
    self.assertTrue(db.table_exists(database.database.WORLD_TABLE))
    self.assertTrue(db.table_exists(database.database.PLAYER_TABLE))
    self.assertTrue(db.table_exists(database.database.ZONE_TABLE))

    # but others don't
    self.assertFalse(db.table_exists("some_other_table"))

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
    self.assertTrue(alias_table.has_column("zone_id", str, True))
    self.assertTrue(alias_table.has_column("id", str, True))
    self.assertTrue(alias_table.has_column("type", str, True))
    self.assertTrue(alias_table.has_column("alias", str, True))
    self.assertEqual(alias_table.num_columns(), 4)

    # exit_table has correct columns
    self.assertTrue(ex_table.has_column("o_zone_id", str, True))
    self.assertTrue(ex_table.has_column("o_id", str, True))
    self.assertTrue(ex_table.has_column("direction", int, True))
    self.assertTrue(ex_table.has_column("d_zone_id", str, False))
    self.assertTrue(ex_table.has_column("d_id", str, False))
    self.assertEqual(ex_table.num_columns(), 5)

    # pref_numeric_table has correct columns
    self.assertTrue(pref_numeric_table.has_column("id", int, True))
    self.assertTrue(pref_numeric_table.has_column("field", str, True))
    self.assertTrue(pref_numeric_table.has_column("value", int, False))
    self.assertEqual(pref_numeric_table.num_columns(), 3)

    # pref_text_table has correct columns
    self.assertTrue(pref_text_table.has_column("id", int, True))
    self.assertTrue(pref_text_table.has_column("field", str, True))
    self.assertTrue(pref_text_table.has_column("value", str, False))
    self.assertEqual(pref_text_table.num_columns(), 3)

    # pref_flag_table has correct columns
    self.assertTrue(pref_flag_table.has_column("id", int, True))
    self.assertTrue(pref_flag_table.has_column("field", str, True))
    self.assertTrue(pref_flag_table.has_column("value", int, False))
    self.assertEqual(pref_flag_table.num_columns(), 3)

    # npc_proto_table has correct columns
    self.assertTrue(npc_proto_table.has_column("zone_id", str, True))
    self.assertTrue(npc_proto_table.has_column("id", str, True))
    self.assertTrue(npc_proto_table.has_column("name", str, False))
    self.assertTrue(npc_proto_table.has_column("desc", str, False))
    self.assertTrue(npc_proto_table.has_column("ldesc", str, False))
    self.assertEqual(npc_proto_table.num_columns(), 5)

    # obj_proto_table has correct columns
    self.assertTrue(obj_proto_table.has_column("zone_id", str, True))
    self.assertTrue(obj_proto_table.has_column("id", str, True))
    self.assertTrue(obj_proto_table.has_column("name", str, False))
    self.assertTrue(obj_proto_table.has_column("desc", str, False))
    self.assertTrue(obj_proto_table.has_column("ldesc", str, False))
    self.assertEqual(obj_proto_table.num_columns(), 5)

    # wld_table has correct columns
    self.assertTrue(wld_table.has_column("zone_id", str, True))
    self.assertTrue(wld_table.has_column("id", str, True))
    self.assertTrue(wld_table.has_column("name", str, False))
    self.assertTrue(wld_table.has_column("desc", str, False))
    self.assertEqual(wld_table.num_columns(), 4)

    # p_table has correct columns
    self.assertTrue(p_table.has_column("id", int, True))
    self.assertTrue(p_table.has_column("name", str, False))
    self.assertTrue(p_table.has_column("password", str, False))
    self.assertEqual(p_table.num_columns(), 3)

    # z_table has correct columns
    self.assertTrue(z_table.has_column("id", str, True))
    self.assertTrue(z_table.has_column("name", str, False))
    self.assertTrue(z_table.has_column("author", str, False))
    self.assertEqual(z_table.num_columns(), 3)

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