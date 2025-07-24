import mudlog

class baccarat_hand_data:
  """Creates a single hand of baccarat.
     player = list of up to three cards used to compute player's score
     banker = same, but for banker"""
  def __init__(self):
    self._player = list()
    self._banker = list()

  def ascii_rep(self, cards, idx, row):
    if row not in range(0,5):
      mudlog.error(f"function {ascii_rep_banker} called with bad row {row}")
      return None
    try:
      return cards[idx].ascii_rep()[row]
    except IndexError:
      # maybe we're tryign to read 2nd or 3rd card but banker doesn't have that many
      return ' ' * 7

  def ascii_rep_player(self, idx, row):
    return self.ascii_rep(self._player, idx, row)

  def ascii_rep_banker(self, idx, row):
    return self.ascii_rep(self._banker, idx, row)

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

  def num_player_cards(self):
    return len(self._player)

  def num_banker_cards(self):
    return len(self._banker)

  def add_card(self, card, target):
    if target == "player":
      self._player.append(card)
    elif target == "banker":
      self._banker.append(card)
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
    return self.hand_value(self._player)

  def banker_score(self):
    return self.hand_value(self._banker)

  def player_natural(self):
    return self.player_score() in {8,9} and len(self._player) == 2

  def banker_natural(self):
    return self.banker_score() in {8,9} and len(self._banker) == 2

  def panda(self):
    if len(self._player) == 3 and self.player_score() > self.banker_score():
      return self.player_score() == 8
  
  def dragon(self):
    if len(self._banker) == 3 and self.player_score() < self.banker_score():
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
 
    n_p = len(self._player)
    n_b = len(self._banker)

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
        ret_val +=  self._player[j].ascii_rep()[i]
        if j < n_p - 1:
          ret_val += ' ' * SPACE_BETWEEN_PLAYER_CARDS
        else:
          ret_val += ' ' * SPACE_BETWEEN_PLAYER_BANKER

      # then banker cards
      for j in range(0, n_b):
        ret_val +=  self._banker[j].ascii_rep()[i]
        if j < n_p - 1:
          ret_val += ' ' * SPACE_BETWEEN_BANKER_CARDS

      ret_val += "\r\n"  
    
    return ret_val

  def __len__(self):
    return len(self._player) + len(self._banker)

  def __str__(self):
    ret_val = f"Banker has {len(self._banker)} cards:\r\n"
    for card in self.banker:
      ret_val += f"{card}\n"
    ret_val += f"Player has {len(self._player)} cards.\r\n"
    for card in self.player:
      ret_val += f"{card}\r\n"
    return ret_val