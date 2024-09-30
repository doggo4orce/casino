import behaviour_data
from color import *
import namelist_data

class entity_proto_data:
  """Acts as blueprints to create entities.
     name      = what to be referred to as
     namelist  = list of keywords to be targetted with
     ldesc     = what to see when the entity is in a room
     desc      = shown when closely examined
     TODO: this should be changed to location, to be less misleading
     behaviour = spec proc manager"""
  def __init__(self):
    self.name ="an unfinished entity proto"
    self.namelist = namelist_data.namelist_data("unfinished", "entity", "proto")
    self.ldesc = "An unfinished entity proto is here."
    self.desc = "This entity proto looks unfinished."
    self.behaviour = behaviour_data.behaviour_data()

  @property
  def name(self):
    return self._name
  @property
  def namelist(self):
    return self._namelist
  @property
  def ldesc(self):
    return self._ldesc
  @property
  def desc(self):
    return self._desc
  @property
  def behaviour(self):
    return self._behaviour

  @name.setter
  def name(self, new_name):
    self._name = new_name
  @namelist.setter
  def namelist(self, new_namelist):
    self._namelist = new_namelist
  @ldesc.setter
  def ldesc(self, new_ldesc):
    self._ldesc = new_ldesc
  @desc.setter
  def desc(self, new_desc):
    self._desc = new_desc
  @behaviour.setter
  def behaviour(self, new_behaviour):
    self._behaviour = new_behaviour

  """Wrapped to namelist:

     add_alias(alias)       <- adds a new alias to namelist
     has_alias(alias)       <- check namelist for alias
     num_aliases            <- count aliases in namelist
     remove_aliases(alias)  <- remove alias from namelist
     remove_all_alias()     <- remove all aliases"""

  def add_alias(self, alias):
    self.namelist.add_alias(alias)
      
  def has_alias(self, alias):
    return self.namelist.has_alias(alias)

  @property
  def num_aliases(self):
    return self.namelist.num_aliases

  def remove_alias(self, alias):
    self.namelist.remove_alias(alias)

  def remove_all_aliases(self):
    self.namelist.remove_all()

  """Wrapped to behaviour:

     assign_spec_proc(spec_proc)   <- assign a single spec proc to behaviour
     assign_spec_procs(spec_procs) <- assign a list of spec procs to behaviour"""

  def assign_spec_proc(self, spec_proc):
    self.behaviour.assign(spec_proc)

  def assign_spec_procs(self, spec_procs):
    for spec_proc in spec_procs:
      self.behaviour.assign(spec_proc)

  # display debugging information
  def debug(self):
    ret_val = f"Name: {CYAN}{self.name}{NORMAL}\r\n"
    ret_val += f"LDesc: {CYAN}{self.ldesc}{NORMAL}\r\n"
    ret_val += f"Alias: {CYAN}{str(self.namelist)}{NORMAL}\r\n"
    ret_val += f"Desc: {CYAN}{str(self.desc)}{NORMAL}\r\n"
    ret_val += self.behaviour.debug()
    return ret_val