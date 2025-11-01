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
      hand             = the current hand in progress (empty between hands)
      state            = keep track of what dealer will do next, FIRST_DRAW etc.
      bac_paused       = RESERVED for heart beat proc baccarat_dealing
      initial_card_val = keep track of how many cards to burn
      simulation_mode  = if True, game runs way too fast to play"""
    super().__init__()
    self._baccarat_hand = baccarat_hand_data.baccarat_hand_data()
    self.bac_state = baccarat_dealer_state.IDLE
    self.bac_paused = 0
    self._initial_card_val = None
    self.simulation_mode = False
    self._history = list()
    self._extras = list()

  @classmethod
  def from_card_dealer(cls, dealer):
    ret_val = cls()

    # copy card dealer attributes
    super().copy_from(ret_val, dealer)

    return ret_val

  def clear_baccarat_hand(self):
    self._baccarat_hand.clear()

  def deal(self, card, target):
    if target not in {"player", "banker"}:
      mudlog.error(f"{self.name} attempting to add card to hand of invalid target: {target}.")
      return
    if (self._baccarat_hand.num_player_cards() == 3 and target == "player") or (self._baccarat_hand.num_banker_cards() == 3 and target == "banker"):
      mudlog.error(f"{self.name} attempting to give {target} layer a fourth card.")
      return

    self._baccarat_hand.add_card(card, target)

  def player_score(self):
    return self._baccarat_hand.player_score()

  def banker_score(self):
    return self._baccarat_hand.banker_score()

  def num_player_cards(self):
    return self._baccarat_hand.num_player_cards()

  def num_banker_cards(self):
    return self._baccarat_hand.num_banker_cards()

  def player_natural(self):
    num_cards = self._baccarat_hand.num_player_cards()
    if num_cards != 2:
      mudlog.warning(f"Player has {num_cards} but {self.name} checking for natural.")
      return False
    return self.player_score() in {8,9}

  def banker_natural(self):
    num_cards = self._baccarat_hand.num_banker_cards()
    if num_cards != 2:
      mudlog.warning(f"Banker has {num_cards} but {self.name} checking for natural.")
      return False
    return self.banker_score() in {8,9}

  def player_third(self):
    return not self.banker_natural() and self.player_score() in {0,1,2,3,4,5}

  def banker_third(self):
    # shortcuts
    banker_score = self._baccarat_hand.banker_score()
    player_third = None
    if self.num_player_cards() == 3:
      player_third = baccarat_hand_data.baccarat_hand_data.card_value(self._baccarat_hand.player[2])
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

  def panda(self):
    return self._baccarat_hand.panda()

  def dragon(self):
    return self._baccarat_hand.dragon()

  def three_card_9_8(self):
    return self._baccarat_hand.three_card_9_8()

  def natural_9_8(self):
    return self._baccarat_hand.natural_9_8()

  def any_8_7(self):
    return self._baccarat_hand.any_8_7()

  def report_history(self, result):
    self._shoe.report_history(result)

  def report_extra(self, result):
    self._extras.append(result)

  def count_reports(self, result):
    return sum(map(lambda entry: entry == result, self._history))

  def count_extras(self, result):
    return sum(map(lambda side_bet: side_bet == result, self._extras))

  """report_history(result) <-- records an occurance of result to self.history
     report_extra(result)   <-- records an occurance of result to self.extras
     count_reports(result)  <-- counts number of occurances of result in self.history
     count_extras(result)   <-- counts number of occurances of result in self.extras"""

  def report_history(self, result):
    self._history.append(result)

  def report_extra(self, result):
    self._extras.append(result)

  def count_reports(self, result):
    return sum(map(lambda entry: entry == result, self._history))

  def count_extras(self, result):
    return sum(map(lambda side_bet: side_bet == result, self._extras))

  def debug(self):
    ret_val = super().debug() + "\r\n"
    ret_val += f"Hand: "
    if len(self._baccarat_hand) == 0:
      ret_val += f"{CYAN}empty{NORMAL}\r\n"
    else:
      ret_val += f"\r\n{self._baccarat_hand.display2()}\r\n"
    ret_val += f"State: {CYAN}{baccarat_dealer_state(self.bac_state).name}{NORMAL}\r\n"
    ret_val += f"Baccarat Paused: {CYAN}{self.bac_paused}{NORMAL}"
    return ret_val