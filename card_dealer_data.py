from color import *
import copy
import mudlog
import npc_data
import shoe_data

class card_dealer_data(npc_data.npc_data):
  def __init__(self):
    """shoe   = reference to the current shoe in progress if the dealer is working
       paused = a pause timer which may be set to"""
    super().__init__()
    self._shoe = shoe_data.shoe_data()
    self._paused = False # TODO: remove this? and associated functions?

  """from_npc(npc)          <- promote npc to card_dealer
     give_french_decks(n=1) <- start over with new shoe 
     shoe_empty()           <- check if shoe is empty
     shoe_length()          <- count cards in shoe
     pause()                <- set paused flag to true
     resume()               <- set paused flag to false
     paused()               <- check paused flag
     peek()                 <- returns top card without removing
     burn_cards(n)          <- burn n cards from my shoe
     draw()                 <- remove and return top card from my shoe
     add_top(shoe)          <- add new card to top of my shoe
     add_bottom(shoe)       <- add new card to bottom of my shoe
     shuffle()              <- shuffle my shoe
     clear_shoe()           <- empty my shoe
     absorb_top(shoe)       <- put shoe on top of my shoe
     absorb_bottom(shoe)    <- put shoe on bottom of my shoe
     pull_front_cards(n)    <- pull top n cards from my shoe"""

  @classmethod
  def from_npc(cls, npc):
    ret_val = cls()
    super().copy_from(ret_val, npc)
    return ret_val

  def copy_from(self, dealer):
    npc_data.npc_data.copy_from(self, dealer)
    self._shoe = copy.deepcopy(dealer._shoe)

  def give_french_decks(self, n=1):
    self.absorb_top(shoe_data.shoe_data.french_deck(n))

  def shoe_empty(self):
    return self.num_cards() == 0

  def shoe_length(self):
    return len(self._shoe)

  def pause(self):
    self._paused = True

  def resume(self):
    self._paused = False

  def paused(self):
    return self._paused

  def peek(self):
    return self._shoe.peek()

  def burn_cards(self, n):
    for _ in range(0,n):
      if len(self._shoe) > 0:
        self._shoe.burn()
      else:
        mudlog.error(f"{self.name} is trying to burn card from empty shoe.")

  def draw(self):
    if len(self._shoe) > 0:
      card = self._shoe.draw()
      print(card.debug())
      return card
    else:
      mudlog.error(f"{self.name} is trying to draw card from empy shoe.")

  def absorb_top(self, shoe):
    self._shoe.absorb_top(shoe)

  def absorb_bottom(self, shoe):
    self._shoe.absorb_bottom(shoe)

  def shuffle(self):
    self._shoe.shuffle()

  def clear_shoe(self):
    self._shoe.clear()

  def debug(self):
    ret_val = f"Type: {CYAN}Card Dealer{NORMAL}\r\n"
    ret_val += super().debug() + "\r\n"
    ret_val += f"Shoe Size: {CYAN}{len(self._shoe)}{NORMAL}"
    return ret_val