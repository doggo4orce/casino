import enum

class olc_mode(enum.IntEnum):
  OLC_MODE_ZEDIT = 0
  OLC_MODE_REDIT = 1

class olc_data:
  """Interface for descriptor to work with their OLC data
     mode      = eg. OLC_MODE_ZEDIT or OLC_MODE_REDIT
     state     = eg. REDIT_EDIT_NAME or REDIT_MAIN_MENU
     changes   = flag to check if changes have been made
     save_data = eg. a redit_save_data or zedit_save_data object"""
  def __init__(self):
    self.mode       =None
    self.state      =None
    self.changes    =False
    self.save_data  =None

  @property
  def mode(self):
    return self._mode
  @property
  def state(self):
    return self._state
  @property
  def changes(self):
    return self._changes
  @property
  def save_data(self):
    return self._save_data

  @mode.setter
  def mode(self, new_mode):
    self._mode = new_mode
  @state.setter
  def state(self, new_state):
    self._state = new_state
  @changes.setter
  def changes(self, new_changes):
    self._changes = new_changes
  @save_data.setter
  def save_data(self, new_save_data):
    self._save_data = new_save_data
