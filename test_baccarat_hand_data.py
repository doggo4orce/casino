import baccarat_hand_data
import card_data

import unittest

class TestBaccaratHandData(unittest.TestCase):
  def test_baccarat_hand(self):
    hand = baccarat_hand_data.baccarat_hand_data()

    card = card_data.card_data(card_data.card_suit.SPADES, card_data.card_rank.TEN)
    hand.add_card(card, 'player')
    card = card_data.card_data(card_data.card_suit.HEARTS, card_data.card_rank.THREE)
    hand.add_card(card, 'banker')
    card = card_data.card_data(card_data.card_suit.HEARTS, card_data.card_rank.FOUR)
    hand.add_card(card, 'player')
    card = card_data.card_data(card_data.card_suit.HEARTS, card_data.card_rank.NINE)
    hand.add_card(card, 'banker')

    self.assertEqual(hand.player_score(), 4)
    self.assertEqual(hand.banker_score(), 2)
    self.assertFalse(hand.panda())
    self.assertFalse(hand.dragon())

  def test_panda(self):
    hand = baccarat_hand_data.baccarat_hand_data()

    card = card_data.card_data(card_data.card_suit.SPADES, card_data.card_rank.TWO)
    hand.add_card(card, 'player')
    card = card_data.card_data(card_data.card_suit.HEARTS, card_data.card_rank.TWO)
    hand.add_card(card, 'banker')
    card = card_data.card_data(card_data.card_suit.HEARTS, card_data.card_rank.FIVE)
    hand.add_card(card, 'player')
    card = card_data.card_data(card_data.card_suit.HEARTS, card_data.card_rank.FIVE)
    hand.add_card(card, 'banker')
    card = card_data.card_data(card_data.card_suit.SPADES, card_data.card_rank.ACE)
    hand.add_card(card, 'player')

    self.assertTrue(hand.panda())

  def test_dragon(self):
    hand = baccarat_hand_data.baccarat_hand_data()

    card = card_data.card_data(card_data.card_suit.SPADES, card_data.card_rank.TWO)
    hand.add_card(card, 'player')
    card = card_data.card_data(card_data.card_suit.HEARTS, card_data.card_rank.TWO)
    hand.add_card(card, 'banker')
    card = card_data.card_data(card_data.card_suit.HEARTS, card_data.card_rank.TEN)
    hand.add_card(card, 'player')
    card = card_data.card_data(card_data.card_suit.HEARTS, card_data.card_rank.THREE)
    hand.add_card(card, 'banker')
    card = card_data.card_data(card_data.card_suit.SPADES, card_data.card_rank.ACE)
    hand.add_card(card, 'player')
    card = card_data.card_data(card_data.card_suit.HEARTS, card_data.card_rank.TWO)
    hand.add_card(card, 'banker')

    print(hand.display2())
    self.assertTrue(hand.dragon())

  def test_card_value(self):
    hand = baccarat_hand_data.baccarat_hand_data()
    card = card_data.card_data(card_data.card_suit.SPADES, card_data.card_rank.THREE)
    hand.add_card(card, 'player')
    card = card_data.card_data(card_data.card_suit.CLUBS, card_data.card_rank.TWO)
    hand.add_card(card, 'banker')

    self.assertEqual(hand.player_score(), 3)
    self.assertEqual(hand.banker_score(), 2)

    card = card_data.card_data(card_data.card_suit.HEARTS, card_data.card_rank.FIVE)
    hand.add_card(card, 'player')
    card = card_data.card_data(card_data.card_suit.DIAMONDS, card_data.card_rank.JACK)
    hand.add_card(card, 'banker')

    self.assertEqual(hand.player_score(), 8)
    self.assertEqual(hand.banker_score(), 2)

    card = card_data.card_data(card_data.card_suit.SPADES, card_data.card_rank.TWO)
    hand.add_card(card, 'player')
    card = card_data.card_data(card_data.card_suit.SPADES, card_data.card_rank.NINE)
    hand.add_card(card, 'banker')

    self.assertEqual(hand.player_score(), 0)
    self.assertEqual(hand.banker_score(), 1)
    print(hand.display())

if __name__ == "__main__":
    unittest.main()