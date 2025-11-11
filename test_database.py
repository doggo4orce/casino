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
    self.assertTrue(db.admin_table_exists(database.database.ALIAS_TABLE))
    self.assertTrue(db.admin_table_exists(database.database.EXIT_TABLE))
    self.assertTrue(db.admin_table_exists(database.database.PREF_NUMERIC_TABLE))
    self.assertTrue(db.admin_table_exists(database.database.PREF_TEXT_TABLE))
    self.assertTrue(db.admin_table_exists(database.database.PREF_FLAG_TABLE))
    self.assertTrue(db.admin_table_exists(database.database.NPC_PROTO_TABLE))
    self.assertTrue(db.admin_table_exists(database.database.OBJ_PROTO_TABLE))
    self.assertTrue(db.admin_table_exists(database.database.WORLD_TABLE))
    self.assertTrue(db.admin_table_exists(database.database.PLAYER_TABLE))
    self.assertTrue(db.admin_table_exists(database.database.ZONE_TABLE))

    # but others don't
    self.assertFalse(db.admin_table_exists("some_other_table"))

    # load the tables as table objects
    alias_table = db.admin_table_by_name(database.database.ALIAS_TABLE)
    ex_table = db.admin_table_by_name(database.database.EXIT_TABLE)
    pref_numeric_table = db.admin_table_by_name(database.database.PREF_NUMERIC_TABLE)
    pref_text_table = db.admin_table_by_name(database.database.PREF_TEXT_TABLE)
    pref_flag_table = db.admin_table_by_name(database.database.PREF_FLAG_TABLE)
    npc_proto_table = db.admin_table_by_name(database.database.NPC_PROTO_TABLE)
    obj_proto_table = db.admin_table_by_name(database.database.OBJ_PROTO_TABLE)
    wld_table = db.admin_table_by_name(database.database.WORLD_TABLE)
    p_table = db.admin_table_by_name(database.database.PLAYER_TABLE)
    z_table = db.admin_table_by_name(database.database.ZONE_TABLE)

    for column in pref_flag_table.list_columns():
      print(str(column))

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

  def test_aliases(self):
    db = database.database(":memory:")
    db.connect()
    db.create_tables()

    db.save_alias(zone_id="castle_black", id="jon_snow", type="npc", alias="jon")
    db.save_alias(zone_id="castle_black", id="jon_snow", type="npc", alias="snow")
    db.save_alias(zone_id="castle_black", id="jon_snow", type="npc", alias="crow")

  def test_exits(self):
    pass

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