import baccarat_dealer_data
import baccarat_procs
import commands
import config
import database
import descriptor_data
import exit_data
import game_data
import hbeat_proc_data
import nanny
import npc_proto_data
import pc_data
import test_utilities
import unittest

class TestBaccaratProcs(unittest.TestCase):
  def test_baccarat_walking_past_baccarat_dealer(self):
    # set up database
    db = database.database(":memory:")
    db.connect()
    db.create_tables()
    db.load_stock()

    # load copy of stock world
    mud = game_data.game_data()
    mud.load_world(db)
    mud.startup()

    # go to the casino
    room = mud.room_by_uid('stockville', 'casino')

    # where the dealer is only npc in room
    dealer = room.people[0]
    
    # put a player in room with him
    player = pc_data.pc_data()

    mud.add_character_to_room(player, room)

    # have player leave west
    commands.do_move(player, None, exit_data.direction.WEST, None, mud, db)

    # have player return from the west
    commands.do_move(player, None, exit_data.direction.EAST, None, mud, db)

  def test_baccarat_dealing(self):
    config.DEBUG_MODE = True

    # set up database
    db = database.database(":memory:")
    db.connect()
    db.create_tables()
    db.load_stock()

    # load copy of stock world
    mud = game_data.game_data()
    mud.load_world(db)
    mud.startup()

    # go to the casino
    room = mud.room_by_uid('stockville', 'casino')

    # where the dealer is only npc in room
    dealer = room.people[0]
    
    # put a player in room with him
    descriptor = descriptor_data.descriptor_data(None, "localhost")
    player = pc_data.pc_data()
    player.descriptor, descriptor.character = descriptor, player
    mud.add_character_to_room(player, room)

    self.assertEqual(dealer.bac_state, baccarat_dealer_data.baccarat_dealer_state.IDLE)

    baccarat_procs.baccarat_dealing(mud, dealer, db)

    # proc has no effect on idle dealer
    self.assertEqual(dealer.bac_state, baccarat_dealer_data.baccarat_dealer_state.IDLE)

    # tell the dealer to start a round
    nanny.interpret_msg(player.descriptor, "baccarat", "simulate", None, mud, db)

    # dealer should be ready to start a shoe
    self.assertEqual(dealer.bac_state, baccarat_dealer_data.baccarat_dealer_state.BEGIN_SHOE)

    for j in range(0,13):
      baccarat_procs.baccarat_dealing(mud, dealer, db)

    print(dealer.debug())
    # self.assertEqual(dealer.bac_state, baccarat_dealer_data.baccarat_dealer_state.SHUFFLE_SHOE)


if __name__ == "__main__":
  unittest.main()