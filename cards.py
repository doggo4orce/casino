import collections
import enum
import pc
import random

class card_suit(enum.IntEnum):
  SPADE   = 0
  HEART   = 1
  CLUB    = 2
  DIAMOND = 3

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

class card:
  """Creates a a new card.
    suit = spades, hearts, etc.
    rank = seven, jack, king, etc.
    value = a number between 1-13, assigned depending on game"""
  def __init__(self, suit, rank, value):
    self._suit = suit
    self._rank = rank
    self._value = value

  @property
  def suit(self):
  	return self._suit
  
  @property
  def rank(self):
  	return self._rank

  @property
  def value(self):
    return self._value

  @suit.setter
  def suit(self, new_suit):
  	self._suit = new_suit

  @rank.setter
  def rank(self, new_rank):
  	self._rank = new_rank

  @value.setter
  def value(self, new_value):
    self._rank = new_value

  def __str__(self):
    return f"{card_rank(self.rank).name} of {card_suit(self.suit).name}"

class shoe:
  """Creates a new shoe (generalization of a deck), which consists of a double-ended
    queue of cards."""
  def __init__(self):
    self._contents = collections.deque()

  @property
  def size(self):
  	return len(self._contents)

  """peek_next_card()    <-- returns the top card without removing it it
     burn()              <-- discards the top card
     draw()              <-- removes and returns the top card
     add_top()           <-- adds a new card to the top of the shoe
     add_bottom()        <-- adds a new card to the bottom of the shoe
     shuffle()           <-- randomizes the order of cards in the shoe
     clear()             <-- empties the shoe
     absorb_top()        <-- add another shoe to the top of this one
     absorb_bottom()     <-- add another shoe to the bottom of this one
     pull_front_cards(n) <-- pulls the top n cards and returns it as a new shoe"""
  
  def peek_next_card(self):
    if self._contents:
      return self._contents[0]

  def burn(self):
    self.draw()

  def draw(self):
    if self._contents:
      return self._contents.popleft()

  def add_top(self, new_card):
    self._contents.appendleft(new_card)

  def add_bottom(self, new_card):
    self._contents.append(new_card)

  def shuffle(self):
    random.shuffle(self._contents)

  def clear(self):
    self._contents.clear()

  def absorb_top(self, other):
    self._contents, other._contents = other._contents, self._contents
    self.absorb_bottom(other)

  def absorb_bottom(self, other):
    self._contents.extend(other._contents)
    other.clear()

  def pull_front_cards(self, n):
    front = shoe()

    if n > self.size:
      return None

    for j in range(0, n):
      front.add_bottom(self.draw())

    return front

  def __str__(self):
    ret_val = f"Deck has {self.size} cards:\n"

    for card in self._contents:
      ret_val += str(card) + '\n'

    return ret_val

class card_dealer(pc.npc):
  def __init__(self):
    super().__init__()
    self._shoe = None
    self._paused = False

  @classmethod
  def from_npc(cls, old_npc):
    ret_val = cls()

    # copy character attributes
    ret_val.entity = old_npc.entity
    ret_val.inventory = old_npc.inventory

    # copy npc attributes
    ret_val.vnum = old_npc.vnum
    ret_val.specs = old_npc.specs
    
    return ret_val

  # Getters
  @property
  def shoe(self):
    return self._shoe
  @property
  def paused(self):
    return self._paused

  # Setters
  @shoe.setter
  def shoe(self, new_shoe):
    self._shoe = new_shoe
  @paused.setter
  def paused(self, is_paused):
    self._paused = is_paused

  def draw(self):
    if self.shoe:
      return self._shoe.draw()

  def burn(self):
    if self.shoe:
      self._shoe.burn()

  def shuffle(self):
    if self.shoe:
      self._shoe.shuffle()

if __name__ == '__main__':
  ch = pc.npc()
  dealer = card_dealer.from_npc(ch, None)

  print(dealer)

