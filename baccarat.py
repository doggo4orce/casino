import cards
import commands
import enum
import event
import logging
import pc

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

  def __len__(self):
    return len(self.player) + len(self.banker)

  def __str__(self):
    ret_val = f"Banker has {len(self.banker)} cards:\n"
    for card in self.banker:
      ret_val += f"{card}\n"
    ret_val += f"Player has {len(self.player)} cards.\n"
    for card in self.player:
      ret_val += f"{card}\n"
    return ret_val

def baccarat_deck():
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

def baccarat_shoe(num_decks):
  shoe = cards.shoe()

  for j in range(0, num_decks):
  	shoe.absorb_bottom(baccarat_deck())

  return shoe

class baccarat_dealer_state(enum.IntEnum):
  IDLE          = 1
  BEGIN_SHOE    = 2
  SHUFFLE_SHOE  = 3
  FIRST_DRAW    = 4
  BURN_CARDS    = 5
  DEAL_HAND     = 6
  SHOW_INITIAL  = 7
  CHECK_NATURAL = 8
  CHECK_PLAYER  = 9
  CHECK_BANKER  = 10
  REPORT_WINNER = 11

class baccarat_dealer_report(enum.IntEnum):
  CARD_PLAYER    = 1
  CARD_BANKER    = 2
  PLAYER_NATURAL = 3
  BANKER_NATURAL = 4
  PLAYER_WIN     = 5
  BANKER_WIN     = 6
  TIE            = 7
  PANDA          = 8
  DRAGON         = 9

class baccarat_dealer(cards.card_dealer):
  def __init__(self):
    """Creates a baccarat dealer
     state = keep track of what dealer will do next, FIRST_DRAW etc.
     working = True when dealer's next step has been initiated"""
    super().__init__()
    self._hand = None
    self._state = baccarat_dealer_state.IDLE
    self._initial_card_val = None

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

  @classmethod
  def from_card_dealer(cls, dealer):
    ret_val = cls()
    # copy character attributes
    ret_val.entity = dealer.entity
    ret_val.inventory = dealer.inventory
    # copy npc attributes
    ret_val.vnum = dealer.vnum
    ret_val.spec = dealer.spec
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
    if banker_score == 3:
      return player_third != 8
    if banker_score == 4:
      return player_third in {2,3,4,5,6,7}
    if banker_score == 5:
      return player_third in {4,5,6,7}
    if banker_score == 6:
      return player_third in {6,7}
    return False

# event function to toggle the working flag for dealer
def dealer_ready(ch, mud):
  ch.paused = False

# special procedures for baccarat dealer
def baccarat_dealer_intro(mud, me, ch, command, argument):
  if ch == None:
    return

  if not isinstance(me, baccarat_dealer):
    logging.warning(f"Attempting to call inappropriate spec proc 'baccarat_dealer_intro' on npc {me}.")
    return False

  if command == "say" and argument.lower() == "hi":
    mud.events.add_event(event.speech_event(me, "Hey, wanna play some Baccarat?  Type 'baccarat' for more information.", None, 10))
    return False
  
  help_str  = "Baccarat Commands:\n"
  help_str += "  baccarat start - begin a baccarat shoe (no commitment)"
  
  if command == "baccarat":
    if argument.lower() == "start":
      if me.state != baccarat_dealer_state.IDLE:
        commands.do_say(me, None, "Excuse me, there is already a game in progress.", None, mud)
        return True

      commands.do_say(me, None, "OK, I'm starting a shoe.  Don't try to interact with me until it's over!", None, mud)
      me.state = baccarat_dealer_state.BEGIN_SHOE
    else:
      ch.write(help_str)
    return True

def baccarat_dealing(mud, me, ch, command, argument):
  if ch != None:
    return False

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
    me.shoe = baccarat_shoe(1)
    mud.echo_around(me, None, f"{me} assembles a new shoe consisting of 1 decks.\n")
    me.state = baccarat_dealer_state.SHUFFLE_SHOE
    pause = 10
  elif me.state == baccarat_dealer_state.SHUFFLE_SHOE:
    me.shuffle()
    mud.echo_around(me, None, f"{me} shuffles the shoe.\n")
    me.state = baccarat_dealer_state.FIRST_DRAW
    pause = 10
  elif me.state == baccarat_dealer_state.FIRST_DRAW:
    first_card = me.draw()
    me.initial_card_val = first_card.value
    mud.echo_around(me, None, f"{me} draws and reveals the first card ({first_card}).\n")
    me.state = baccarat_dealer_state.BURN_CARDS
    pause = 10
  elif me.state == baccarat_dealer_state.BURN_CARDS:
    for j in range(0, me.initial_card_val):
      me.draw()
    mud.echo_around(me, None, f"{me} burns {me.initial_card_val} cards.\n")
    me.state = baccarat_dealer_state.DEAL_HAND
    pause = 10
  elif me.state == baccarat_dealer_state.DEAL_HAND:
    if me.shoe.size < 6:
      commands.do_say(me, None, "Ladies and gentlemen, that was our final hand.  Thanks for playing!\n")
      me.shoe = None
      me.state = baccarat_dealer_state.IDLE
      return

    me.hand = baccarat_hand()
    mud.echo_around(me, None, f"{me} deals ({me.deal_next_card('player')}) to the player.\n")
    mud.echo_around(me, None, f"{me} deals ({me.deal_next_card('banker')}) to the banker.\n")
    mud.echo_around(me, None, f"{me} deals ({me.deal_next_card('player')}) to the player.\n")
    mud.echo_around(me, None, f"{me} deals ({me.deal_next_card('banker')}) to the banker.\n")
    me.state = baccarat_dealer_state.SHOW_INITIAL
    pause = 10
  elif me.state == baccarat_dealer_state.SHOW_INITIAL:
    commands.do_say(me, None, f"Player shows {me.hand.player_score()}. Banker shows {me.hand.banker_score()}.", None, mud)
    me.state = baccarat_dealer_state.CHECK_NATURAL
    pause = 10
  elif me.state == baccarat_dealer_state.CHECK_NATURAL:
    if me.hand.player_natural():
      commands.do_say(me, None, f"Player shows natural {me.hand.player_score()}.  No more cards.\n", None, mud)
      me.state = baccarat_dealer_state.REPORT_WINNER
      pause = 10
    elif me.hand.banker_natural():
      commands.do_say(me, None, f"Banker shows natural {me.hand.banker_score()}.  No more cards.\n", None, mud)
      me.state = baccarat_dealer_state.REPORT_WINNER
      pause = 10
    else:
      me.state = baccarat_dealer_state.CHECK_PLAYER
      pause = 10 # already paused before checking naturals
  elif me.state == baccarat_dealer_state.CHECK_PLAYER:
    if me.check_player_third():
      commands.do_say(me, None, "Card for player.", None, mud)
      mud.echo_around(me, None, f"{me} deals a card ({me.deal_next_card('player')}) to the player.\n")
    else:
      commands.do_say(me, None, "Player stands.", None, mud)
    me.state = baccarat_dealer_state.CHECK_BANKER
    pause = 10
  elif me.state == baccarat_dealer_state.CHECK_BANKER:
    if me.check_banker_third():
      commands.do_say(me, None, "Card for banker.", None, mud)
      mud.echo_around(me, None, f"{me} deals a card ({me.deal_next_card('banker')}) to the banker.\n")
    else:
      commands.do_say(me, None, "Banker stands.", None, mud)
    me.state = baccarat_dealer_state.REPORT_WINNER
    pause = 10
  elif me.state == baccarat_dealer_state.REPORT_WINNER:
    if me.hand.player_score() > me.hand.banker_score():
      commands.do_say(me, None, f"Player wins {me.hand.player_score()} over {me.hand.banker_score()}.", None, mud)
    elif me.hand.player_score() < me.hand.banker_score():
      commands.do_say(me, None, f"Banker wins {me.hand.banker_score()} over {me.hand.player_score()}.", None, mud)
    else:
      commands.do_say(me, None, f"Player and banker tie!\n", None, mud)
    me.hand = None
    me.state = baccarat_dealer_state.DEAL_HAND
    pause = 60

  if pause != 0:
    mud.events.add_event(event.event(me, dealer_ready, None, pause))


if __name__ == '__main__':
  the_shoe = baccarat_shoe(1)
  the_dealer = baccarat_dealer()
  the_dealer.entity.name = "the dealer"

  print(f"{the_dealer} assembles a new shoe.\n")
  the_dealer.shoe = the_shoe
  the_dealer.state = baccarat_dealer_state.SHUFFLE_SHOE

  print(f"{the_dealer} shuffles the shoe.\n")
  the_dealer.shuffle()
  the_dealer.state = baccarat_dealer_state.FIRST_DRAW

  print(f"{the_dealer} draws and reveals the first card.\n")
  first_card = the_dealer.draw()
  print(f"A {first_card} is drawn.\n")
  the_dealer.initial_card_val = first_card.value
  the_dealer.state = baccarat_dealer_state.BURN_CARDS

  for j in range(0, the_dealer.initial_card_val):
    print(f"{the_dealer} burns a card.")
    the_dealer.draw() # discard return value
  print("")
  the_dealer.state = baccarat_dealer_state.DEAL_HAND

  print(f"{the_dealer} deals a card ({the_dealer.deal_next_card('player')}) to the player.")
  print(f"{the_dealer} deals a card ({the_dealer.deal_next_card('banker')}) to the banker.")
  print(f"{the_dealer} deals a card ({the_dealer.deal_next_card('player')}) to the player.")
  print(f"{the_dealer} deals a card ({the_dealer.deal_next_card('banker')}) to the banker.\n")
  the_dealer.state = baccarat_dealer_state.SHOW_INITIAL

  print("Score:")
  print(f"Player: {the_dealer.hand.player_score()}.")
  print(f"Banker: {the_dealer.hand.banker_score()}.\n")
  the_dealer.state = baccarat_dealer_state.CHECK_NATURAL

  if the_dealer.hand.player_natural():
    print(f"Player shows natural {the_dealer.hand.player_score()}.  No more cards.")
    the_dealer.state = baccarat_dealer_state.REPORT_WINNER
    exit()
  elif the_dealer.hand.banker_natural():
    print(f"Banker shows natural {the_dealer.hand.banker_score()}.  No more cards.")
    the_dealer.state = baccarat_dealer_state.REPORT_WINNER
    exit()
  the_dealer.state = baccarat_dealer_state.CHECK_PLAYER

  if the_dealer.check_player_third():
    print("Card for player.")
    print(f"{the_dealer} deals a card ({the_dealer.deal_next_card('player')}) to the player.\n")
  else:
    print("Player stands.")
  the_dealer.state = baccarat_dealer_state.CHECK_BANKER

  if the_dealer.check_banker_third():
    print("Card for banker.")
    print(f"{the_dealer} deals a card ({the_dealer.deal_next_card('banker')}) to the banker.\n")
  else:
    print("Banker stands.")
  the_dealer.state = baccarat_dealer_state.REPORT_WINNER




