import entity_data
import unique_id_data

class obj_proto_data:
  def __init__(self):
    self.entity = entity_data.entity()
    # DELETE THeSE AND REPLACE WITH BEHAVIOUR_DATA
    self.prefix_cmd_triggers = list()
    self.suffix_cmd_triggers = list()
    self.hbeat_procs = list()
    self.unique_id = unique_id_data.unique_id()

  @property
  def entity(self):
    return self._entity
  @property
  def prefix_cmd_triggers(self):
    return self._prefix_cmd_triggers
  @property
  def suffix_cmd_triggers(self):
    return self._suffix_cmd_triggers
  @property
  def hbeat_procs(self):
    return self._hbeat_procs
  @property
  def unique_id(self):
    return self._unique_id

  @entity.setter
  def entity(self, new_entity):
    self._entity = new_entity
  @prefix_cmd_triggers.setter
  def prefix_cmd_triggers(self, new_cmd_trigs):
    self._prefix_cmd_triggers = new_cmd_trigs
  @suffix_cmd_triggers.setter
  def suffix_cmd_triggers(self, new_cmd_trigs):
    self._suffix_cmd_triggers = new_cmd_trigs
  @hbeat_procs.setter
  def hbeat_procs(self, new_procs):
    self._hbeat_procs = new_procs
  @unique_id.setter
  def unique_id(self, new_uid):
    self._unique_id = new_uid