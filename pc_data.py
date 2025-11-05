from color import *
import character_data
import collections
import mudlog
import copy
import config
import editor
import entity_data
import gc
import inventory_data
import object_data
import pc_save_data
import pref_data
import spec_proc_data
import string_handling

class pc_data(character_data.character_data):
  """Creates a new PC (playable character).
     descriptor  = descriptor controlling the character
     password    = password used to log in
     player_id   = unique player ID
     preferences = player preferences such as screen height, width, etc.
     save_data   = game data that is saved to player files
     title       = player's chosen title"""
  def __init__(self):
    super().__init__()
    self.descriptor = None
    self.password = None
    self.player_id = None
    self.preferences = pref_data.preferences_data()
    self.save_data = pc_save_data.pc_save_data()
    self.title = None

  # preference property shortcuts
  @property
  def numeric_prefs(self):
    return self.preferences.numeric
  @property
  def text_prefs(self):
    return self.preferences.text
  @property
  def flag_prefs(self):
    return self.preferences.flags

  # flag prefs properties
  @property
  def active_idle(self):
    return self.flag_prefs.active_idle
  @property
  def brief_mode(self):
    return self.flag_prefs.brief_mode
  @property
  def debug_mode(self):
    return self.flag_prefs.debug_mode

  # numeric prefs properties
  @property
  def page_width(self):
    return self.numeric_prefs.page_width
  @property
  def page_length(self):
    return self.numeric_prefs.page_length

  # text prefs properties
  @property
  def color_mode(self):
    return self.text_prefs.color_mode

  """set_pref(str, val) <- updates preference with name str to val (see do_prefs in commands.py)
     save_char(db)      <- saves character to database
     write(msg)         <- sends msg to descriptor controlling self"""

  def set_pref(self, attr_str, new_val):
    self.preferences.set(attr_str, new_val)

  def save_char(self, db):
    db.save_player(self)
    db.save_preferences(self)

  def write(self, message):
    if self.descriptor != None:
      self.descriptor.write(message)

  def debug(self):
    ret_val = super().debug() + "\r\n"
    ret_val += f"Descriptor: {CYAN}{self.descriptor}{NORMAL}\r\n"
    ret_val += f"Id: {CYAN}{self.player_id}{NORMAL}\r\n"
    ret_val += self.numeric_prefs.debug()
    ret_val += self.text_prefs.debug()
    ret_val += self.flag_prefs.debug()
    return ret_val