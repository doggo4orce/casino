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

class TestDatabase(unittest.TestCase):

  def test_create_tables(self):
    db = database.database(":memory:")
    db.connect()
    db.create_tables()

    p_table = db.admin_table_by_name(database.database.PLAYER_TABLE)

    print(p_table.debug())

  def test_aliases(self):
    pass

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