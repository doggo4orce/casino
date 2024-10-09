import cards
from color import *
import commands
import enum
import event
import mudlog
import nanny
import pc
import string_handling
import spec_proc_data

class baccarat_hand:
  """Creates a single hand of baccarat.
     player = list of up to three cards used to compute player's score
     banker = same, but for banker"""
  def __init__(self):
    self._player = list()
    self._banker = list()

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

  def ascii_rep(self, cards, idx, row):
    if row not in range(0,5):
      print(f"function {ascii_rep_banker} called with bad row {row}")
      return None
    try:
      return cards[idx].ascii_rep()[row]
    except IndexError:
      # maybe we're tryign to read 2nd or 3rd card but banker doesn't have that many
      return ' ' * 7

  def ascii_rep_player(self, idx, row):
    return self.ascii_rep(self.player, idx, row)

  def ascii_rep_banker(self, idx, row):
    return self.ascii_rep(self.banker, idx, row)

  """add_card(card, target) <-- adds the card to either the player or banker's hand
     add_player(name)       <-- add a player to the game
     card_value(card)       <-- returns 7 if card is a SEVEN, 10 for a KING, etc.
     hand_value(cards)      <-- determines the score based on list of cards
     player_score()         <-- return's player's current score
     banker_score()         <-- returns the banker's current score
     player_natural()       <-- checks if player's first two cards add to 8/9
     banker_natural()       <-- same but for player
     panda()                <-- checks if the player won with three card 8
     dragon()               <-- checks if banker won with three card 7
     three_card_9_8()       <-- checks if hand won with 9 over 8 (both 3 cards)
     natural_9_8()          <-- checks if hand won with 9 over 8 (both natural)
     any_8_7()              <-- checks if hand won with 8 over 7
     display()              <-- displays the cards in a string return"""

  def add_card(self, card, target):
    if target == "player":
      self.player.append(card)
    elif target == "banker":
      self.banker.append(card)
    return card

  @staticmethod
  def card_value(card):
    if int(card.rank) in range(1, 11):
      return int(card.rank)
    else:
      return 10 

  def hand_value(self, cards):
    total = sum(self.card_value(card) for card in cards)
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
      # only way to get 17 is a 9 and and 8
      return self.player_score() + self.banker_score() == 17

  def natural_9_8(self):
    if self.player_natural() and self.banker_natural():
      return self.player_score() + self.banker_score() == 17

  def any_8_7(self):
    return {self.player_score(), self.banker_score()} == {7, 8}

  def display2(self):
    SPACE_BEFORE_CARDS = 9
    SPACE_BETWEEN_PLAYER_BANKER = 16
    SPACE_BETWEEN_PLAYER_CARDS = 1
    SPACE_BETWEEN_BANKER_CARDS = 1

    ret_val = ""

    for idx in range(0,5):
      ret_val += f"{' '*SPACE_BEFORE_CARDS}"
      for j in range(0,3):
        ret_val += f"{self.ascii_rep_player(j, idx)}{' '*SPACE_BETWEEN_PLAYER_CARDS}"

      ret_val += ' '*(SPACE_BETWEEN_PLAYER_BANKER - 1)

      for j in range(0,3):
        ret_val += f"{self.ascii_rep_banker(j, idx)}{' '*SPACE_BETWEEN_BANKER_CARDS}"

      ret_val += "\r\n"

    return ret_val

  def display(self):
    SPACE_BEFORE_CARDS = 0
    SPACE_BETWEEN_PLAYER_BANKER = 0
    SPACE_BETWEEN_PLAYER_CARDS = 0
    SPACE_BETWEEN_BANKER_CARDS = 0

    ret_val = ""
 
    n_p = len(self.player)
    n_b = len(self.banker)

    # ensure player and banker have the correct number of cards
    for n in [n_p,n_b]:
      if n < 1 or n > 3:
        return ret_val

    if n_p == 2:
      SPACE_BEFORE_CARDS = 3
      SPACE_BETWEEN_PLAYER_CARDS = 3
    elif n_p == 3:
      SPACE_BEFORE_CARDS = 0
      SPACE_BETWEEN_PLAYER_CARDS = 1
    
    if n_b == 2:
      SPACE_BETWEEN_BANKER_CARDS = 3
    elif n_b == 3:
      SPACE_BETWEEN_BANKER_CARDS = 1

    if n_b + n_p == 4:
      SPACE_BETWEEN_PLAYER_BANKER = 11
    elif n_b + n_p == 5:
      SPACE_BETWEEN_PLAYER_BANKER = 8
    else:
      SPACE_BETWEEN_PLAYER_BANKER = 5

    ret_val = "        Player                      Banker\r\n\r\n"

    for i in range(0, 5):
      ret_val += ' ' * SPACE_BEFORE_CARDS

      # player cards first
      for j in range(0, n_p):
        ret_val +=  self.player[j].ascii_rep()[i]
        if j < n_p - 1:
          ret_val += ' ' * SPACE_BETWEEN_PLAYER_CARDS
        else:
          ret_val += ' ' * SPACE_BETWEEN_PLAYER_BANKER

      # then banker cards
      for j in range(0, n_b):
        ret_val +=  self.banker[j].ascii_rep()[i]
        if j < n_p - 1:
          ret_val += ' ' * SPACE_BETWEEN_BANKER_CARDS

      ret_val += "\r\n"  
    
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
  """Keeps track of a baccarat shoe in progress.
    history = outcomes from previous hands, e.g. player win, dragon
    extras  = occurances of side bet winnings, e.g. three card 9 over 8"""
  def __init__(self, num_decks):
    super().__init__()
    self._history = list()
    self._extras = list()
    for j in range(0, num_decks):
      self.absorb_bottom(cards.shoe.french_deck())

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

class baccarat_dealer(cards.card_dealer):
  def __init__(self):
    """Creates a baccarat dealer
      hand             = the current hand in progress, or None between hands
      state            = keep track of what dealer will do next, FIRST_DRAW etc.
      bac_paused       = RESERVED for heart beat proc baccarat_dealing
      initial_card_val = keep track of how many cards to burn
      simulation_mode  = if True, game runs way too fast to play"""
    super().__init__()
    self._hand = None
    self._bac_state = baccarat_dealer_state.IDLE
    self._bac_paused = 0
    self._initial_card_val = None
    self._simulation_mode = False

  # getters
  @property
  def hand(self):
    return self._hand
  @property
  def bac_state(self):
    return self._bac_state
  @property
  def bac_paused(self):
    return self._bac_paused
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
  @bac_state.setter
  def bac_state(self, new_bac_state):
    self._bac_state = new_bac_state
  @bac_paused.setter
  def bac_paused(self, new_paused):
    self._bac_paused = new_paused
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
    ret_val.bac_state = baccarat_dealer_state.IDLE
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

  def debug(self):
    ret_val = super().debug()
    ret_val += f"State: {baccarat_dealer_state(self.bac_state).name}\r\n"
    ret_val += f"Paused: {self.bac_paused}"
    return ret_val

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

"""Special Procedures for the Baccarat dealer:

   baccarat_dealer_history() <- display the history of the shoe
   baccarat_dealer_intro()   <- basic response to a greeting
   baccarat_syntax_parser()  <- handles all syntax associated with the baccarat game
   baccarat_dealing()        <- handles the baccarat game"""

def baccarat_dealer_history(mud, me, ch, command, argument, db):
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

def baccarat_dealer_intro(mud, me, ch, command, argument, db):
  if not isinstance(me, baccarat_dealer):
    logging.warning(f"Attempting to call inappropriate spec proc 'baccarat_dealer_intro' on npc {me}.")
    return
  if command == "say" and argument.lower() == "hi":
    commands.do_say(me, None, "Hey, wanna play some Baccarat?  Type 'baccarat' for more information.", None, mud, db)
    return

def baccarat_dealer_syntax_parser(mud, me, ch, command, argument, db):
  if not isinstance(me, baccarat_dealer):
    logging.warning(f"Attempting to call inappropriate spec_proc 'baccarat_dealer_syntax_parser' on npc {me}.")
    return

  help_str  = "Baccarat Commands:\r\n"
  help_str += "  baccarat chips         - ask dealer for a set of chips\r\n"
  help_str += "  baccarat playing       - see who is playing the game\r\n"
  help_str += "  baccarat start         - start the game\r\n"
  help_str += "  baccarat simulate      - simulate a baccarat shoe (fast)\r\n"
  help_str += "  baccarat stop          - stop the game\r\n"
  help_str += "\r\n"
  help_str += "Gameplay Commands:\r\n"
  help_str += "  sit                    - sit down at the table (if there is room)\r\n"
  help_str += "  leave                  - stand up and leave the table\r\n"
  help_str += "  bet <player or banker> - bet a red chip on player or banker\r\n"

  if command == "bet":
    if me.bac_state not in [
      baccarat_dealer_state.BEGIN_SHOE,
      baccarat_dealer_state.SHUFFLE_SHOE,
      baccarat_dealer_state.FIRST_DRAW,
      baccarat_dealer_state.BURN_CARDS,
      baccarat_dealer_state.LAST_CALL_BETS,
      baccarat_dealer_state.NO_MORE_BETS]:  # <-- hasn't quite said no more bets
      ch.write("The dealer slaps you.\r\n")
      return spec_procs.prefix_command_trigger_messages.BLOCK_INTERPRETER
    else:
      ch.write("You put a red chip down on the table.\r\n")
      return spec_procs.prefix_command_trigger_messages.BLOCK_INTERPRETER
  elif command == "baccarat":
    if argument.lower() == "playing":
      if len(me.players) == 0:
        commands.do_say(me, None, f"Right now, we have nobody playing!", None, mud, db)
      else:
        names = [name.capitalize() for name in me.players]
        commands.do_say(me, None, f"Right now, we have {string_handling.oxford_comma(names)} playing.", None, mud, db)
    elif argument.lower() == "stop":
      me.bac_state = baccarat_dealer_state.IDLE
    elif argument.lower() in ["start", "simulate"]:
      if me.bac_state != baccarat_dealer_state.IDLE:
        ch.write("There is already a game in progress!\r\n")
        return spec_procs.prefix_command_trigger_messages.BLOCK_INTERPRETER
      ch.write("You signal to the dealer to start the next shoe.\r\n")
      mud.echo_around(ch, None, f"{ch} signals to the dealer to start the next shoe.\r\n")
      me.bac_paused = 10
      me.bac_state = baccarat_dealer_state.BEGIN_SHOE
  
      if argument.lower() == "simulate":
        me.simulation_mode = True
    elif argument.lower() == "chips":
      ch.write("You ask the dealer for some chips to play with.\r\n")
      ch.write(f"{me} nods in your direction without comment.\r\n")
      mud.echo_around(ch, None, f"{me} nods in {ch}'s direction without comment.\r\n")

      for n in range(0, 5):
        red_chip = mud.load_obj('stockville[red_chip]')
        ch.inventory.insert(red_chip)

      ch.write(f"{me} gives you five red chips.")
      mud.echo_around(ch, None, f"{me} gives {ch} five red chips.")

    else:
      ch.write(help_str)
    return spec_procs.prefix_command_trigger_messages.BLOCK_INTERPRETER
  elif command == "bet":
    if argument.lower() in ["player", "banker"]:
      pass
    pass

def baccarat_dealing(mud, me, db):
  NUM_DECKS = 6

  panda_string = "{}P{}a{}n{}d{}a{}!{}".format(CYAN, DARK_GRAY, CYAN, DARK_GRAY, CYAN, DARK_GRAY, NORMAL)
  dragon_string = "{}D{}r{}a{}g{}o{}n{}!{}".format(CYAN, GREEN, CYAN, GREEN, CYAN, GREEN, CYAN, NORMAL)

  if me.bac_state == baccarat_dealer_state.IDLE:
    return
  if me.bac_paused > 0:
    me.bac_paused -= 1
    return
  if not isinstance(me, baccarat_dealer):
    logging.warning(f"{me} attempting to call 'baccarat_dealing' but is not a baccarat dealer")
    return
  
  if me.bac_state == baccarat_dealer_state.BEGIN_SHOE:
    me.shoe = baccarat_shoe(NUM_DECKS)
    mud.echo_around(me, None, f"{me} assembles a new shoe consisting of {NUM_DECKS} deck{'s' if NUM_DECKS > 1 else ' '}.\r\n")
    me.bac_state = baccarat_dealer_state.SHUFFLE_SHOE
    pause = 30
  elif me.bac_state == baccarat_dealer_state.SHUFFLE_SHOE:
    me.shuffle()
    mud.echo_around(me, None, f"{me} shuffles the shoe.\r\n")
    me.bac_state = baccarat_dealer_state.FIRST_DRAW
    pause = 30
  elif me.bac_state == baccarat_dealer_state.FIRST_DRAW:
    first_card = me.draw()
    me.initial_card_val = baccarat_hand.card_value(first_card)
    mud.echo_around(me, None, "{} draws the first card, which is {} {}.\r\n".format(
      me, string_handling.ana(cards.card_rank(first_card.rank).name), first_card))
    me.bac_state = baccarat_dealer_state.BURN_CARDS
    pause = 30
  elif me.bac_state == baccarat_dealer_state.BURN_CARDS:
    for j in range(0, me.initial_card_val):
      me.draw()
    mud.echo_around(me, None, f"{me} burns {me.initial_card_val} card{'s' if me.initial_card_val > 1 else ''}.\n")
    me.bac_state = baccarat_dealer_state.LAST_CALL_BETS
    pause = 30
  elif me.bac_state == baccarat_dealer_state.LAST_CALL_BETS:
    commands.do_say(me, None, f"Last call, any more bets?", None, mud, db)
    me.bac_state = baccarat_dealer_state.NO_MORE_BETS
    pause = 120
  elif me.bac_state == baccarat_dealer_state.NO_MORE_BETS:
    mud.echo_around(me, None, f"{me} gestures and says, 'No more bets.'\r\n")
    me.bac_state = baccarat_dealer_state.PLAYER_FIRST
    pause = 30
  elif me.bac_state == baccarat_dealer_state.PLAYER_FIRST:
    if me.shoe.size < 6:
      commands.do_say(me, None, "Ladies and gentlemen, that was our final hand.  Thanks for playing!", None, mud, db)
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
      me.bac_state = baccarat_dealer_state.IDLE
      me.bac_paused = 0
      me.simulation_mode = False
      return
    me.hand = baccarat_hand()
    mud.echo_around(me, None, f"{me} deals {me.deal_next_card('player')} to the player.\r\n")
    me.bac_state = baccarat_dealer_state.BANKER_FIRST
    pause = 10
  elif me.bac_state == baccarat_dealer_state.BANKER_FIRST:
    mud.echo_around(me, None, f"{me} deals {me.deal_next_card('banker')} to the banker.\r\n")
    me.bac_state = baccarat_dealer_state.PLAYER_SECOND
    pause = 10
  elif me.bac_state == baccarat_dealer_state.PLAYER_SECOND:
    mud.echo_around(me, None, f"{me} deals {me.deal_next_card('player')} to the player.\r\n")
    me.bac_state = baccarat_dealer_state.BANKER_SECOND
    pause = 10
  elif me.bac_state == baccarat_dealer_state.BANKER_SECOND:
    mud.echo_around(me, None, f"{me} deals {me.deal_next_card('banker')} to the banker.\r\n")
    me.bac_state = baccarat_dealer_state.SHOW_INITIAL
    pause = 10
  elif me.bac_state == baccarat_dealer_state.SHOW_INITIAL:
    #mud.echo_around(me, None, me.hand.display() + "\n\n")
    commands.do_say(me, None, f"Player shows {me.hand.player_score()}. Banker shows {me.hand.banker_score()}.", None, mud, db)
    me.bac_state = baccarat_dealer_state.CHECK_NATURAL
    pause = 60
  elif me.bac_state == baccarat_dealer_state.CHECK_NATURAL:
    if me.hand.player_natural():
      commands.do_say(me, None, f"Player shows natural {me.hand.player_score()}.  No more draws.", None, mud, db)
      me.bac_state = baccarat_dealer_state.REPORT_WINNER
      pause = 30
    elif me.hand.banker_natural():
      commands.do_say(me, None, f"Banker shows natural {me.hand.banker_score()}.  No more draws.", None, mud, db)
      me.bac_state = baccarat_dealer_state.REPORT_WINNER
      pause = 30
    else:
      me.bac_state = baccarat_dealer_state.CHECK_PLAYER
      pause = 30
  elif me.bac_state == baccarat_dealer_state.CHECK_PLAYER:
    if me.check_player_third():
      commands.do_say(me, None, "Card for player.", None, mud, db)
      me.bac_state = baccarat_dealer_state.DEAL_PLAYER_THIRD
    else:
      commands.do_say(me, None, "Player stands.", None, mud, db)
      me.bac_state = baccarat_dealer_state.CHECK_BANKER
    pause = 10
  elif me.bac_state == baccarat_dealer_state.DEAL_PLAYER_THIRD:
    player_third = me.deal_next_card('player')
    mud.echo_around(me, None, "{} deals {} {} to the player.\r\n".format(
      me, string_handling.ana(cards.card_rank(player_third.rank).name), player_third))
    me.bac_state = baccarat_dealer_state.UPDATE_PLAYER_THIRD
    pause = 10
  elif me.bac_state == baccarat_dealer_state.UPDATE_PLAYER_THIRD:
    #mud.echo_around(me, None, "\n" + me.hand.display() + "\r\n")
    me.bac_state = baccarat_dealer_state.CHECK_BANKER
    pause = 60
  elif me.bac_state == baccarat_dealer_state.CHECK_BANKER:
    if me.check_banker_third():
      commands.do_say(me, None, "Card for banker.", None, mud, db)
      me.bac_state = baccarat_dealer_state.DEAL_BANKER_THIRD
      pause = 10
    else:
      commands.do_say(me, None, "Banker stands.", None, mud, db)
      me.bac_state = baccarat_dealer_state.REPORT_WINNER
      pause = 30
  elif me.bac_state == baccarat_dealer_state.DEAL_BANKER_THIRD:
    banker_third = me.deal_next_card('banker')
    mud.echo_around(me, None, "{} deals {} {} to the banker.\r\n".format(
      me, string_handling.ana(cards.card_rank(banker_third.rank).name), banker_third))
    me.bac_state = baccarat_dealer_state.UPDATE_BANKER_THIRD
    pause = 10
  elif me.bac_state == baccarat_dealer_state.UPDATE_BANKER_THIRD:
    #mud.echo_around(me, None, "\n" + me.hand.display() + "\r\n")
    me.bac_state = baccarat_dealer_state.REPORT_WINNER
    pause = 60
  elif me.bac_state == baccarat_dealer_state.REPORT_WINNER:
    if me.hand.panda():
      commands.do_say(me, None, panda_string, None, mud, db)
      me.shoe.report_history(history_entry.PANDA)
    elif me.hand.dragon():
      commands.do_say(me, None, dragon_string, None, mud, db)
      me.shoe.report_history(history_entry.DRAGON)
    elif me.hand.player_score() > me.hand.banker_score():
      commands.do_say(me, None, f"Player wins {me.hand.player_score()} over {me.hand.banker_score()}.", None, mud, db)
      me.shoe.report_history(history_entry.PLAYER_WIN)
    elif me.hand.player_score() < me.hand.banker_score():
      commands.do_say(me, None, f"Banker wins {me.hand.banker_score()} over {me.hand.player_score()}.", None, mud, db)
      me.shoe.report_history(history_entry.BANKER_WIN)
    else:
      commands.do_say(me, None, f"Player and banker tie!", None, mud, db)
      me.shoe.report_history(history_entry.TIE)
    # Check Michael's Side Bets
    if me.hand.three_card_9_8():
      me.shoe.report_extra(extra_side_bet.THREE_CARD_9_8)
    if me.hand.natural_9_8():
      me.shoe.report_extra(extra_side_bet.NATURAL_9_8)
    if me.hand.any_8_7():
      me.shoe.report_extra(extra_side_bet.ANY_8_7)
    me.hand = None
    me.bac_state = baccarat_dealer_state.CLEAR_CARDS
    pause = 60
  elif me.bac_state == baccarat_dealer_state.CLEAR_CARDS:
    mud.echo_around(me, None, f"{me} clears the cards from the table.\n")
    me.bac_state = baccarat_dealer_state.LAST_CALL_BETS
    pause = 120

  if pause != 0 and not me.simulation_mode:
    me.bac_paused = pause
 
  return
  