import behaviour_data
from color import *
import entity_proto_data
import unique_id_data

class obj_proto_data(entity_proto_data.entity_proto_data):
  def __init__(self):
    super().__init__()
    # define object specific fields below
    self.uid = unique_id_data.unique_id_data()
    self.behaviour = behaviour_data.behaviour_data()

  @property
  def id(self):
    return self.uid.id
  @property
  def zone_id(self):
    return self.uid.zone_id

  @id.setter
  def id(self, new_id):
    self.uid.id = new_id
  @zone_id.setter
  def zone_id(self, new_zone_id):
    self.uid.zone_id = new_zone_id

  def debug(self):
    ret_val = f"ID: {CYAN}{str(self.uid)}{NORMAL}\r\n"
    ret_val += super().debug()
    # append object specific data below
    return ret_val