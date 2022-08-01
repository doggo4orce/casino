import cards
from color import *
import commands
import enum
import event
import logging
import pc
import string_handling
import spec_procs
import structs

class baccarat_hand:
  def __init__(self):
    self._player = [ ]
    self._banker = [ ]

  # getters
  @property
  def player(self):
    return self._player
  @property
  def banker(self):
    return self._banker
  @property
  def state(self):
    return self._state

  # setters
  @player.setter
  def player(self, new_player):
    self._player = new_player
  @banker.setter
  def banker(self, new_banker):
    self._banker = new_banker
  @state.setter
  def state(self, new_state):
    self._state = new_state

  def add_card(self, card, target):
    if target == "player":
      self.player.append(card)
    elif target == "banker":
      self.banker.append(card)
    return card

  def hand_value(self, cards):
    total = sum(card.value for card in cards)
    return total % 10

  def player_score(self):
    return self.hand_value(self.player)

  def banker_score(self):
    return self.hand_value(self.banker)

  def player_natural(self):
    return self.player_score() in {8,9} and len(self.player) == 2

  def banker_natural(self):
    return self.banker_score() in {8,9} and len(self.banker) == 2

  def panda(self):
    if len(self.player) == 3 and self.player_score() > self.banker_score():
      return self.player_score() == 8
  
  def dragon(self):
    if len(self.banker) == 3 and self.player_score() < self.banker_score():
      return self.banker_score() == 7

  def three_card_9_8(self):
    if len(self) == 6:
      # only way get 17 is a 9 and and 8
      return self.player_score() + self.banker_score() == 17

  def natural_9_8(self):
    if self.player_natural() and self.banker_natural():
      return self.player_score() + self.banker_score() == 17

  def any_8_7(self):
    x, y = self.player_score(), self.banker_score()
    return (x == 8 and y == 7) or (x == 7 and y == 8)

  def ascii_render(self):
    SPACE_BETWEEN_CARD = 1
    SPACE_BETWEEN_PLAYER_BANKER = 3

    ret_val  = "        Player:                     Banker:\r\n"

    if len(self) == 4:
      ret_val += "   +-----+   +-----+           +-----+   +-----+\r\n"
      ret_val += "   |{}   |   |{}   |           |{}   |   |{}   |\r\n".format(
        self.player[0].card_color() + self.player[0].card_rank_abbrev().ljust(2) + NORMAL,
        self.player[1].card_color() + self.player[1].card_rank_abbrev().ljust(2) + NORMAL,
        self.banker[0].card_color() + self.banker[0].card_rank_abbrev().ljust(2) + NORMAL,
        self.banker[1].card_color() + self.banker[1].card_rank_abbrev().ljust(2) + NORMAL)
      ret_val += "   |{}|   |{}|           |{}|   |{}|\r\n".format(
        self.player[0].card_color() + self.player[0].card_suit_abbrev_5() + NORMAL,
        self.player[1].card_color() + self.player[1].card_suit_abbrev_5() + NORMAL,
        self.banker[0].card_color() + self.banker[0].card_suit_abbrev_5() + NORMAL,
        self.banker[1].card_color() + self.banker[1].card_suit_abbrev_5() + NORMAL)
      ret_val += "   |   {}|   |   {}|           |   {}|   |   {}|\r\n".format(
        self.player[0].card_color() + self.player[0].card_rank_abbrev().rjust(2) + NORMAL,
        self.player[1].card_color() + self.player[1].card_rank_abbrev().rjust(2) + NORMAL,
        self.banker[0].card_color() + self.banker[0].card_rank_abbrev().rjust(2) + NORMAL,
        self.banker[1].card_color() + self.banker[1].card_rank_abbrev().rjust(2) + NORMAL)
      ret_val += "   +-----+   +-----+           +-----+   +-----+"
    elif len(self) == 5:
      if len(self.player) == 3:
        ret_val += "+-----+ +-----+ +-----+        +-----+   +-----+\r\n"
        ret_val += "|{}   | |{}   | |{}   |        |{}   |   |{}   |\r\n".format(
          self.player[0].card_color() + self.player[0].card_rank_abbrev().ljust(2) + NORMAL,
          self.player[1].card_color() + self.player[1].card_rank_abbrev().ljust(2) + NORMAL,
          self.player[2].card_color() + self.player[2].card_rank_abbrev().ljust(2) + NORMAL,
          self.banker[0].card_color() + self.banker[0].card_rank_abbrev().ljust(2) + NORMAL,
          self.banker[1].card_color() + self.banker[1].card_rank_abbrev().ljust(2) + NORMAL)
        ret_val += "|{}| |{}| |{}|        |{}|   |{}|\r\n".format(
          self.player[0].card_color() + self.player[0].card_suit_abbrev_5() + NORMAL,
          self.player[1].card_color() + self.player[1].card_suit_abbrev_5() + NORMAL,
          self.player[2].card_color() + self.player[2].card_suit_abbrev_5() + NORMAL,
          self.banker[0].card_color() + self.banker[0].card_suit_abbrev_5() + NORMAL,
          self.banker[1].card_color() + self.banker[1].card_suit_abbrev_5() + NORMAL)
        ret_val += "|   {}| |   {}| |   {}|        |   {}|   |   {}|\r\n".format(
          self.player[0].card_color() + self.player[0].card_rank_abbrev().rjust(2) + NORMAL,
          self.player[1].card_color() + self.player[1].card_rank_abbrev().rjust(2) + NORMAL,
          self.player[2].card_color() + self.player[2].card_rank_abbrev().rjust(2) + NORMAL,
          self.banker[0].card_color() + self.banker[0].card_rank_abbrev().rjust(2) + NORMAL,
          self.banker[1].card_color() + self.banker[1].card_rank_abbrev().rjust(2) + NORMAL)
        ret_val += "+-----+ +-----+ +-----+        +-----+   +-----+\r\n"
      else:
        ret_val += "   +-----+   +-----+        +-----+ +-----+ +-----+\r\n"
        ret_val += "   |{}   |   |{}   |        |{}   | |{}   | |{}   |\r\n".format(
          self.player[0].card_color() + self.player[0].card_rank_abbrev().ljust(2) + NORMAL,
          self.player[1].card_color() + self.player[1].card_rank_abbrev().ljust(2) + NORMAL,
          self.banker[0].card_color() + self.banker[0].card_rank_abbrev().ljust(2) + NORMAL,
          self.banker[1].card_color() + self.banker[1].card_rank_abbrev().ljust(2) + NORMAL,
          self.banker[2].card_color() + self.banker[2].card_rank_abbrev().ljust(2) + NORMAL)
        ret_val += "   |{}|   |{}|        |{}| |{}| |{}|\r\n".format(
          self.player[0].card_color() + self.player[0].card_suit_abbrev_5() + NORMAL,
          self.player[1].card_color() + self.player[1].card_suit_abbrev_5() + NORMAL,
          self.banker[0].card_color() + self.banker[0].card_suit_abbrev_5() + NORMAL,
          self.banker[1].card_color() + self.banker[1].card_suit_abbrev_5() + NORMAL,
          self.banker[2].card_color() + self.banker[2].card_suit_abbrev_5() + NORMAL)
        ret_val += "   |   {}|   |   {}|        |   {}| |   {}| |   {}|\n".format(
          self.player[0].card_color() + self.player[0].card_rank_abbrev().rjust(2) + NORMAL,
          self.player[1].card_color() + self.player[1].card_rank_abbrev().rjust(2) + NORMAL,
          self.banker[0].card_color() + self.banker[0].card_rank_abbrev().rjust(2) + NORMAL,
          self.banker[1].card_color() + self.banker[1].card_rank_abbrev().rjust(2) + NORMAL,
          self.banker[2].card_color() + self.banker[2].card_rank_abbrev().rjust(2) + NORMAL)
        ret_val += "   +-----+   +-----+        +-----+ +-----+ +-----+\r\n"
    elif len(self) == 6:
      ret_val += "+-----+ +-----+ +-----+     +-----+ +-----+ +-----+\r\n"
      ret_val += "|{}   | |{}   | |{}   |     |{}   | |{}   | |{}   |\r\n".format(
        self.player[0].card_color() + self.player[0].card_rank_abbrev().ljust(2) + NORMAL,
        self.player[1].card_color() + self.player[1].card_rank_abbrev().ljust(2) + NORMAL,
        self.player[2].card_color() + self.player[2].card_rank_abbrev().ljust(2) + NORMAL,
        self.banker[0].card_color() + self.banker[0].card_rank_abbrev().ljust(2) + NORMAL,
        self.banker[1].card_color() + self.banker[1].card_rank_abbrev().ljust(2) + NORMAL,
        self.banker[2].card_color() + self.banker[2].card_rank_abbrev().ljust(2) + NORMAL)
      ret_val += "|{}| |{}| |{}|     |{}| |{}| |{}|\n".format(
        self.player[0].card_color() + self.player[0].card_suit_abbrev_5() + NORMAL,
        self.player[1].card_color() + self.player[1].card_suit_abbrev_5() + NORMAL,
        self.player[2].card_color() + self.player[2].card_suit_abbrev_5() + NORMAL,
        self.banker[0].card_color() + self.banker[0].card_suit_abbrev_5() + NORMAL,
        self.banker[1].card_color() + self.banker[1].card_suit_abbrev_5() + NORMAL,
        self.banker[2].card_color() + self.banker[2].card_suit_abbrev_5() + NORMAL)
      ret_val += "|   {}| |   {}| |   {}|     |   {}| |   {}| |   {}|\r\n".format(
        self.player[0].card_color() + self.player[0].card_rank_abbrev().rjust(2) + NORMAL,
        self.player[1].card_color() + self.player[1].card_rank_abbrev().rjust(2) + NORMAL,
        self.player[2].card_color() + self.player[2].card_rank_abbrev().rjust(2) + NORMAL,
        self.banker[0].card_color() + self.banker[0].card_rank_abbrev().rjust(2) + NORMAL,
        self.banker[1].card_color() + self.banker[1].card_rank_abbrev().rjust(2) + NORMAL,
        self.banker[2].card_color() + self.banker[2].card_rank_abbrev().rjust(2) + NORMAL)
      ret_val += "+-----+ +-----+ +-----+     +-----+ +-----+ +-----+"
    else:
      ret_val = "Nothing has been dealt yet!"

    return ret_val

  def __len__(self):
    return len(self.player) + len(self.banker)

  def __str__(self):
    ret_val = f"Banker has {len(self.banker)} cards:\r\n"
    for card in self.banker:
      ret_val += f"{card}\n"
    ret_val += f"Player has {len(self.player)} cards.\r\n"
    for card in self.player:
      ret_val += f"{card}\r\n"
    return ret_val

class history_entry(enum.IntEnum):
  PLAYER_WIN = 1
  BANKER_WIN = 2
  TIE        = 3
  PANDA      = 4
  DRAGON     = 5

class extra_side_bet(enum.IntEnum):
  THREE_CARD_9_8 = 1
  NATURAL_9_8    = 2
  ANY_8_7        = 3

class baccarat_shoe(cards.shoe):
  def __init__(self, num_decks):
    super().__init__()

    self._history = list() # keeps track of standard history entries
    self._extras = list()  # keeps track of extra side bets

    for j in range(0, num_decks):
      self.absorb_bottom(baccarat_shoe.baccarat_deck())

  @classmethod
  def baccarat_deck(cls):
    deck = cards.shoe()
    for suit in cards.card_suit:
      deck.add_bottom(cards.card(cards.card_suit(suit), cards.card_rank(cards.card_rank.ACE), 1))
      deck.add_bottom(cards.card(cards.card_suit(suit), cards.card_rank(cards.card_rank.TWO), 2))
      deck.add_bottom(cards.card(cards.card_suit(suit), cards.card_rank(cards.card_rank.THREE), 3))
      deck.add_bottom(cards.card(cards.card_suit(suit), cards.card_rank(cards.card_rank.FOUR), 4))
      deck.add_bottom(cards.card(cards.card_suit(suit), cards.card_rank(cards.card_rank.FIVE), 5))
      deck.add_bottom(cards.card(cards.card_suit(suit), cards.card_rank(cards.card_rank.SIX), 6))
      deck.add_bottom(cards.card(cards.card_suit(suit), cards.card_rank(cards.card_rank.SEVEN), 7))
      deck.add_bottom(cards.card(cards.card_suit(suit), cards.card_rank(cards.card_rank.EIGHT), 8))
      deck.add_bottom(cards.card(cards.card_suit(suit), cards.card_rank(cards.card_rank.NINE), 9))
      deck.add_bottom(cards.card(cards.card_suit(suit), cards.card_rank(cards.card_rank.TEN), 10))
      deck.add_bottom(cards.card(cards.card_suit(suit), cards.card_rank(cards.card_rank.JACK), 10))
      deck.add_bottom(cards.card(cards.card_suit(suit), cards.card_rank(cards.card_rank.QUEEN), 10))
      deck.add_bottom(cards.card(cards.card_suit(suit), cards.card_rank(cards.card_rank.KING), 10))
    return deck

  def report_history(self, result):
    self._history.append(result)

  def report_extra(self, result):
    self._extras.append(result)

  def count_reports(self, result):
    return sum(map(lambda entry: entry == result, self._history))

  def count_extras(self, result):
    return sum(map(lambda side_bet: side_bet == result, self._extras))

class baccarat_dealer(cards.card_dealer):
  def __init__(self):
    """Creates a baccarat dealer
     state = keep track of what dealer will do next, FIRST_DRAW etc."""
    super().__init__()
    self._hand = None
    self._state = baccarat_dealer_state.IDLE
    self._initial_card_val = None
    self._simulation_mode = False

  # getters
  @property
  def state(self):
    return self._state
  @property
  def hand(self):
    return self._hand
  @property
  def initial_card_val(self):
    return self._initial_card_val
  @property
  def simulation_mode(self):
    return self._simulation_mode

  # setters
  @hand.setter
  def hand(self, new_hand):
    self._hand = new_hand
  @state.setter
  def state(self, new_state):
    self._state = new_state
  @initial_card_val.setter
  def initial_card_val(self, new_val):
    self._initial_card_val = new_val
  @simulation_mode.setter
  def simulation_mode(self, new_mode):
    self._simulation_mode = new_mode

  @classmethod
  def from_card_dealer(cls, dealer):
    ret_val = cls()
    # copy character attributes
    ret_val.entity = dealer.entity
    ret_val.ldesc = dealer.ldesc
    ret_val.inventory = dealer.inventory
    # copy npc attributes
    ret_val.prefix_command_triggers = dealer.prefix_command_triggers
    ret_val.suffix_command_triggers = dealer.suffix_command_triggers
    ret_val.heart_beat_procs = dealer.heart_beat_procs
    ret_val.hand = baccarat_hand()
    ret_val.state = baccarat_dealer_state.IDLE
    # copy dealer attributes
    ret_val.shoe = dealer.shoe
    return ret_val

  def deal_next_card(self, target):
    if target not in {"player", "banker"}:
      logging.warning(f"{self.name} attempting to add card to hand of invalid target: {target}.")
      return None
    if (len(self.hand.player) == 3 and target == "player") or (len(self.hand.banker) == 3 and target == "banker"):
      logging.warning(f"{self.name} attempting to give {target} layer a fourth card.")
      return None
    return self.hand.add_card(self.draw(), target)

  def check_player_natural(self):
    return self.hand.player_score() in {8,9}

  def check_banker_natural(self):
    return self.hand.banker_score() in {8,9}

  def check_player_third(self):
    if self.check_player_natural() or self.check_banker_natural():
      return False
    return self.hand.player_score() in {0,1,2,3,4,5}

  def check_banker_third(self):
    # shortcuts
    banker_score = self.hand.banker_score()
    player_third = None
    if len(self.hand.player) == 3:
      player_third = self.hand.player[2].value
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

"""Special Procedures for the Baccarat dealer:

   baccarat_dealer_history() <- display the history of the shoe
   baccarat_dealer_intro()   <- called as a basic response to a greeting
   baccarat_syntax_parser()  <- handles all syntax associated with the baccarat game
   baccarat_table_render()   <- renders a snapshot of the current hand in ascii
   baccarat_dealing()        <- handles the baccarat game"""

def baccarat_dealer_history(mud, me, ch, command, argument):
  if not isinstance(me, baccarat_dealer):
    logging.warning(f"Attempting to call inappropriate spec proc 'baccarat_dealer_intro' on npc {me}.")
    return

  if command != "history":
    return

  b_win = f"{BRIGHT_RED}*{NORMAL}"
  b_8 = f"{BRIGHT_RED}8{NORMAL}"
  b_9 = f"{BRIGHT_RED}9{NORMAL}"

  p_win = f"{BRIGHT_BLUE}*{NORMAL}"
  p_8 = f"{BRIGHT_BLUE}8{NORMAL}"
  p_9 = f"{BRIGHT_BLUE}9{NORMAL}"

  tie = f"{BRIGHT_GREEN}T{NORMAL}"
  panda = f"{BRIGHT_MAGENTA}P{NORMAL}"
  dragon = f"{BRIGHT_CYAN}D{NORMAL}"

  out_str = "  EZ Baccarat".ljust(33) + "\r\n"

  out_str += f"{YELLOW}+--------------+".ljust(33) + f"{b_win} - banker win\r\n"
  out_str += f"{YELLOW}|{BKGD_YELLOW}{b_win}{p_win}{p_win}           {YELLOW}|".ljust(76) + f"{b_8} - banker win with natural 8\r\n"
  out_str += f"{YELLOW}|{tie}{b_win}            {YELLOW}|".ljust(60) + f"{b_9} - banker win with natural 9\r\n"
  out_str += f"{YELLOW}|{b_win}{FLASH}{dragon}            {YELLOW}|".ljust(64) + f"{p_8} - player win with natural 8\r\n"
  out_str += f"{YELLOW}|{BKGD_YELLOW}{b_8}{tie}            {YELLOW}|".ljust(65) + f"{p_9} - player win with natural 9\r\n"
  out_str += f"{YELLOW}|{BKGD_CYAN}{p_9}{b_win}            {YELLOW}|".ljust(65) + f"{tie} - tie\r\n"
  out_str += f"{YELLOW}|{FLASH}{panda}{BKGD_WHITE}{b_9}            {YELLOW}|".ljust(69) + f"{panda} - panda\r\n"
  out_str += f"{YELLOW}+--------------+{NORMAL}".ljust(37) + f"{dragon} - dragon\r\n\r\n"

  out_str += f"{BKGD_YELLOW} {NORMAL} - any 8 over 7\r\n"
  out_str += f"{BKGD_CYAN} {NORMAL} - three card 9 over 8\r\n"
  out_str += f"{BKGD_WHITE} {NORMAL} - natural 9 over 8\r\n"
  ch.write(out_str)

  return spec_procs.prefix_command_trigger_messages.BLOCK_INTERPRETER

def baccarat_dealer_intro(mud, me, ch, command, argument):
  if not isinstance(me, baccarat_dealer):
    logging.warning(f"Attempting to call inappropriate spec proc 'baccarat_dealer_intro' on npc {me}.")
    return
  if command == "say" and argument.lower() == "hi":
    commands.do_say(me, None, "Hey, wanna play some Baccarat?  Type 'baccarat' for more information.", None, mud)
    return

def baccarat_syntax_parser(mud, me, ch, command, argument):
  if not isinstance(me, baccarat_dealer):
    logging.warning(f"Attempting to call inappropriate spec proc 'baccarat_dealer_intro' on npc {me}.")
    return

  help_str  = "Baccarat Commands:\r\n"
  help_str += "  baccarat start - play a baccarat shoe\r\n"
  help_str += "  baccarat simulate - simulate a baccarat shoe (fast)\r\n"

  if command == "baccarat":
    if argument.lower() in ["start", "simulate"]:
      if me.state != baccarat_dealer_state.IDLE:
        ch.write("There is already a game in progress!\r\n")
        return spec_procs.prefix_command_trigger_messages.BLOCK_INTERPRETER
      ch.write("You signal to the dealer to start the next shoe.\r\n")
      mud.echo_around(ch, None, f"{ch} signals to the dealer to start the next shoe.\r\n")
      me.paused = True
      me.state = baccarat_dealer_state.BEGIN_SHOE
      mud.add_event(event.event(me, unpause_dealer, None, 10))
      
      me.simulation_mode = argument.lower() == "simulate"

    else:
      ch.write(help_str)
    return spec_procs.prefix_command_trigger_messages.BLOCK_INTERPRETER

def baccarat_table_render(mud, me, ch, command, argument):
  if not isinstance(me, baccarat_dealer):
    logging.warning(f"Attempting to call inappropriate spec proc 'baccarat_dealer_intro' on npc {me}.")
    return

  if command == "table":
    if me.hand == None:
      ch.write("The table is empty.\r\n")
    else:
      ch.write(me.hand.ascii_render() + "\r\n")
    return spec_procs.prefix_command_trigger_messages.BLOCK_INTERPRETER

class baccarat_dealer_state(enum.IntEnum):
  IDLE                = 1
  BEGIN_SHOE          = 2
  SHUFFLE_SHOE        = 3
  FIRST_DRAW          = 4
  BURN_CARDS          = 5
  PLAYER_FIRST        = 6
  BANKER_FIRST        = 7
  PLAYER_SECOND       = 8
  BANKER_SECOND       = 9 
  SHOW_INITIAL        = 10
  CHECK_NATURAL       = 11
  CHECK_PLAYER        = 12
  DEAL_PLAYER_THIRD   = 13
  UPDATE_PLAYER_THIRD = 14
  CHECK_BANKER        = 15
  DEAL_BANKER_THIRD   = 16
  UPDATE_BANKER_THIRD = 17
  REPORT_WINNER       = 18
  CLEAR_CARDS         = 19

def baccarat_dealing(mud, me):
  NUM_DECKS = 8

  panda_string = "{}P{}a{}n{}d{}a{}!{}".format(
    CYAN,
    DARK_GRAY,
    CYAN,
    DARK_GRAY,
    CYAN,
    DARK_GRAY,
    NORMAL)

  dragon_string = "{}D{}r{}a{}g{}o{}n{}!{}".format(
    CYAN,
    GREEN,
    CYAN,
    GREEN,
    CYAN,
    GREEN,
    CYAN,
    NORMAL)

  if me.state == baccarat_dealer_state.IDLE:
    return
  if me.paused:
    return
  if not isinstance(me, baccarat_dealer):
    logging.warning(f"Attempting to call inappropriate spec proc 'baccarat_dealing' on npc {me}.")
    return
    
  me.paused = True
  pause = 0
  if me.state == baccarat_dealer_state.BEGIN_SHOE:
    me.shoe = baccarat_shoe(NUM_DECKS)
    mud.echo_around(me, None, f"{me} assembles a new shoe consisting of {NUM_DECKS} deck{'s' if NUM_DECKS > 1 else ' '}.\r\n")
    me.state = baccarat_dealer_state.SHUFFLE_SHOE
    pause = 30
  elif me.state == baccarat_dealer_state.SHUFFLE_SHOE:
    me.shuffle()
    mud.echo_around(me, None, f"{me} shuffles the shoe.\r\n")
    me.state = baccarat_dealer_state.FIRST_DRAW
    pause = 30
  elif me.state == baccarat_dealer_state.FIRST_DRAW:
    first_card = me.draw()
    me.initial_card_val = first_card.value
    mud.echo_around(me, None, "{} draws and reveals the first card, which is {} {}.\r\n".format(
      me,
      string_handling.ana(cards.card_rank(first_card.rank).name),
      first_card
      ))
    me.state = baccarat_dealer_state.BURN_CARDS
    pause = 30
  elif me.state == baccarat_dealer_state.BURN_CARDS:
    for j in range(0, me.initial_card_val):
      me.draw()
    mud.echo_around(me, None, f"{me} burns {me.initial_card_val} cards.\n")
    me.state = baccarat_dealer_state.PLAYER_FIRST
    pause = 30
  elif me.state == baccarat_dealer_state.PLAYER_FIRST:
    if me.shoe.size < 6:
      commands.do_say(me, None, "Ladies and gentlemen, that was our final hand.  Thanks for playing!", None, mud)
      mud.echo_around(me, None, "Player wins: {}{}{} (including pandas)\r\nBanker wins: {}{}{}\r\nTies: {}{}{}\r\nPandas: {}{}{}\r\nDragons: {}{}{}\r\n".format(
        BLUE, me.shoe.count_reports(history_entry.PLAYER_WIN) + me.shoe.count_reports(history_entry.PANDA), NORMAL,
        RED, me.shoe.count_reports(history_entry.BANKER_WIN), NORMAL,
        GREEN, me.shoe.count_reports(history_entry.TIE), NORMAL,
        MAGENTA, me.shoe.count_reports(history_entry.PANDA), NORMAL,
        CYAN, me.shoe.count_reports(history_entry.DRAGON), NORMAL))
      mud.echo_around(me, None, "3-card 9/8's: {}{}{}\r\nNatural 9/8's: {}{}{}\r\nAny 8/7's: {}{}{}\r\n".format(
        YELLOW, me.shoe.count_extras(extra_side_bet.THREE_CARD_9_8), NORMAL,
        YELLOW, me.shoe.count_extras(extra_side_bet.NATURAL_9_8), NORMAL,
        YELLOW, me.shoe.count_extras(extra_side_bet.ANY_8_7), NORMAL
        ))
      me.shoe = None
      me.state = baccarat_dealer_state.IDLE
      me.paused = False
      me.simulation_mode = False
      return
    me.hand = baccarat_hand()
    mud.echo_around(me, None, f"{me} deals {me.deal_next_card('player')} to the player.\r\n")
    me.state = baccarat_dealer_state.BANKER_FIRST
    pause = 10
  elif me.state == baccarat_dealer_state.BANKER_FIRST:
    mud.echo_around(me, None, f"{me} deals {me.deal_next_card('banker')} to the banker.\r\n")
    me.state = baccarat_dealer_state.PLAYER_SECOND
    pause = 10
  elif me.state == baccarat_dealer_state.PLAYER_SECOND:
    mud.echo_around(me, None, f"{me} deals {me.deal_next_card('player')} to the player.\r\n")
    me.state = baccarat_dealer_state.BANKER_SECOND
    pause = 10
  elif me.state == baccarat_dealer_state.BANKER_SECOND:
    mud.echo_around(me, None, f"{me} deals {me.deal_next_card('banker')} to the banker.\r\n")
    me.state = baccarat_dealer_state.SHOW_INITIAL
    pause = 10
  elif me.state == baccarat_dealer_state.SHOW_INITIAL:
    mud.echo_around(me, None, me.hand.ascii_render() + "\n\n")
    commands.do_say(me, None, f"Player shows {me.hand.player_score()}. Banker shows {me.hand.banker_score()}.", None, mud)
    me.state = baccarat_dealer_state.CHECK_NATURAL
    pause = 60
  elif me.state == baccarat_dealer_state.CHECK_NATURAL:
    if me.hand.player_natural():
      commands.do_say(me, None, f"Player shows natural {me.hand.player_score()}.  No more draws.", None, mud)
      me.state = baccarat_dealer_state.REPORT_WINNER
      pause = 30
    elif me.hand.banker_natural():
      commands.do_say(me, None, f"Banker shows natural {me.hand.banker_score()}.  No more draws.", None, mud)
      me.state = baccarat_dealer_state.REPORT_WINNER
      pause = 30
    else:
      me.state = baccarat_dealer_state.CHECK_PLAYER
      pause = 30
  elif me.state == baccarat_dealer_state.CHECK_PLAYER:
    if me.check_player_third():
      commands.do_say(me, None, "Card for player.", None, mud)
      me.state = baccarat_dealer_state.DEAL_PLAYER_THIRD
    else:
      commands.do_say(me, None, "Player stands.", None, mud)
      me.state = baccarat_dealer_state.CHECK_BANKER
    pause = 10
  elif me.state == baccarat_dealer_state.DEAL_PLAYER_THIRD:
    player_third = me.deal_next_card('player')
    mud.echo_around(me, None, "{} deals {} {} to the player.\r\n".format(
      me,
      string_handling.ana(cards.card_rank(player_third.rank).name),
      player_third
      ))
    me.state = baccarat_dealer_state.UPDATE_PLAYER_THIRD
    pause = 10
  elif me.state == baccarat_dealer_state.UPDATE_PLAYER_THIRD:
    mud.echo_around(me, None, "\n" + me.hand.ascii_render() + "\r\n")
    me.state = baccarat_dealer_state.CHECK_BANKER
    pause = 60
  elif me.state == baccarat_dealer_state.CHECK_BANKER:
    if me.check_banker_third():
      commands.do_say(me, None, "Card for banker.", None, mud)
      me.state = baccarat_dealer_state.DEAL_BANKER_THIRD
      pause = 10
    else:
      commands.do_say(me, None, "Banker stands.", None, mud)
      me.state = baccarat_dealer_state.REPORT_WINNER
      pause = 30
  elif me.state == baccarat_dealer_state.DEAL_BANKER_THIRD:
    banker_third = me.deal_next_card('banker')
    mud.echo_around(me, None, "{} deals {} {} to the banker.\r\n".format(
      me,
      string_handling.ana(cards.card_rank(banker_third.rank).name),
      banker_third
      ))
    me.state = baccarat_dealer_state.UPDATE_BANKER_THIRD
    pause = 10
  elif me.state == baccarat_dealer_state.UPDATE_BANKER_THIRD:
    mud.echo_around(me, None, "\n" + me.hand.ascii_render() + "\r\n")
    me.state = baccarat_dealer_state.REPORT_WINNER
    pause = 60
  elif me.state == baccarat_dealer_state.REPORT_WINNER:
    if me.hand.panda():
      commands.do_say(me, None, panda_string, None, mud)
      me.shoe.report_history(history_entry.PANDA)
    elif me.hand.dragon():
      commands.do_say(me, None, dragon_string, None, mud)
      me.shoe.report_history(history_entry.DRAGON)
    elif me.hand.player_score() > me.hand.banker_score():
      commands.do_say(me, None, f"Player wins {me.hand.player_score()} over {me.hand.banker_score()}.", None, mud)
      me.shoe.report_history(history_entry.PLAYER_WIN)
    elif me.hand.player_score() < me.hand.banker_score():
      commands.do_say(me, None, f"Banker wins {me.hand.banker_score()} over {me.hand.player_score()}.", None, mud)
      me.shoe.report_history(history_entry.BANKER_WIN)
    else:
      commands.do_say(me, None, f"Player and banker tie!", None, mud)
      me.shoe.report_history(history_entry.TIE)
    
    # Check Michael's Side Bets
    if me.hand.three_card_9_8():
      me.shoe.report_extra(extra_side_bet.THREE_CARD_9_8)
    if me.hand.natural_9_8():
      me.shoe.report_extra(extra_side_bet.NATURAL_9_8)
    if me.hand.any_8_7():
      me.shoe.report_extra(extra_side_bet.ANY_8_7)

    me.hand = None
    me.state = baccarat_dealer_state.CLEAR_CARDS
    pause = 60
  elif me.state == baccarat_dealer_state.CLEAR_CARDS:
    mud.echo_around(me, None, f"{me} clears the cards from the table.\n")
    me.state = baccarat_dealer_state.PLAYER_FIRST
    pause = 120
  if pause != 0:
    if me.simulation_mode:
      me.paused = False
    else:
      mud.add_event(event.event(me, unpause_dealer, None, pause))
  return

"""This function is used by the preceding function to allow pauses between behaviour for the Baccarat dealer.
   For example, if the dealer should pause for one second, set

     the_dealer.paused=True

   and then attach to it an event which calls this function with a countdown of 30.

   TODO:  this seems a bit silly.  would it not make more sense to just add a timer field directly
   to NPC's if they are to be paused?"""
def unpause_dealer(ch, mud):
  ch.paused = False

if __name__ == '__main__':
  new_shoe = baccarat_shoe(6)
  new_shoe.add_report(history_entry.PLAYER_WIN)
  new_shoe.add_report(history_entry.PANDA)
  new_shoe.add_report(history_entry.BANKER_WIN)
  print(f"Player wins: {new_shoe.count_reports(history_entry.PLAYER_WIN)} (including pandas)")
  print(f"Banker wins: {new_shoe.count_reports(history_entry.BANKER_WIN)}")
  print(f"Ties: {new_shoe.count_reports(history_entry.TIE)}")
