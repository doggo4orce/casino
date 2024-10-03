import behaviour_data
from color import *
import copy
import namelist_data
  
class entity_data:
  """Manages attributes common to characters and objects.
     name      = what to be referred to as
     namelist  = list of keywords to be targetted with (PRIVATE)
     ldesc     = what to see when the entity is in a room
     desc      = shown when closely examined
     TODO: room should be renamed to location, to be less misleading
     room      = reference to room if it is in one, and None otherwise
     behaviour = spec proc manager

     Additional Properties:
     Name      = same as name but capitalized
     in_zone   = zone_id of entity's location (if any)"""

  def __init__(self, proto=None):
    self.behaviour = behaviour_data.behaviour_data()

    if proto == None:
      self.name = "an unfinished entity"
      self._namelist = namelist_data.namelist_data("unfinished", "entity")
      self.ldesc = "An unfinished entity is here."
      self.desc = "This entity looks unfinished."
    else:
      self.name = proto.name
      self._namelist = namelist_data.namelist_data(*proto.aliases())
      self.ldesc = proto.ldesc
      self.desc = proto.desc
      self.behaviour = copy.deepcopy(proto.behaviour)

    self.room = None

  @property
  def name(self):
    return self._name
  @property
  def ldesc(self):
    return self._ldesc
  @property
  def desc(self):
    return self._desc
  @property
  def behaviour(self):
    return self._behaviour
  @property
  def room(self):
    return self._room

  @name.setter
  def name(self, new_name):
    self._name = new_name
  @ldesc.setter
  def ldesc(self, new_ldesc):
    self._ldesc = new_ldesc
  @desc.setter
  def desc(self, new_desc):
    self._desc = new_desc
  @behaviour.setter
  def behaviour(self, new_behaviour):
    self._behaviour = new_behaviour
  @room.setter
  def room(self, new_room):
    self._room = new_room

  @property
  def Name(self):
    return self.name.capitalize()

  @property
  def in_zone(self):
    if self.room == None:
      return None
    return self.room.zone_id

  """Wrapped to namelist:

     add_alias(alias)        <- adds a new alias to namelist
     has_alias(alias)        <- check namelist for alias
     num_aliases             <- count aliases in namelist
     remove_aliases(alias)   <- remove alias from namelist
     remove_all_aliases()    <- remove all aliases
     reset_aliases(*aliases) <- start fresh with new aliases
     aliases()               <- returns copy of aliases as list"""

  def add_alias(self, alias):
    self._namelist.add_alias(alias)
      
  def has_alias(self, alias):
    return self._namelist.has_alias(alias)

  @property
  def num_aliases(self):
    return self._namelist.num_aliases

  def remove_alias(self, alias):
    self._namelist.remove_alias(alias)

  def remove_all_aliases(self):
    self._namelist.remove_all()

  def reset_aliases(self, *aliases):
    self._namelist.reset(*aliases)

  def aliases(self):
    return self._namelist.list()

  """wrapped to behaviour:

     assign_spec_proc(spec_proc)   <- assign a single spec proc to behaviour
     assign_spec_procs(spec_procs) <- assign a list of spec procs to behaviour"""

  def assign_spec_proc(self, spec_proc):
    self.behaviour.assign(spec_proc)

  def assign_spec_procs(self, spec_procs):
    for spec_proc in spec_procs:
      self.behaviour.assign(spec_proc)

  # display state in readable string
  def debug(self):
    ret_val = f"Name: {CYAN}{self.name}{NORMAL}\r\n"
    ret_val += f"LDesc: {CYAN}{self.ldesc}{NORMAL}\r\n"
    ret_val += f"Alias: {CYAN}{self._namelist}{NORMAL}\r\n"
    ret_val += f"Desc: {CYAN}{str(self.desc)}{NORMAL}\r\n"
    ret_val += f"Room: {CYAN}{self.room}{NORMAL}\r\n"
    ret_val += self.behaviour.debug()
    return ret_val