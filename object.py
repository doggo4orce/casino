import dataclasses
import logging
import structs

class object:
  """Creates an object which characters can get, drop, and otherwise interact with.
    entity = aggregates name, namelist, description, and room
    ldesc = one line description shown after room description"""
  def __init__(self, proto=None):
    self._entity = structs.entity_data()
    self._ldesc = "An unfinished object has been left here."
    self._prefix_command_triggers = list()
    self._suffix_command_triggers = list()
    self._heart_beat_procs = list()

    if proto != None:
      self._entity = dataclasses.replace(proto.entity)
      self.ldesc = proto.ldesc
      self._prefix_command_triggers = proto.prefix_command_triggers.copy()
      self._suffix_command_triggers = proto.suffix_command_triggers.copy()
      self._heart_beat_procs = proto.heart_beat_procs.copy()

  @property
  def entity(self):
    return self._entity
  @property
  def ldesc(self):
    return self._ldesc
  @property
  def room(self):
    return self._entity.room
  @property
  def name(self):
    return self._entity.name
  @property
  def desc(self):
    return self._entity.desc

  # Setters
  def entity(self, new_entity):
    self._entity = new_entity
  @ldesc.setter
  def ldesc(self, new_ldesc):
    self._ldesc = new_ldesc
  @room.setter
  def room(self, new_room):
  	self._entity.room = new_room
  @name.setter
  def name(self, new_name):
    self._entity.name = new_name

  def has_alias(self, alias):
    return self._entity.has_alias(alias)

  def __str__(self):
    return self.name
