from color import *
import enum

class card_suit(enum.IntEnum):
  SPADES   = 0
  HEARTS   = 1
  CLUBS    = 2
  DIAMONDS = 3

class card_rank(enum.IntEnum):
  ACE   = 1
  TWO   = 2
  THREE = 3
  FOUR  = 4
  FIVE  = 5
  SIX   = 6
  SEVEN = 7
  EIGHT = 8
  NINE  = 9
  TEN   = 10
  JACK  = 11
  QUEEN = 12
  KING  = 13

class card_data:
  """Creates a a new card.
     suit = spades, hearts, etc.
     rank = seven, jack, king, etc"""
  def __init__(self, suit, rank):
    self._suit = suit
    self._rank = rank

  @property
  def suit(self):
  	return self._suit
  @property
  def rank(self):
  	return self._rank

  @suit.setter
  def suit(self, new_suit):
  	self._suit = new_suit
  @rank.setter
  def rank(self, new_rank):
  	self._rank = new_rank

  """card_color()         <-- returns the designated colour code for black/red cards
     card_rank_abbrev()   <-- returns 10 for ten, Q for queen, etc.
     card_suit_abbrev_5() <-- returns SPADE for spades, DIAMD for diamonds, etc.
     ascii_rep()          <-- returns a list of 5 7-char strings to draw the card"""

  def card_color(self):
    if self.suit in {card_suit.SPADES, card_suit.CLUBS}:
      return DARK_GRAY
    else:
      return RED

  def card_rank_abbrev(self):
    if self.rank in {2,3,4,5,6,7,8,9}:
      return str(int(self.rank))
    elif self.rank == 10:
      return '10'
    else:
      return self.rank.name[0] # J, Q, or K

  def card_suit_abbrev_5(self):
    if self.suit == card_suit.SPADES:
      return "SPADE"
    if self.suit == card_suit.CLUBS:
      return "CLUBS"
    if self.suit == card_suit.HEARTS:
      return "HEART"
    if self.suit == card_suit.DIAMONDS:
      return "DIAMD"

  def ascii_rep(self):
    return [
      "+-----+",
      "|{}   |".format(self.card_color() + self.card_rank_abbrev().ljust(2) + NORMAL),
      "|{}|".format(self.card_color() + self.card_suit_abbrev_5() + NORMAL),
      "|   {}|".format(self.card_color() + self.card_rank_abbrev().rjust(2) + NORMAL),
      "+-----+"]

  def debug(self):
    ret_val = f"Suit: {CYAN}{self.card_suit_abbrev_5()}{NORMAL}\r\n"
    ret_val += f"Rank: {CYAN}{self.card_rank_abbrev()}{NORMAL}"
    return ret_val

  def __str__(self):
    return card_rank(self.rank).name.lower() + " of " + card_suit(self.suit).name.lower()