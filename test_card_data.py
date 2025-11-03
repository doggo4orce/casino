import card_data
import unittest

class TestCardData(unittest.TestCase):
  def test_card_data(self):
    card = card_data.card_data(card_data.card_suit.SPADES, card_data.card_rank.NINE)

    self.assertEqual(card.suit, card_data.card_suit.SPADES)
    self.assertEqual(card.rank, card_data.card_rank.NINE)
    self.assertEqual(card.card_rank_abbrev(), '9')
    self.assertEqual(card.card_suit_abbrev_5(), 'SPADE')

    card.suit = card_data.card_suit.CLUBS
    card.rank = card_data.card_rank.TWO

    self.assertEqual(card.suit, card_data.card_suit.CLUBS)
    self.assertEqual(card.rank, card_data.card_rank.TWO)
    self.assertEqual(card.card_rank_abbrev(), '2')
    self.assertEqual(card.card_suit_abbrev_5(), 'CLUBS')

    for line in card.ascii_rep():
      print(line)

    print(card.debug())

if __name__ == "__main__":
  unittest.main()