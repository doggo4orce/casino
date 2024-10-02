import dataclasses
import entity_data
import logging
import spec_proc_data

class object_data(entity_data.entity_data):
  """Creates an object which characters can get, drop, and otherwise interact with.
     entity           = aggregates name, namelist, description, ldesc, and room"""

  """Note: It may seem that nothing distinguishes objects from entities but this is
     not the case.  It's just that those differences have not been implemented yet.
     For example, objects will eventually have stats that do not yet appear here."""
  def __init__(self, proto=None):
    super().__init__(proto)

    if proto == None:
      self.name = "an unfinished object"
      self.reset_aliases("unfinished", "object")
      self.ldesc = "An unfinished object has been left here."
      self.desc = "This object looks unfinished."

  @property
  def entity(self):
    return self._entity

  @property(self):
  def name(self):
    return self.entity.name

  @property
  def ldesc(self):
    return self.entity.ldesc
  @property
  def room(self):
    return self.entity.room
  @property
  def name(self):
    return self.entity.name
  @property
  def desc(self):
    return self.entity.desc

  # Setters
  @entity.setter
  def entity(self, new_entity):
    self._entity = new_entity
  @ldesc.setter
  def ldesc(self, new_ldesc):
    self.entity.ldesc = new_ldesc
  @room.setter
  def room(self, new_room):
  	self.entity.room = new_room
  @name.setter
  def name(self, new_name):
    self.entity.name = new_name
  @desc.setter
  def desc(self, new_desc):
    self.entity.desc = new_desc
  def has_alias(self, alias):
    return self._entity.has_alias(alias)

  # wrapped from entity

  def add_alias(self, alias):
    self.entity.add_alias(alias)
      
  def has_alias(self, alias):
    return self.entity.has_alias(alias)

  def num_aliases(self):
    return self.entity.num_aliases()

  def remove_alias(self, alias):
    self.entity.remove_alias(alias)

  def remove_all_alias(self):
    self.entity.remove_all_alias()

  def assign_spec_proc(self, spec_proc):
    self.entity.behaviour.assign(spec_proc)

  def assign_spec_procs(self, spec_procs):
    for spec_proc in spec_procs:
      self.entity.behaviour.assign(spec_proc)

  def debug(self):
    ret_val = self.entity.debug()
    return ret_val

  def __str__(self):
    return self.name
