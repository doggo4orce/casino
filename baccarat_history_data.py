import enum

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

class baccarat_history_data():
  """Keeps track of a baccarat shoe in progress.
    history = outcomes from previous hands, e.g. player win, dragon
    extras  = occurances of side bet winnings, e.g. three card 9 over 8"""
  def __init__(self):
    self._history = list()
    self._extras = list()

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