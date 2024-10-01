from color import *
import entity_proto_data
import unique_id_data

class npc_proto_data(entity_proto_data.entity_proto_data):
  def __init__(self):
    super().__init__()
    # define NPC specific fields below

  def debug(self):
    ret_val = ""
    ret_val += super().debug()
    return ret_val