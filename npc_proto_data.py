import behaviour_data
import buffer_data
import entity_data
import entity_proto_data
from mudlog import mudlog_type, mudlog
import spec_proc_data
import unique_id_data

class npc_proto_data:
  """Each of these fields are loaded into the corresponding NPC fields.
     entity_proto = name, namelist, ldesc, desc (entity_data.py)
     unique_id = global and local identifier (unique_id.py)
     behaviour = spec proc manager (behaviour_data.py)"""
  def __init__(self):
    self.entity_proto = entity_proto_data.entity_proto_data()
    self.unique_id = unique_id_data.unique_id_data()
    self.behaviour = behaviour_data.behaviour_data()
    self.ldesc = "An unfinished npc proto_type stands here."

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
  def entity_proto(self, new_entity_proto):
    self._entity_proto = new_entity_proto
  @unique_id.setter
  def unique_id(self, new_uid):
    self._unique_id = new_uid
  @behaviour.setter
  def behaviour(self, new_behaviour):
    self._behaviour = new_behaviour

  # Wrapped properties
  @property
  def ldesc(self):
    return self.entity_proto._ldesc
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
    ret_val = f"NPC: {CYAN}{self.entity.name}{NORMAL} "
    ret_val += f"Alias: {CYAN}{' '.join(self.namelist)}{NORMAL}\r\n"
    ret_val += buffer_data.buffer_data(self.entity.desc).display(width=65, indent=True)
    ret_val += f"Desc:\r\n{self.entity.desc.str()}\r\n"
    ret_val += f"L-Desc: {self.ldesc}\r\n"
    ret_val += str(self.behaviour)
    return ret_val