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
    name      = characters name (wrapped from entity)
    Name      = characters name capitalized
    desc      = characters description as a buffer (wrapped from entity)
    ldec      = how character is listed in a room to others (wrapped from entity)
    room      = what room character is in (wrapped from entity)
    namelist  = list of aliases for character to be accessed by (wrapped from entity)
    inventory = iterable container consisting of all objects held (see object.py)

    Note: This class is meant to encapsulate the functionality shared by pcs/npcs,
    so that they need not be distinguished between throughout this codebase.  While
    there is nothing stopping one from instantiating it directly, such use is not intended."""
  def __init__(self):
    self.entity    = structs.entity_data()
    self.name = "an unfinished character"
    self.desc = editor.buffer("This character looks unfinished.")
    self.ldesc = "An unfinished character is here."
    self.room = structs.unique_identifier.from_string(config.VOID_ROOM)
    self.namelist = ["unfinished", "character"]
    self.inventory = inventory.inventory()

  # Getters
  @property
  def entity(self):
    return self._entity
  @property
  def name(self):
    return self.entity.name
  @property
  def Name(self):
    return self.entity.Name
  @property
  def desc(self):
    return self.entity.desc
  @property
  def ldesc(self):
    return self.entity.ldesc
  @property
  def room(self):
    return self.entity.room
  @property
  def namelist(self):
    return self.entity.namelist
  @property
  def inventory(self):
    return self._inventory

  # Setters
  @entity.setter
  def entity(self, new_ent):
    self._entity = new_ent
  @name.setter
  def name(self, new_name):
    self._entity.name = new_name
  @desc.setter
  def desc(self, new_desc):
    self.entity.desc = new_desc
  @ldesc.setter
  def ldesc(self, new_ldesc):
    self.entity.ldesc = new_ldesc
  @room.setter
  def room(self, new_room):
    self.entity.room = new_room
  @namelist.setter
  def namelist(self, new_namelist):
    self.entity.namelist = new_namelist
  @inventory.setter
  def inventory(self, new_inventory):
    self._inventory = new_inventory

  """write(message)   <-- no operation, should be over-written by derived classes
     in_zone()        <-- return zone_id of character's location
     has_alias(alias) <-- check if alias is in self.namelist
     debug()          <-- display state in readable string"""

  def write(self, message):
    logging.warning(f"Attempting to send message {message} to character {self.entity.name}")
    return

  def in_zone(self):
    if self.room == None:
      return None
    return self.room.zone_id

  def has_alias(self, alias):
    return self._entity.has_alias(alias)

  def debug(self):
    ret_val = self.entity.debug()
    ret_val += f"Type: {type(self)}\r\n"
    return ret_val

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
  # As soon as this property is written, the call to super().__init__() above
  # tries to access this specific property.  since no new setter has been written
  # it raises an AttributeError.  so this function should be deleted and this
  # linkless business should be handled elsewhere, good night! (oct 7, 23)
  @property
  def ldesc(self):
    out_str = f"{self.Name} {self.title}"
    if self.d == None:
      out_str += " (linkless)"
    out_str += " is here."
    return out_str
  @property
  def save_data(self):
    return self._save_data

  # preference property shortcuts
  @property
  def numeric_prefs(self):
    return self._prefs.numeric
  @property
  def text_prefs(self):
    return self._prefs.text
  @property
  def flag_prefs(self):
    return self._prefs.flags

  # preference setter shortcuts
  @flag_prefs.setter
  def flag_prefs(self, new_flag_prefs):
    self._prefs.flags = new_flag_prefs

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
  def screen_width(self):
    return self.numeric_prefs.screen_width
  @property
  def screen_length(self):
    return self.numeric_prefs.screen_length

  # text prefs properties
  @property
  def color_mode(self):
    return self.text_prefs.color_mode
  

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
  @ldesc.setter
  def ldesc(self, new_ldesc):
    # I think it's stupid that just writing
    #       super().ldesc = new_ldesc
    # doesn't work
    super(pc, self.__class__).ldesc.fset(self, new_ldesc)

  """update_pref(str, val) <- updates preference with name str to val (see do_prefs in commands.py)
     save_char(db)         <- saves character to database
     write(msg)            <- sends msg to descriptor controlling self"""

  def update_pref(self, attr_str, new_val):
    if hasattr(self._prefs, attr_str):
      setattr(self._prefs, attr_str, new_val)
    else:
      logging.warning(f"{self.name} attempting to set non-existent attribute {attr_str} to {new_val}.")

  def save_char(self, db):
    db.save_player(self)
    db.save_prefs(self)

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
    self.name = "an unfinished npc"
    self.desc = editor.buffer("This npc looks unfinished.")
    self.ldesc = "An unfinished npc is here."
    self.entity.namelist = ["unfinished", "npc"]
    self.prefix_command_triggers = list()
    self.suffix_command_triggers = list()
    self.heart_beat_procs = list()

    if proto != None:
      self.entity = dataclasses.replace(proto.entity)
      self.ldesc = proto.ldesc
      #TODO: write npc.assign_spec_proc function and use it to copy list manually here
      self.prefix_command_triggers = proto.prefix_command_triggers.copy()
      self.suffix_command_triggers = proto.suffix_command_triggers.copy()
      self.heart_beat_procs = proto.heart_beat_procs.copy()

  # Getters
  @property
  def entity(self):
    return self._entity
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
  @entity.setter
  def entity(self, new_entity):
    self._entity = new_entity
  @prefix_command_triggers.setter
  def prefix_command_triggers(self, new_triggers):
    self._prefix_command_triggers = new_triggers
  @suffix_command_triggers.setter
  def suffix_command_triggers(self, new_triggers):
    self._suffix_command_triggers = new_triggers
  @heart_beat_procs.setter
  def heart_beat_procs(self, new_procs):
    self._heart_beat_procs = new_procs

  """from_char(ch)                                       <- upgrades character ch to npc
     write(msg)                                          <- does nothing (see below)
     assign_spec_proc(new_proc)                          <- adds new_proc to self.specs
     call_prefix_command_triggers(mud, ch, cmd, arg, db) <- calls all prefix command trigger procs
     call_suffix_command_triggers(mud, ch, cmd, arg, db) <- calls all suffix command trigger procs
     call_heart_beat_procs(mud, db)                      <- calls all heart beat procs"""
     
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

  def debug(self):
    ret_val = super().debug()

    #TODO: factor this code out into entity (see below)
    #because it also appears in object.debug()
    ret_val += "Prefix Procs:\r\n"

    for spec in self.prefix_command_triggers:
      ret_val += f"  {spec.name}\r\n"
    
    ret_val += "Suffix Procs:\r\n"

    for spec in self.suffix_command_triggers:
      ret_val += f"  {spec.name}\r\n"

    ret_val += "Heartbeat Procs:\r\n"
    
    for spec in self.heart_beat_procs:
      ret_val += f"  {spec.name}\r\n"

    return ret_val

  #TODO: factor this code out of entity, so it doesn't get repeated in the object class
  def call_prefix_command_triggers(self, mud, ch, command, argument, db):
    block_interpreter = False
    for procedure in self.prefix_command_triggers:
      if procedure.call(mud, self, ch, command, argument, db) == spec_procs.prefix_command_trigger_messages.BLOCK_INTERPRETER:
        block_interpreter = True
    return block_interpreter

  def call_suffix_command_triggers(self, mud, ch, command, argument, db):
    for procedure in self.suffix_command_triggers:
      procedure.call(mud, self, ch, command, argument, db)

  def call_heart_beat_procs(self, mud, db):
    for procedure in self.heart_beat_procs:
      procedure.call(mud, self, db)

