import collections
import dataclasses
import logging
import copy
import config
import editor
import gc
import inventory
import object
import spec_procs
import string_handling
import structs

class character:
  """Creates a new char(acter) which can act within the world.

    entity    = dataclass encapsulating name, appearance and location (see structs.py)
    inventory = iterable container consisting of all objects held (see object.py)

    Note: This class is meant to encapsulate the functionality shared by pcs/npcs,
    so that they need not be distinguished between throughout this codebase.  While
    there is nothing stopping one from instantiating it directly, such use is not intended."""
  def __init__(self):
    self._entity    = structs.entity_data()
    self._inventory = inventory.inventory()

  # Getters
  @property
  def entity(self):
    return self._entity
  @property
  def name(self):
    return self._entity.name
  @property
  def Name(self):
    return self._entity.Name
  @property
  def room(self):
    return self._entity.room
  @property
  def inventory(self):
    return self._inventory
  @property
  def ldesc(self):
    return "This character's ldesc should never be seen!"
  
  # Setters
  @entity.setter
  def entity(self, new_ent):
    self._entity = new_ent
  @name.setter
  def name(self, new_name):
    self._entity.name = new_name
  @room.setter
  def room(self, new_room):
    self._entity.room = new_room
  @inventory.setter
  def inventory(self, new_inv):
    self._inventory = new_inv

  # This function should never be called.  It should be overridden by any derived classes.
  def write(self, message):
    logging.warning(f"Attempting to send message {message} to character {self.entity.name}")
    return

  """in_zone()        <-- returns zone_id of the zone that character is occupying
     has_alias(alias) <-- returns True if alias is once of the characters key-words"""
  def in_zone(self):
    if self.room == None:
      return None
    return self.room.zone_id

  def has_alias(self, alias):
    return self._entity.has_alias(alias)

  def __str__(self):
    return self.name

class pc(character):
  """Creates a new PC (playable character).
     d         = descriptor controlling the character
     pwd       = password used to log in
     title     = what the player calls themself
     id        = unique player ID
     prefs     = player preferences such as screen height, width, etc. (structs.py)
     save_data = game data that is saved to player files               (structs.py)"""
  def __init__(self):
    super().__init__()
    self._d = None
    self._pwd = "password"
    self._title = config.DEFAULT_TITLE
    self._id = None
    self._prefs = structs.preferences()
    self._save_data = structs.pc_save_data()

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
  @property
  def save_data(self):
    return self._save_data
  
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
  @save_data.setter
  def save_data(self, new_data):
    self._save_data = new_data

  """parse_tag(tag, value, rf) <- processes a line from a pfile through rf
     update_pref(str, val) <- updates preference with name str to val (see do_prefs in commands.py)
     save_char()           <- saves character data to player file
     write(msg)            <- sends msg to descriptor controlling self"""

  def parse_tag(self, tag, value, rf):
    # Load Administrative Data
    if tag == "name":
      self.name = value
      self.entity.namelist = [value]
    elif tag == "id":
      self.id = value
    elif tag == "password":
      self.pwd = value
    # Load Entity Data (not all of these will have been saved, but any of them are allowed to be)
    elif tag == "room":
      # room counts as entity data, but it needs to be parsed separately
      self.entity.room = structs.unique_identifier.from_string(value)
    elif tag == "desc":
      self.desc = editor.buffer()
      line = ""
      while line != "~\n":
        line = rf.readline()
        if line != "~\n":
          self.desc.add_line(line)
    elif hasattr(self.entity, tag):
      setattr(self.entity, tag, value)
    # Load Game Data
    elif hasattr(self.save_data.numerical, tag):
      setattr(self.save_data.numerical, tag, int(value))
    elif hasattr(self.save_data.non_numerical, tag):
      setattr(self.save_data.non_numerical, tag, value)
    # Load Preferences
    elif hasattr(self.prefs, tag):
      if tag in ['screen_width', 'screen_length']:
        setattr(self.prefs, tag, int(value))
      else:
        setattr(self.prefs, tag, value)
    else:
      # TODO: replace this with exception?
      logging.warning(f"Line ({line_number}) -- Trying to assign value to unrecognized tag {tag} while loading {rf.name}.")

  def update_pref(self, attr_str, new_val):
    if hasattr(self._prefs, attr_str):
      setattr(self._prefs, attr_str, new_val)
    else:
      logging.warning(f"{self.name} attempting to set non-existent attribute {attr_str} to {new_val}.")

  def save_char(self):
    file_name = config.PFILES_PATH + self.name.lower() + ".plr"
    with open(file_name, "w") as wf:
      wf.write("# Administrative Data\n")

      wf.write(f"name: {self.name}\n".format(self.name))
      wf.write(f"id: {self.id}\n")
      wf.write(f"password: {self.pwd}\n")

      wf.write("\n# Game Data\n")

      for field in self.save_data.non_numerical.__dataclass_fields__:
        wf.write(f"{field}: {getattr(self._save_data.non_numerical, field)}\n")

      for field in self.save_data.numerical.__dataclass_fields__:
        wf.write(f"{field}: {getattr(self._save_data.numerical, field)}\n")

      wf.write(f"room: {str(self.room)}\n")

      wf.write("\n# Preferences\n")
      self.save_prefs(wf)

  def save_prefs(self, file_stream):
    for field in self.prefs.__dataclass_fields__:
      file_stream.write(f"{field}: {getattr(self.prefs, field)}\n")

  def write(self, message):
    if self._d != None:
      self._d.write(message)

class npc(character):
  """Creates a new NPC (non-playable character).
     ldesc = one line description shown after room description
     prefix_command_triggers = procs called before command is processed
     suffix_command_triggers = procs called after command is processed
     heart_beat_procs = list of pulsing special procedures"""
  def __init__(self, proto=None):
    super().__init__()
    self._ldesc = "An unfinished npc stands here."
    self._prefix_command_triggers = list()
    self._suffix_command_triggers = list()
    self._heart_beat_procs = list()

    if proto != None:
      self.entity = dataclasses.replace(proto.entity)
      self._ldesc = proto.ldesc
      self._prefix_command_triggers = proto.prefix_command_triggers.copy()
      self._suffix_command_triggers = proto.suffix_command_triggers.copy()
      self._heart_beat_procs = proto.heart_beat_procs.copy()

  # Getters
  @property
  def ldesc(self):
    return self._ldesc
  @property
  def prefix_command_triggers(self):
    return self._prefix_command_triggers
  @property
  def suffix_command_triggers(self):
    return self._suffix_command_triggers
  @property
  def heart_beat_procs(self):
    return self._heart_beat_procs

  # Setters
  @ldesc.setter
  def ldesc(self, new_ldesc):
    self._ldesc = new_ldesc
  @prefix_command_triggers.setter
  def prefix_command_triggers(self, new_triggers):
    self._prefix_command_triggers = new_triggers
  @suffix_command_triggers.setter
  def suffix_command_triggers(self, new_triggers):
    self._suffix_command_triggers = new_triggers
  @heart_beat_procs.setter
  def heart_beat_procs(self, new_procs):
    self._heart_beat_procs = new_procs

  """from_char(ch)                                   <- upgrades character ch to npc
     write(msg)                                      <- does nothing (see below)
     assign_spec_proc(new_proc)                      <- adds new_proc to self.specs
     call_prefix_command_triggers(mud, ch, cmd, arg) <- calls all prefix command trigger procs
     call_suffix_command_triggers(mud, ch, cmd, arg) <- calls all suffix command trigger procs
     call_heart_beat_procs(mud)                      <- calls all heart beat procs"""
     
  @classmethod
  def from_char(cls, ch):
    ret_val = cls()
    ret_val.entity = ch.entity
    ret_val.ldesc = ch.ldesc
    ret_val.inventory = ch.inventory
    return ret_val

  """it's unclear what should be done with message, but since I'd like pcs and npcs
     to be as interchangeable as possible, this function ought to exist.

     Perhaps this function could:
       -process speech triggers (if such things were to be implemented), or
       -route the message to a player who is controlling the npc (eg. with a spell)?"""
  def write(self, message):
    pass

  def call_prefix_command_triggers(self, mud, ch, command, argument):
    block_interpreter = False
    for procedure in self.prefix_command_triggers:
      if procedure.call(mud, self, ch, command, argument) == spec_procs.prefix_command_trigger_messages.BLOCK_INTERPRETER:
        block_interpreter = True
    return block_interpreter

  def call_suffix_command_triggers(self, mud, ch, command, argument):
    for procedure in self.suffix_command_triggers:
      procedure.call(mud, self, ch, command, argument)

  def call_heart_beat_procs(self, mud):
    for procedure in self.heart_beat_procs:
      procedure.call(mud, self)

