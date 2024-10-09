import actor_data
import character_data

class npc_data(character_data.character_data, actor_data.actor_data):
  """Creates a new NPC (non-playable character).
     ldesc = one line description shown after room description
     prefix_command_triggers = procs called before command is processed
     suffix_command_triggers = procs called after command is processed
     heart_beat_procs = list of pulsing special procedures"""
  def __init__(self, proto=None):
    actor_data.actor_data.__init__(self)
    character_data.character_data.__init__(self)
    self.name = "an unfinished npc"
    self.desc = "This npc looks unfinished."
    self.ldesc = "An unfinished npc is here."
    self.reset_aliases("unfinished", "npc")

    if proto != None:
      self.ldesc = proto.ldesc
      actor_data.actor_data.__init__(self, proto.behaviour)

  """from_character(ch) <- returns npc created from ch
     copy_from(npc)     <- make copy of npc
     write(msg)         <- noop (see below)"""
  @classmethod
  def from_character(cls, ch):
    ret_val = cls()
    character_data.character_data.copy_from(ret_val, ch)
    return ret_val

  def copy_from(self, npc):
    actor_data.actor_data.copy_from(self, ch)
    character_data.character_data.copy_from(self, ch)
    return ret_val
        
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
    ret_val += actor_data.actor_data.debug(self)
    return ret_val

