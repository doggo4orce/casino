import actor_data
import character_data
from color import *
import entity_data
import unique_id_data

class npc_data(actor_data.actor_data, character_data.character_data):
  """Creates a new NPC (non-playable character).
     ldesc = one line description shown after room description
     prefix_command_triggers = procs called before command is processed
     suffix_command_triggers = procs called after command is processed
     heart_beat_procs = list of pulsing special procedures"""
  def __init__(self, proto=None):
    actor_data.actor_data.__init__(self)
    character_data.character_data.__init__(self)
    self.uid = unique_id_data.unique_id_data()
    self.name = "an unfinished npc"
    self.desc = "This npc looks unfinished."
    self.ldesc = "An unfinished npc is here."
    self.reset_aliases("unfinished", "npc")

    if proto != None:
      self.zone_id = proto.zone_id
      self.id = proto.id
      entity_data.entity_data.__init__(self, proto)
      actor_data.actor_data.__init__(self, proto.behaviour)

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

  """from_character(ch) <- returns npc created from ch
     copy_from(npc)     <- make copy of npc
     write(msg)         <- noop (see below)"""

  @classmethod
  def from_character(cls, ch):
    ret_val = cls()
    character_data.character_data.copy_from(ret_val, ch)
    return ret_val

  def copy_from(self, npc):
    actor_data.actor_data.copy_from(self, npc)
    character_data.character_data.copy_from(self, npc)
    self.id = npc.id
    self.zone_id = npc.zone_id
        
  """it's unclear what should be done with message, but since I'd like pcs and npcs
     to be as interchangeable as possible, this function ought to exist.

     Perhaps this function could:
       -process speech triggers (if such things were to be implemented), or
       -route the message to a player who is controlling the npc
        (eg. with a spell)?"""
  def write(self, message):
    pass

  def debug(self):
    ret_val = character_data.character_data.debug(self) + "\r\n"
    ret_val += f"UID: {CYAN}{self.uid}{NORMAL}\r\n"
    ret_val += actor_data.actor_data.debug(self)
    return ret_val

