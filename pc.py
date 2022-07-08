import collections
import dataclasses
import logging
import copy
import config
import gc
import object
import string_handling
import structs

class character:
  #Creates a new char(acter) which can act within the world.
  def __init__(self):
    self.entity     = structs.entity()
    self._inventory = object.inventory()

  # Getters
  @property
  def ldesc(self):
    return self.entity.ldesc
  @property
  def room(self):
    return self.entity.room
  @property
  def inventory(self):
    return self._inventory
  @property
  def name(self):
    return self.entity.name
  
  # Setters
  @name.setter
  def name(self, new_name):
    self.entity.name = new_name
  @room.setter
  def room(self, new_room):
    self.entity.room = new_room
  @inventory.setter
  def inventory(self, new_inv):
    self._inventory = new_inv

  def write(self, message):
    logging.warning(f"Attempting to send message {message} to non-PC character {self.entity.name}")
    return

  def __str__(self):
    return self.name

class pc(character):
  """Creates a new PC (playable character).
     d      = descriptor controlling the character
     pwd    = password used to log in
     title  = what the player calls themself
     id     = unique player ID
     prefs  = player preferences such as screen height, width, etc."""
  def __init__(self):
    super().__init__()
    self._d = None
    self._pwd = "password"
    self._title = config.DEFAULT_TITLE
    self._id = None
    self._prefs = structs.preferences()

  # Getters
  @property
  def d(self):
    return self._d
  @property
  def pwd(self):
  	return self._pwd
  @property
  def title(self):
  	return self._title
  @property
  def id(self):
    return self._id
  @property
  def prefs(self):
    return self._prefs

  @property
  def ldesc(self):
    out_str = f"{self} {self.title}"
    if self.d == None:
      out_str += " (linkless)"
    out_str += " is here."
    return out_str
  
  # Setters
  @d.setter
  def d(self, new_d):
  	self._d = new_d
  @pwd.setter
  def pwd(self, new_pwd):
  	self._pwd = new_pwd
  @title.setter
  def title(self, new_title):
  	self._title = new_title
  @id.setter
  def id(self, new_id):
    self._id = new_id

  def update_pref(self, attr_str, new_val):
    if hasattr(self._prefs, attr_str):
      setattr(self._prefs, attr_str, new_val)
    else:
      logging.warning(f"{self.name} attempting to set non-existent attribute {attr_str} to {new_val}.")

  def save_char(self):
    file_name = config.PFILES_PATH + self.name.lower() + ".plr"

    with open(file_name, "w") as wf:
      wf.write(f"name: {self.name}\r\n".format(self.name))
      wf.write(f"id: {self.id}\r\n")
      wf.write(f"password: {self.pwd}\r\n")
      wf.write(f"title: {self.title}\r\n")
      wf.write(f"room: {self.room}\r\n")
      wf.write(f"brief: {self.prefs.brief_mode}\r\n")
      wf.write(f"active: {self.prefs.active_idle}\r\n")
      wf.write(f"width: {self.prefs.screen_width}\r\n")
      wf.write(f"length: {self.prefs.screen_length}\r\n")
      wf.write(f"color: {self.prefs.color_mode}\r\n")

  def write(self, message):
    if self._d != None:
      self._d.write(message)

class npc(character):
  """Creates a new NPC (non-playable character).
     vnum = virtual number of npc or None
     spec = list of special procedure functions which define mob behaviour

     TODO: document spec functions here"""
  def __init__(self, new_vnum = None, new_spec = None):
    super().__init__()
    self._vnum = new_vnum
    if new_spec != None:
      self._spec = new_spec
    else:
      self._spec = [ ]

  # Upgrades a character to an NPC
  @classmethod
  def from_char(cls, ch):
    ret_val = cls()

    ret_val.entity = ch.entity
    ret_val.inventory = ch.inventory

    return ret_val

  # Getters
  @property
  def vnum(self):
    return self._vnum
  @property
  def spec(self):
    return self._spec

  # Setters
  @vnum.setter
  def vnum(self, new_vnum):
    self._vnum = new_vnum

  @spec.setter
  def spec(self, new_spec):
    self._spec = new_spec

  def write(self, message):
    # process speech triggers?
    pass

  def call_spec_procs(self, mud, ch, command, argument):
    handled_command = False

    for func in self.spec:
      if func(mud, self, ch, command, argument):
        handled_command = True

    return handled_command

if __name__ == '__main__':
  ch1 = character()
  print(type(ch1))

  ch2 = npc.from_char(ch1)
  print(type(ch2))


