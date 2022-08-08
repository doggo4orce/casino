class card:
  def __init__(self, suit, rank):
    self._suit = suit
    self._rank = rank

class baccarat_card(card):
  def __init__(self, suit, rank):
    super().__init__(suit, rank)

  @property
  def value(self):
    if int(self.suit) in range(1, 11):
      return int(self.suit)
    else:
      return 10

class shoe:
  def __init__(self):
    self._contents = collections.deque()

  def add_top(self, new_card):
    self._contents.appendleft(new_card)

  def add_bottom(self, new_card):
    self._contents.append(new_card)

  def absorb_top(self, other):
    self._contents, other._contents = other._contents, self._contents
    self.absorb_bottom(other)

  def absorb_bottom(self, other):
    self._contents.extend(other._contents)
    other.clear()

class baccarat_shoe(shoe):
  def __init__(self):
    super().__init__()

  def add_top(self, new_card):
    if not isinstance(new_card, baccarat_card):
      print(f"Error: Trying to insert {type(new_card)} into {type(self)}.")
    else:
      super().add_top(new_card)

  def add_bottom(self, new_card):
    if not isinstance(new_card, baccarat_card):
      print(f"Error: Trying to insert {type(new_card)} into baccarat shoe.")
    else:
      super().add_bottom(new_card)

  def absorb_top(self, other):
    if not isinstance(other, baccarat_shoe):
      print(f"Error: Trying to absorb {type(other)} into top of {type(self)}.")
    else:
      self._contents, other._contents = other._contents, self._contents
      self.absorb_bottom(other)

  def absorb_bottom(self, other):
    if not isinstance(other, baccarat_shoe):
      print(f"Error: Trying to absorb {type(other)} into bottom of {type(self)}.")
    else:
      self._contents.extend(other._contents)
      other.clear()