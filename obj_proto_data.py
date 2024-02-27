import behaviour_data
from color import *
import entity_data
import entity_proto_data
import unique_id_data

# Note: much of this file is identical to npc_proto_data.py
#
# This suggests perhaps more should be factored?
#  - behaviour and unique_id could be pulled into entity_proto?
#
class obj_proto_data:
  """Each of these fields are loaded into the corresponding object fields.
     entity_proto = name, namelist, ldesc, desc (entity_data.py)
     unique_id = global and local identifier (unique_id.py)
     behaviour = spec proc manager (behaviour_data.py)"""
  def __init__(self):
    self.entity_proto = entity_proto_data.entity_proto_data()
    self.unique_id = unique_id_data.unique_id_data()
    self.behaviour = behaviour_data.behaviour_data()

    # wrappd to entity_proto
    self.ldesc = "An unfinished object prototype stands here."

  @property
  def entity_proto(self):
    return self._entity_proto
  @property
  def unique_id(self):
    return self._unique_id
  @property
  def behaviour(self):
    return self._behaviour

  @entity_proto.setter
  def entity_proto(self, new_entity):
    self._entity_proto = new_entity
  @unique_id.setter
  def unique_id(self, new_uid):
    self._unique_id = new_uid
  @behaviour.setter
  def behaviour(self, new_behaviour):
    self._behaviour = new_behaviour

  # Wrapped properties
  @property
  def ldesc(self):
    return self.entity_proto.ldesc
  @property
  def id(self):
    return self.unique_id.id
  @property
  def zone_id(self):
    return self.unique_id.zone_id

  # Wrapped setters
  @ldesc.setter
  def ldesc(self, new_ldesc):
    self.entity_proto.ldesc = new_ldesc
  @id.setter
  def id(self, new_id):
    self.unique_id.id = new_id
  @zone_id.setter
  def zone_id(self, new_zid):
    self.unique_id.zone_id = new_zid

  """assign_spec_proc(spec_proc)   <- assign a single spec proc to behaviour
     assign_spec_procs(spec_procs) <- assign a list of spec procs to behaviour"""

  def assign_spec_proc(self, spec_proc):
    self.behaviour.assign(spec_proc)

  def assign_spec_procs(self, spec_procs):
    for spec_proc in spec_procs:
      self.behaviour.assign(spec_proc)

  def __str__(self):
    ret_val = f"Object: {CYAN}{self.entity_proto.name}{NORMAL}\r\n"
    ret_val += f"Alias: {CYAN}{' '.join(self.entity_proto.namelist)}{NORMAL}\r\n"
    ret_val += f"Desc: {CYAN}{self.entity_proto.desc}{NORMAL}\r\n"
    ret_val += f"L-Desc: {CYAN}{self.ldesc}{NORMAL}\r\n"
    ret_val += str(self.behaviour)
    return ret_val