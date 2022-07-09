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
  """Creates a new char(acter) which can act within the world.
    entity = dataclass encapsulating name, appearance and location (see structs.py)
    inventory = iterable container consisting of all objects held (see object.py)

    Note: This class is meant to encapsulate the functionality shared by pcs/npcs,
    so that they need not be distinguished between throughout this codebase.  While
    there is nothing stopping one from instantiating it directly, such use is not intended."""
  def __init__(self):
    self._entity     = structs.entity()
    self._inventory = object.inventory()

  # Getters
  @property
  def entity(self):
    return self._entity
  @property
  def inventory(self):
    return self._inventory
  @property
  def ldesc(self):
    return self.entity.ldesc
  @property
  def room(self):
    return self.entity.room
  @property
  def name(self):
    return self.entity.name
  
  # Setters
  @entity.setter
  def entity(self, new_ent):
    self._entity = new_ent
  @inventory.setter
  def inventory(self, new_inv):
    self._inventory = new_inv
  @name.setter
  def name(self, new_name):
    self.entity.name = new_name
  @room.setter
  def room(self, new_room):
    self.entity.room = new_room

  # This function should never be called.  It should be overridden by any derived classes.
  def write(self, message):
    logging.warning(f"Attempting to send message {message} to character {self.entity.name}")
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

  """update_pref(str, val) <- updates preference with name str to val (see do_prefs in commands.py)
     save_char()           <- saves character data to player file
     write(msg)            <- sends msg to descriptor controlling self"""

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
     command_triggers = list of command triggered special procedures (see structs.py)
     heart_beat_procs = list of pulsing special procedures (see structs.py)"""
  def __init__(self, new_vnum = None):
    super().__init__()
    self._vnum = new_vnum
    self._command_triggers = list()
    self._heart_beat_procs = list()


  # Getters
  @property
  def vnum(self):
    return self._vnum
  @property
  def command_triggers(self):
    return self._command_triggers
  @property
  def heart_beat_procs(self):
    return self._heart_beat_procs

  # Setters
  @vnum.setter
  def vnum(self, new_vnum):
    self._vnum = new_vnum
  @command_triggers.setter
  def command_triggers(self, new_triggers):
    self._command_triggers = new_triggers
  @heart_beat_procs.setter
  def heart_beat_procs(self, new_procs):
    self._heart_beat_procs = new_procs

  """from_char(ch)                            <- returns an npc built from attributes of ch
     write(msg)                               <- does nothing (see below)
     assign_spec_proc(new_proc)               <- adds new_proc to self.specs
     call_command_triggers(mud, ch, cmd, arg) <- calls all command trigger spec procs
     call_heart_beat_procs(mud)               <- calls all heart beat procs"""
     
  @classmethod
  def from_char(cls, ch):
    ret_val = cls()
    ret_val.entity = ch.entity
    ret_val.inventory = ch.inventory
    return ret_val

  """it's unclear what should be done with message, but since I'd like pcs and npcs
     to be as interchangeable as possible, this function ought to exist.

     Perhaps this function could:
       -process speech triggers (if such things were to be implemented), or
       -route the message to a player who is controlling the npc (eg. with a spell)?"""
  def write(self, message):
    pass

  def assign_spec_proc(self, spec_proc):
    self.specs.append(spec_proc)

  def call_command_triggers(self, mud, ch, command, argument):
    block_interpreter = False
    for procedure in self.command_triggers:
      if procedure.func(mud, self, ch, command, argument) == structs.command_trigger_messages.BLOCK_INTERPRETER:
        block_interpreter = True
    return block_interpreter

  def call_heart_beat_procs(self, mud):
    for procedure in self.heart_beat_procs:
      features = procedure.func(mud, self)

