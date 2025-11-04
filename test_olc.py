import config
import database
import game_data
import olc
import pc_data
import unittest
import unique_id_data

class TestOLC(unittest.TestCase):
  def test_redit(self):
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

    # try redit command
    olc.do_redit(player, None, "", None, mud, db)

if __name__ == "__main__":
  unittest.main()