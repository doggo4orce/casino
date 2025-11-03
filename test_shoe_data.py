import card_data
import shoe_data

import unittest

class TestShoeData(unittest.TestCase):
  def test_draw_add_top_and_bottom(self):
    shoe = shoe_data.shoe_data()

    # add three of spades on top
    card = card_data.card_data(card_data.card_suit.SPADES, card_data.card_rank.THREE)
    self.assertNotIn(card, shoe)
    shoe.add_top(card)
    self.assertIn(card, shoe)
    
    # add five of hearts on the top
    card = card_data.card_data(card_data.card_suit.HEARTS, card_data.card_rank.FIVE)
    self.assertNotIn(card, shoe)
    shoe.add_top(card)
    self.assertIn(card, shoe)

    # add ten of clubs on bottom
    card = card_data.card_data(card_data.card_suit.CLUBS, card_data.card_rank.TEN)
    self.assertNotIn(card, shoe)
    shoe.add_bottom(card)
    self.assertIn(card, shoe)

    # five of hearts is on top
    card = shoe.draw()
    self.assertNotIn(card, shoe)
    self.assertEqual(card.rank, card_data.card_rank.FIVE)
    self.assertEqual(card.suit, card_data.card_suit.HEARTS)

    # next should be three of spade
    card = shoe.draw()
    self.assertNotIn(card, shoe)
    self.assertEqual(card.rank, card_data.card_rank.THREE)
    self.assertEqual(card.suit, card_data.card_suit.SPADES)

    # finally the ten of clubs
    card = shoe.draw()
    self.assertNotIn(card, shoe)
    self.assertEqual(card.rank, card_data.card_rank.TEN)
    self.assertEqual(card.suit, card_data.card_suit.CLUBS)

    # should be no cards left
    print("There should be an error ...")
    card = shoe.draw()
    print("... between these lines.")

    self.assertIsNone(card)

    card = shoe.peek()
    self.assertIsNone(card)

  def test_iteration(self):
    shoe = shoe_data.shoe_data()

    card = card_data.card_data(card_data.card_suit.SPADES, card_data.card_rank.THREE)
    shoe.add_bottom(card)
    
    card = card_data.card_data(card_data.card_suit.HEARTS, card_data.card_rank.FIVE)
    shoe.add_bottom(card)

    card = card_data.card_data(card_data.card_suit.CLUBS, card_data.card_rank.TEN)
    shoe.add_bottom(card)

    print("-=-= Test Iteration -=-=-")
    print(shoe.debug())
    print("-=-=-==-=-=-=-=-=-=--=-=-")

  def test_peek(self):
    shoe = shoe_data.shoe_data()

    card = card_data.card_data(card_data.card_suit.SPADES, card_data.card_rank.THREE)
    shoe.add_bottom(card)

    card = card_data.card_data(card_data.card_suit.HEARTS, card_data.card_rank.FIVE)
    shoe.add_bottom(card)

    card = shoe.peek()
    self.assertEqual(card.suit, card_data.card_suit.SPADES)
    self.assertEqual(card.rank, card_data.card_rank.THREE)

    self.assertEqual(len(shoe), 2)

  def test_french_deck(self):
    shoe = shoe_data.shoe_data.french_deck(1)

    self.assertEqual(len(shoe), 52)

    print("-=-= Test French Deck -=-=-")
    print(shoe.debug())
    print("-=-=-==-=-=-=-=-=-=--=-=-")


  def test_burn(self):
    shoe = shoe_data.shoe_data.french_deck(1)

    self.assertEqual(len(shoe), 52)

    # burn the ace, 2, 3, 4, and 5 of spades
    for _ in range(0,5):
      shoe.burn()

    card = shoe.peek()
    self.assertEqual(card.suit, card_data.card_suit.SPADES)
    self.assertEqual(card.rank, card_data.card_rank.SIX)

  def test_shuffle(self):
    shoe = shoe_data.shoe_data.french_deck(1)
    shoe.shuffle()
    print("-=-= Test Shuffle -=-=-=-")
    print(shoe.debug())
    print("-=-=-==-=-=-=-=-=-=--=-=-")

  def test_clear(self):
    shoe = shoe_data.shoe_data.french_deck(1)
    shoe.clear()
    self.assertEqual(len(shoe), 0)

  def test_absorb_top(self):
    shoe1 = shoe_data.shoe_data.french_deck(1)
    shoe2 = shoe_data.shoe_data.french_deck(1)

    shoe2.shuffle()

    shoe2.absorb_top(shoe1)

    card1 = shoe2.peek()
    card2 = shoe2.peek()
    card3 = shoe2.peek()

    self.assertEqual(card1.suit, card_data.card_suit.SPADES)
    self.assertEqual(card1.rank, card_data.card_rank.ACE)

    self.assertEqual(card2.suit, card_data.card_suit.SPADES)
    self.assertEqual(card2.rank, card_data.card_rank.ACE)

    self.assertEqual(card3.suit, card_data.card_suit.SPADES)
    self.assertEqual(card3.rank, card_data.card_rank.ACE)

    self.assertEqual(len(shoe1), 0)
    self.assertEqual(len(shoe2), 104)

  def test_absorb_bottom(self):
    shoe1 = shoe_data.shoe_data.french_deck(1)
    shoe2 = shoe_data.shoe_data.french_deck(1)

    shoe2.shuffle()

    # add clean deck on bottom
    shoe2.absorb_bottom(shoe1)

    self.assertEqual(len(shoe1), 0)
    self.assertEqual(len(shoe2), 104)

    # remove shuffled half
    shoe1 = shoe2.pull_front_cards(52)

    self.assertEqual(len(shoe1), 52)
    self.assertEqual(len(shoe2), 52)

    # next three should be clean
    card1 = shoe2.peek()
    card2 = shoe2.peek()
    card3 = shoe2.peek()

    self.assertEqual(card1.suit, card_data.card_suit.SPADES)
    self.assertEqual(card1.rank, card_data.card_rank.ACE)

    self.assertEqual(card2.suit, card_data.card_suit.SPADES)
    self.assertEqual(card2.rank, card_data.card_rank.ACE)

    self.assertEqual(card3.suit, card_data.card_suit.SPADES)
    self.assertEqual(card3.rank, card_data.card_rank.ACE)



if __name__ == "__main__":
  unittest.main()