import card_data
import collections
from color import *
import mudlog
import random

class shoe_data:
  """Creates a new shoe (may be thought of as a deck but is more general)
     contents = a double-ended queue containing the cards in the shoe"""
  def __init__(self):
    self._contents = collections.deque()

  """french_deck(num_decks) <- returns a shoe with 52 card decks
     peek()                 <- returns top card without removing
     burn()                 <- remove top card without returning
     draw()                 <- remove and return top card
     add_top()              <- add new card to top of shoe
     add_bottom()           <- add new card to bottom of shoe
     shuffle()              <- randomize order of cards in the shoe
     clear()                <- empty the shoe
     absorb_top(shoe)       <- empty shoe into top of this one
     absorb_bottom(shoe)    <- empty shoe into bottom of this one
     pull_front_cards(n)    <- pulls the top n cards and returns it as a new shoe"""
  
  @classmethod
  def french_deck(cls, num_decks):
    deck = cls()
    for k in range(0, num_decks):
      for suit in card_data.card_suit:
        for rank in card_data.card_rank:
          deck.add_bottom(card_data.card_data(suit, rank))
    return deck

  def peek(self):
    if self._contents:
      return self._contents[0]

  def burn(self):
    if self._contents:
      self.draw()
    else:
      mudlog.error("Trying to burn card from empty shoe.")

  def draw(self):
    if self._contents:
      return self._contents.popleft()
    else:
      mudlog.error("Trying to draw card from empty shoe.")

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
    front = shoe_data()
    if n > len(self):
      return None
    for j in range(0, n):
      front.add_bottom(self.draw())
    return front

  def debug(self):
    ret_val = f"Num Cards: {CYAN}{len(self)}{NORMAL}\n"

    for card in self._contents:
      ret_val += f"{CYAN}{str(card)}{NORMAL}\r\n"

    return ret_val[:-1]

  def __getitem__(self, key):
    return self._contents[key]

  def __contains__(self, card):
    return card in self._contents
    
  def __iter__(self):
    return shoe_data_iterator(self)

  def __len__(self):
    return len(self._contents)

class shoe_data_iterator:
  def __init__(self, shoe):
    self._shoe = shoe
    self._index = 0

  def __next__(self):
    if self._index < len(self._shoe):
      result = self._shoe[self._index]
      self._index += 1
      return result
    raise StopIteration
  