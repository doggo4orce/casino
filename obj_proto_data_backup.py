from color import *
import entity_proto_data
import unique_id_data

class obj_proto_data:
  """Each of these fields are loaded into the corresponding object fields.
     entity_proto = name, namelist, ldesc, desc (entity_data.py)
     unique_id = unique identifier of object prototype"""
  def __init__(self):
    self.entity_proto = entity_proto_data.entity_proto_data()
    self.unique_id = unique_id_data.unique_id_data()

    # wrapped to entity_proto
    self.ldesc = "An unfinished object prototype stands here."

  @property
  def entity_proto(self):
    return self._entity_proto
  @property
  def unique_id(self):
    return self._unique_id
  @property
  def ldesc(self):
    return self.entity_proto.ldesc

  @property
  def id(self):
    return self.unique_id.id
  @property
  def zone_id(self):
    return self.unique_id.zone_id
  @property
  def behaviour(self):
    return self.entity_proto._behaviour

  @entity_proto.setter
  def entity_proto(self, new_entity):
    self._entity_proto = new_entity
  @unique_id.setter
  def unique_id(self, new_uid):
    self._unique_id = new_uid
  @ldesc.setter
  def ldesc(self, new_ldesc):
    self.entity_proto.ldesc = new_ldesc

  @id.setter
  def id(self, new_id):
    self.unique_id.id = new_id
  @zone_id.setter
  def zone_id(self, new_zid):
    self.unique_id.zone_id = new_zid
  @behaviour.setter
  def behaviour(self, new_behaviour):
    self.entity_proto.behaviour = new_behaviour

  """Wrapped to entity_proto:

     add_alias(alias)       <- adds a new alias to entity_proto
     has_alias(alias)       <- check entity_proto for alias
     num_aliases            <- count aliases in entity_proto
     remove_aliases(alias)  <- remove alias from entity_proto
     remove_all_aliases()     <- remove all aliases"""

  def add_alias(self, alias):
    self.entity_proto.add_alias(alias)
      
  def has_alias(self, alias):
    return self.entity_proto.has_alias(alias)

  @property
  def num_aliases(self):
    return self.entity_proto.num_aliases

  def remove_alias(self, alias):
    self.entity_proto.remove_alias(alias)

  def remove_all_alias(self):
    self.entity_proto.remove_all_aliases()

  """Wrapped to entity_proto:

     assign_spec_proc(spec_proc)   <- assign a single spec proc to behaviour
     assign_spec_procs(spec_procs) <- assign a list of spec procs to behaviour"""

  def assign_spec_proc(self, spec_proc):
    self.entity_proto.behaviour.assign(spec_proc)

  def assign_spec_procs(self, spec_procs):
    for spec_proc in spec_procs:
      self.entity_proto.behaviour.assign(spec_proc)

  def debug(self):
    ret_val = f"Object: {CYAN}{self.entity_proto.name}{NORMAL}\r\n"
    ret_val += f"Alias: {CYAN}{' '.join(self.entity_proto.namelist)}{NORMAL}\r\n"
    ret_val += f"Desc: {CYAN}{self.entity_proto.desc}{NORMAL}\r\n"
    ret_val += f"L-Desc: {CYAN}{self.ldesc}{NORMAL}\r\n"
    ret_val += self.behaviour.debug()
    return ret_val