import baccarat_dealer_data
import baccarat_procs
import commands
import database
import game_data
import hbeat_proc_data
import npc_proto_data
import pc_data
import test_utilities
import unittest

class TestBaccaratProcs(unittest.TestCase):
  def test_baccarat_dealing(self):
    db = database.database(":memory:")

    db.connect()
    db.create_tables()
    db.load_stock()

    mud = game_data.game_data()
    mud.load_world(db)
    mud.startup()

    room = mud.room_by_uid('stockville', 'casino')

    dealer = room.people[0]

    print(dealer.debug())
    
    # put him in the room with player
    #mud.add_character_to_room(dealer, room)

    #print(dealer.debug())

if __name__ == "__main__":
  unittest.main()