from color import *
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
      mudlog.warning(f"Trying to access non-existent {self.__class__.__name__}.{field}.")

  def set(self, field, value):
    if hasattr(self, field):
      setattr(self, field, value)
    else:
      mudlog.warning(f"Trying to set non-existent {self.__class__.__name__}.{field} to {value}.")

  def fields(self):
    return self.__dataclass_fields__

  def debug(self):
    ret_val = ""
    for field in self.fields():
      ret_val += f"{field}: {CYAN}{getattr(self, field)}{NORMAL}\r\n"
    return ret_val

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
  title:      str = config.DEFAULT_TITLE

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
      mudlog.warning(f"Trying to set pref_data_flags.{field} to {val}, which is neither True nor False.")
    else:
      super().set(field, val)

  def flip(self, field):
    if getattr(self, field) == True:
      setattr(self, field, False)
    elif getattr(self, field) == False:
      setattr(self, field, True)
    else:
      mudlog.warning(f"Trying to switch non-boolean pref_data_flags.{field}, turning off.")
      setattr(self, field, False)

  def flags_string(self):
    fields = self.__dataclass_fields__
    flags = [ field for field in fields if getattr(self, field)]
    return ' '.join(flags)

  def debug(self):
    return f"Pref Flags: {CYAN}{self.flags_string()}{NORMAL}\r\n"

class preferences_data:
  """Creates preferences_data object used to store various types of preferences,
     each stored in their own corresponding derived subclass of pref_data
     numeric = numeric preferences like screen_width and screen_length
     text    = text preferences like color_mode in ['off', '16, '256']
     flags   = boolean preferences like debug_mode or active_idle"""
  def __init__(self):
    self.numeric = pref_data_numeric()
    self.text = pref_data_text()
    self.flags = pref_data_flags()

  def get(self, field):
    if hasattr(self.numeric, field):
      return self.numeric.get(field)
    elif hasattr(self.text, field):
      return self.text.get(field)
    elif hasattr(self.flags, field):
      return self.flags.get(field)
    else:
      mudlog.warning(f"Trying to get preferences_data.{field} which is not defined.")

  def set(self, field, value):
    if hasattr(self.numeric, field):
      self.numeric.set(field, value)
    elif hasattr(self.text, field):
      self.text.set(field, value)
    elif hasattr(self.flags, field):
      self.flags.set(field, value)
    else:
      mudlog.warning(f"Trying to set non-existent preferences_data.{field} to {value}.")

  def flip(self, field):
    if hasattr(self.flags, field):
      self.flags.flip(field)
    else:
      mudlog.warning(f"Trying to flip non-existent preferences_data.{field}.")