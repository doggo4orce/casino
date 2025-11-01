import baccarat_dealer_data
import card_data
import card_dealer_data
import npc_data
import unittest

class TestBaccaratDealerData(unittest.TestCase):
  def test_baccarat_dealer(self):
    b_dealer = baccarat_dealer_data.baccarat_dealer_data()
    b_dealer.id = 'baccarat_dealer'
    b_dealer.zone_id = 'casino'
    b_dealer.name = 'baccarat dealer'
    b_dealer.remove_all_aliases()
    b_dealer.add_alias('card')
    b_dealer.add_alias('dealer')
    b_dealer.ldesc = 'a card dealer stands here'
    b_dealer.desc = 'He wants to take your money.'

  def test_create_froms(self):
    dealer = card_dealer_data.card_dealer_data()
    dealer.id = 'card_dealer'
    dealer.zone_id = 'casino'
    dealer.name = 'baccarat dealer'
    dealer.remove_all_aliases()
    dealer.add_alias('card')
    dealer.add_alias('dealer')
    dealer.ldesc = 'a card dealer stands here'
    dealer.desc = 'He wants to take your money.'

    b_dealer = baccarat_dealer_data.baccarat_dealer_data.from_card_dealer(dealer)

    # print(b_dealer.debug())

  def test_new_hand_deal(self):
    b_dealer = baccarat_dealer_data.baccarat_dealer_data()
    b_dealer.id = 'baccarat_dealer'
    b_dealer.zone_id = 'casino'
    b_dealer.name = 'baccarat dealer'
    b_dealer.remove_all_aliases()
    b_dealer.add_alias('card')
    b_dealer.add_alias('dealer')
    b_dealer.ldesc = 'a card dealer stands here'
    b_dealer.desc = 'He wants to take your money.'

    b_dealer.clear_baccarat_hand()
    b_dealer.give_french_decks(1)
    b_dealer.shuffle()

    b_dealer.deal(b_dealer.draw(), 'player')
    b_dealer.deal(b_dealer.draw(), 'player')
    b_dealer.deal(b_dealer.draw(), 'player')
    b_dealer.deal(b_dealer.draw(), 'banker')
    b_dealer.deal(b_dealer.draw(), 'banker')
    b_dealer.deal(b_dealer.draw(), 'banker')

    print(b_dealer.debug())

  def test_add_card_check_scores_naturals(self):
    b_dealer = baccarat_dealer_data.baccarat_dealer_data()

    b_dealer.clear_baccarat_hand()
    card = card_data.card_data(card_data.card_suit.SPADES, card_data.card_rank.FIVE)
    b_dealer.deal(card, 'player')
    card = card_data.card_data(card_data.card_suit.HEARTS, card_data.card_rank.THREE)
    b_dealer.deal(card, 'player')
    card = card_data.card_data(card_data.card_suit.DIAMONDS, card_data.card_rank.NINE)
    b_dealer.deal(card, 'banker')
    card = card_data.card_data(card_data.card_suit.CLUBS, card_data.card_rank.TEN)
    b_dealer.deal(card, 'banker')

    self.assertEqual(b_dealer.player_score(), 8)
    self.assertEqual(b_dealer.banker_score(), 9)
    self.assertTrue(b_dealer.player_natural())
    self.assertTrue(b_dealer.banker_natural())

    b_dealer.clear_baccarat_hand()
    card = card_data.card_data(card_data.card_suit.SPADES, card_data.card_rank.FIVE)
    b_dealer.deal(card, 'player')
    card = card_data.card_data(card_data.card_suit.HEARTS, card_data.card_rank.FOUR)
    b_dealer.deal(card, 'player')
    card = card_data.card_data(card_data.card_suit.DIAMONDS, card_data.card_rank.FOUR)
    b_dealer.deal(card, 'banker')
    card = card_data.card_data(card_data.card_suit.CLUBS, card_data.card_rank.FOUR)
    b_dealer.deal(card, 'banker')

    self.assertEqual(b_dealer.player_score(), 9)
    self.assertEqual(b_dealer.banker_score(), 8)
    self.assertTrue(b_dealer.player_natural())
    self.assertTrue(b_dealer.banker_natural())

    b_dealer.clear_baccarat_hand()
    card = card_data.card_data(card_data.card_suit.SPADES, card_data.card_rank.FIVE)
    b_dealer.deal(card, 'player')
    card = card_data.card_data(card_data.card_suit.HEARTS, card_data.card_rank.FIVE)
    b_dealer.deal(card, 'player')
    card = card_data.card_data(card_data.card_suit.DIAMONDS, card_data.card_rank.THREE)
    b_dealer.deal(card, 'banker')
    card = card_data.card_data(card_data.card_suit.CLUBS, card_data.card_rank.TEN)
    b_dealer.deal(card, 'banker')

    self.assertEqual(b_dealer.player_score(), 0)
    self.assertEqual(b_dealer.banker_score(), 3)
    self.assertFalse(b_dealer.player_natural())
    self.assertFalse(b_dealer.banker_natural())

if __name__ == "__main__":
  unittest.main()