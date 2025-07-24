import card_data
import card_dealer_data
import npc_proto_data
import npc_data
import unittest

class TestCardDealerData(unittest.TestCase):
  def test_pausing(self):
    npc_p = npc_proto_data.npc_proto_data()
    npc_p.id = 'card_dealer'
    npc_p.zone_id = 'casino'
    npc_p.name = 'blackjack dealer'
    npc_p.remove_all_aliases()
    npc_p.add_alias('card')
    npc_p.add_alias('dealer')
    npc_p.ldesc = 'a card dealer stands here'
    npc_p.desc = 'He wants to take your money.'

    npc = npc_data.npc_data(npc_p)

    dealer = card_dealer_data.card_dealer_data.from_npc(npc)

    print(dealer.debug())

  def test_burn_draw_peek(self):
    npc_p = npc_proto_data.npc_proto_data()
    npc_p.id = 'card_dealer'
    npc_p.zone_id = 'casino'
    npc_p.name = 'blackjack dealer'
    npc_p.remove_all_aliases()
    npc_p.add_alias('card')
    npc_p.add_alias('dealer')
    npc_p.ldesc = 'a card dealer stands here'
    npc_p.desc = 'He wants to take your money.'

    npc = npc_data.npc_data(npc_p)

    dealer = card_dealer_data.card_dealer_data.from_npc(npc)

    dealer.give_french_decks()

    self.assertEqual(dealer.shoe_length(), 52)

    dealer.clear_shoe()
    dealer.give_french_decks(2)

    self.assertEqual(dealer.shoe_length(), 104)

    # expecting A, 2, 3, of diamonds
    card = dealer.draw()
    self.assertEqual(card.suit, card_data.card_suit.SPADES)
    self.assertEqual(card.rank, card_data.card_rank.ACE)
    card = dealer.draw()
    self.assertEqual(card.suit, card_data.card_suit.SPADES)
    self.assertEqual(card.rank, card_data.card_rank.TWO)
    card = dealer.draw()
    self.assertEqual(card.suit, card_data.card_suit.SPADES)
    self.assertEqual(card.rank, card_data.card_rank.THREE)

    # burn the next 48
    dealer.burn_cards(48)

    # expecting last card of deck, king of diamonds
    card = dealer.draw()
    self.assertEqual(card.suit, card_data.card_suit.DIAMONDS)
    self.assertEqual(card.rank, card_data.card_rank.KING)

    # expecting A, 2, 3 of diamonds
    card = dealer.draw()
    self.assertEqual(card.suit, card_data.card_suit.SPADES)
    self.assertEqual(card.rank, card_data.card_rank.ACE)
    card = dealer.draw()
    self.assertEqual(card.suit, card_data.card_suit.SPADES)
    self.assertEqual(card.rank, card_data.card_rank.TWO)
    card = dealer.draw()
    self.assertEqual(card.suit, card_data.card_suit.SPADES)
    self.assertEqual(card.rank, card_data.card_rank.THREE)

    #burn the next 30
    dealer.burn_cards(36)
    
    card = dealer.peek()
    self.assertEqual(card.suit, card_data.card_suit.DIAMONDS)
    self.assertEqual(card.rank, card_data.card_rank.ACE)

    # expecting A, 2, 3 of diamonds
    card = dealer.draw()
    self.assertEqual(card.suit, card_data.card_suit.DIAMONDS)
    self.assertEqual(card.rank, card_data.card_rank.ACE)
    card = dealer.draw()
    self.assertEqual(card.suit, card_data.card_suit.DIAMONDS)
    self.assertEqual(card.rank, card_data.card_rank.TWO)
    card = dealer.draw()
    self.assertEqual(card.suit, card_data.card_suit.DIAMONDS)
    self.assertEqual(card.rank, card_data.card_rank.THREE)


if __name__ == "__main__":
  unittest.main()