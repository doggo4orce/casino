import config
import dataclasses
import mudlog

"""Abstract class to keep track of player preferences, the derived classes
   below consist of the different forms of preferences available.

   At the base level, we have only get and set, which act as getters and
   setters of the fields."""
class pref_data:
  def get(self, field):
    if hasattr(self, field):
      return getattr(self, field)
    else:
      mudlog.warning(f"Trying to access preference field {field} which is not defined.")

  def set(self, field, value):
    if hasattr(self, field):
      setattr(self, field, value)
    else:
      mudlog.warning(f"Trying to set {field} to {value}, but {field} is not defined.")

@dataclasses.dataclass
class pref_data_numeric(pref_data):
  """Derived pref_data class to store numeric preferences.
     screen_width = width that text should be formatted to
     screen_length = (not yet used) for formatting large output"""
  screen_width:  int = config.DEFAULT_SCREEN_WIDTH
  screen_length: int = config.DEFAULT_SCREEN_LENGTH

@dataclasses.dataclass
class pref_data_text(pref_data):
  """Derived pref_data class to store text preferences.
     color_mode = element of ['off', '16', or '256']"""
  color_mode: str = config.DEFAULT_COLOR_MODE

@dataclasses.dataclass
class pref_data_flags(pref_data):
  """Derived pref_data class to store boolean preferences.
     active_idle = send a periodic wake-up call to stop them from timing out
     brief_mode = suppress extra information when walking through rooms
     debug_mode = display extra information when looking at entities"""
  active_idle: bool=config.DEFAULT_ACTIVE_IDLE
  brief_mode: bool=config.DEFAULT_BRIEF_MODE
  debug_mode: bool=config.DEFAULT_DEBUG_MODE

  def set(self, field, val):
    if val not in [True, False]:
      mudlog.warning(f"set function called on {field} flag with value {val} which is neither True nor False.")
    else:
      super().set(field, val)

  def flip(self, field):
    if getattr(self, field) == True:
      setattr(self, field, False)
    elif getattr(self, field) == False:
      setattr(self, field, True)
    else:
      mudlog.warning(f"switch function called on {field}, which was neither on nor off, turning off.")
      setattr(self, field, False)