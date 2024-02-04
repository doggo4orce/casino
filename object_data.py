import dataclasses
import entity_data
import logging
import spec_procs
import structs

class object_data:
  """Creates an object which characters can get, drop, and otherwise interact with.
    entity                  = aggregates name, namelist, description, and room
    ldesc                   = one line description shown after room description
    prefix_command_triggers = spec procs that fire before commands processed
    suffix_command_triggers = spec procs that fire after commands processed
    heart_beat_procs        = spec procs that fire each heartbeat"""
  def __init__(self, proto=None):
    self.entity = entity.entity_data()
    self.ldesc = "An unfinished object has been left here."
    self.prefix_command_triggers = list()
    self.suffix_command_triggers = list()
    self.heart_beat_procs = list()

    if proto != None:
      self.entity = dataclasses.replace(proto.entity)
      self.ldesc = proto.ldesc
      self.prefix_command_triggers = proto.prefix_command_triggers.copy()
      self.suffix_command_triggers = proto.suffix_command_triggers.copy()
      self.heart_beat_procs = proto.heart_beat_procs.copy()

  @property
  def entity(self):
    return self._entity
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
  @ldesc.setter
  def ldesc(self, new_ldesc):
    self.entity.ldesc = new_ldesc
  @room.setter
  def room(self, new_room):
  	self.entity.room = new_room
  @name.setter
  def name(self, new_name):
    self.entity.name = new_name
  @prefix_command_triggers.setter
  def prefix_command_triggers(self, new_triggers):
    self._prefix_command_triggers = new_triggers
  @suffix_command_triggers.setter
  def suffix_command_triggers(self, new_triggers):
    self._suffix_command_triggers = new_triggers
  @heart_beat_procs.setter
  def heart_beat_procs(self, new_procs):
    self._heart_beat_procs = new_procs

  def has_alias(self, alias):
    return self._entity.has_alias(alias)

  def call_prefix_command_triggers(self, mud, ch, command, argument, db):
    for procedure in self.prefix_command_triggers:
      if procedure.call(mud, self, ch, command, argument, db) == spec_procs.prefix_command_trigger_messages.BLOCK_INTERPRETER:
        return spec_procs.prefix_command_trigger_messages.BLOCK_INTERPRETER
    return spec_procs.prefix_command_trigger_messages.RUN_INTERPRETER

  def call_suffix_command_triggers(self, mud, ch, command, argument, db):
    for procedure in self.suffix_command_triggers:
      procedure.call(mud, self, ch, command, argument, db)

  def call_heart_beat_procs(self, mud, db):
    for procedure in self.heart_beat_procs:
      procedure.call(mud, self, db)

  def debug(self):
    ret_val = self.entity.debug()
    #TODO: factor sepc_proc code out into entity
    #because it also appears in npc
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
  def __str__(self):
    return self.name
