import baccarat_hand_data
import card_dealer_data
from color import *
import enum
import mudlog
import npc_data

class baccarat_dealer_state(enum.IntEnum):
  IDLE                = 1
  BEGIN_SHOE          = 2
  SHUFFLE_SHOE        = 3
  FIRST_DRAW          = 4
  BURN_CARDS          = 5
  LAST_CALL_BETS      = 6
  NO_MORE_BETS        = 7
  PLAYER_FIRST        = 8
  BANKER_FIRST        = 9
  PLAYER_SECOND       = 10
  BANKER_SECOND       = 11
  SHOW_INITIAL        = 12
  CHECK_NATURAL       = 13
  CHECK_PLAYER        = 14
  DEAL_PLAYER_THIRD   = 15
  UPDATE_PLAYER_THIRD = 16
  CHECK_BANKER        = 17
  DEAL_BANKER_THIRD   = 18
  UPDATE_BANKER_THIRD = 19
  REPORT_WINNER       = 20
  CLEAR_CARDS         = 21

class baccarat_dealer_data(card_dealer_data.card_dealer_data):
  def __init__(self):
    """Creates a baccarat dealer
      hand             = the current hand in progress, or None between hands
      state            = keep track of what dealer will do next, FIRST_DRAW etc.
      bac_paused       = RESERVED for heart beat proc baccarat_dealing
      initial_card_val = keep track of how many cards to burn
      simulation_mode  = if True, game runs way too fast to play"""
    super().__init__()
    self._hand = baccarat_hand_data.baccarat_hand_data()
    self._bac_state = baccarat_dealer_state.IDLE
    self._bac_paused = 0
    self._initial_card_val = None
    self._simulation_mode = False

  @classmethod
  def from_card_dealer(cls, dealer):
    ret_val = cls()

    # copy card dealer attributes
    super().copy_from(ret_val, dealer)

    return ret_val

  def new_hand(self):
    self._hand = baccarat_hand_data.baccarat_hand_data()

  def add_card(self, card, target):
    self._hand.add_card(card, target)

  def deal_next_card(self, target):
    if target not in {"player", "banker"}:
      mudlog.error(f"{self.name} attempting to add card to hand of invalid target: {target}.")
      return
    if (self._hand.num_player_cards() == 3 and target == "player") or (self._hand.num_banker_cards() == 3 and target == "banker"):
      mudlog.error(f"{self.name} attempting to give {target} layer a fourth card.")
      return
    self.add_card(self.draw(), target)

  def player_score(self):
    return self._hand.player_score()

  def banker_score(self):
    return self._hand.banker_score()

  def player_natural(self):
    num_cards = self._hand.num_player_cards()
    if num_cards != 2:
      mudlog.warning(f"Player has {num_cards} but {self.name} checking for natural.")
      return False
    return self.player_score() in {8,9}

  def banker_natural(self):
    num_cards = self._hand.num_banker_cards()
    if num_cards != 2:
      mudlog.warning(f"Banker has {num_cards} but {self.name} checking for natural.")
      return False
    return self.banker_score() in {8,9}

  def player_third(self):
    return not self.banker_natural() and self.hand.player_score() in {0,1,2,3,4,5}

  def banker_third(self):
    # shortcuts
    banker_score = self.hand.banker_score()
    player_third = None
    if len(self.hand.player) == 3:
      player_third = baccarat_hand.card_value(self.hand.player[2])
    if player_third == None:
      return banker_score in {0,1,2,3,4,5}
    if banker_score in {0,1,2}:
      return True
    if banker_score == 3:
      return player_third != 8
    if banker_score == 4:
      return player_third in {2,3,4,5,6,7}
    if banker_score == 5:
      return player_third in {4,5,6,7}
    if banker_score == 6:
      return player_third in {6,7}
    return False

  def three_card_9_8(self):
    return self._hand.three_card_9_8()

  def natural_9_8(self):
    return self._hand.natural_9_8()

  def any_8_7(self):
    return self._hand.any_8_7()

  def debug(self):
    ret_val = super().debug() + "\r\n"
    ret_val += f"Hand:"
    if len(self._hand) == 0:
      ret_val += f"{CYAN}empty{NORMAL}\r\n"
    else:
      ret_val += f"\r\n{self._hand.display2()}\r\n"
    ret_val += f"State: {CYAN}{baccarat_dealer_state(self._bac_state).name}{NORMAL}\r\n"
    ret_val += f"Baccarat Paused: {CYAN}{self._bac_paused}{NORMAL}"
    return ret_val