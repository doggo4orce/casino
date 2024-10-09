import dataclasses

@dataclasses.dataclass
class pc_save_data_numerical:
  hp: int=None

@dataclasses.dataclass
class pc_save_data_strings:
  title: str=None

class pc_save_data:
  """Creates pc_save_data object that stores all of the player data that is saved
     to the database.  Any new fields added to the preceding dataclasses should
     automatically be saved.
     numerical = all of the numerical data (eg. hp, mana)
     text = all of the text data (eg. title, religion)"""
  def __init__(self):
    self.numerical = pc_save_data_numerical()
    self.text = pc_save_data_strings()

  @property
  def hp(self):
    return self.numerical.hp
  @property
  def title(self):
    return self.text.title

  @hp.setter
  def hp(self, new_hp):
    self.numerical.hp = new_hp
  @title.setter
  def title(self, new_title):
    self.text.title = new_title