import baccarat_dealer
import baccarat_table
import cards
import pc
import object
import structs
import table
import unittest

class TestTable(unittest.TestCase):
  def create_object(self):
    op = structs.obj_proto_data()
    op.entity.name = "test table"
    op.entity.namelist = ["test", "table"]
    op.entity.desc = "<p>This is a table made for unit testing.</p>"
    op.entity.room = None
    op.ldesc = "A test table is here, waiting to be tested."
    op.unique_id.zone_id = 'unit_test'
    op.unique_id.id = 'test_table'
    return object.object(op)

  def create_table(self, num_seats):
    tab = self.create_object()
    tab = table.table.from_obj(tab, num_seats)
    return tab

  def create_baccarat_table(self):
    b_table = self.create_table(3)
    b_table = baccarat_table.baccarat_table.from_table(b_table)
    return b_table

  def create_npc(self):
    np = structs.npc_proto_data()
    np.entity.name = "test mob"
    np.entity.namelist = ["test", "mob"]
    np.entity.desc = "<p>This is a dealer made for unit testing</p>"
    np.entity.room = None
    np.ldesc = "A test dealer is here, waiting to be tested."
    np.unique_id.zone_id = 'unit_test'
    np.unique_id.id = 'test_table'
    return pc.npc(np)

  def create_dealer(self):
    dealer = self.create_npc()
    dealer = cards.card_dealer.from_npc(dealer)
    return dealer

  def create_baccarat_dealer(self):
    b_dealer = self.create_dealer()
    b_dealer = baccarat_dealer.baccarat_dealer.from_card_dealer(b_dealer)
    return b_dealer

  def create_baccarat_hand(self, num_cards):
    hand = baccarat_dealer.baccarat_hand()

    if num_cards > 6:
      num_cards = 6
    if num_cards < 0:
      num_cards = 0

    if num_cards >= 1:
      hand.add_card(cards.card(cards.card_suit.SPADES, cards.card_rank.ACE), "player")
    if num_cards >= 2:
      hand.add_card(cards.card(cards.card_suit.CLUBS, cards.card_rank.ACE), "banker")
    if num_cards >= 3:
      hand.add_card(cards.card(cards.card_suit.DIAMONDS, cards.card_rank.ACE), "player")
    if num_cards >= 4:
      hand.add_card(cards.card(cards.card_suit.HEARTS, cards.card_rank.ACE), "banker")
    if num_cards >= 5:
      hand.add_card(cards.card(cards.card_suit.SPADES, cards.card_rank.TWO), "player")
    if num_cards == 6:
      hand.add_card(cards.card(cards.card_suit.CLUBS, cards.card_rank.TWO), "banker")
    return hand

  def test_table(self):
    obj = self.create_object()
    tab = table.table.from_obj(obj, 4)

    self.assertEqual(tab.num_guests, 0)
    
    tab.add_guest("arthur")
    tab.add_guest("lancelot")
    self.assertTrue(tab.is_seated("arthur"))
    self.assertTrue(tab.is_seated("lancelot"))
    self.assertEqual(tab.num_guests, 2)
    
    tab.remove_guest("lancelot")
    self.assertFalse(tab.is_seated("lancelot"))
    self.assertEqual(tab.num_guests, 1)

  def test_baccarat_table(self):
    b_table = self.create_baccarat_table()
    b_table.dealer = self.create_baccarat_dealer()
    b_table.dealer.hand = self.create_baccarat_hand(6)

    print(b_table.render())
