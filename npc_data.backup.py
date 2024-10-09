import character_data

class npc_data(character_data.character_data, actor_data.actor_data):
  """Creates a new NPC (non-playable character).
     ldesc = one line description shown after room description
     prefix_command_triggers = procs called before command is processed
     suffix_command_triggers = procs called after command is processed
     heart_beat_procs = list of pulsing special procedures"""
  def __init__(self, proto=None):
    super(character_data.character_data).__init__()
    self.name = "an unfinished npc"
    self.desc = editor.buffer("This npc looks unfinished.")
    self.ldesc = "An unfinished npc is here."
    self.entity.namelist = ["unfinished", "npc"]
    self.prefix_command_triggers = list()
    self.suffix_command_triggers = list()
    self.heart_beat_procs = list()

    if proto != None:
      self.entity = dataclasses.replace(proto.entity)
      self.ldesc = proto.ldesc
      super(actor_data.actor_data).__init__(proto.behaviour)


  # Getters
  @property
  def entity(self):
    return self._entity
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
  @prefix_command_triggers.setter
  def prefix_command_triggers(self, new_triggers):
    self._prefix_command_triggers = new_triggers
  @suffix_command_triggers.setter
  def suffix_command_triggers(self, new_triggers):
    self._suffix_command_triggers = new_triggers
  @heart_beat_procs.setter
  def heart_beat_procs(self, new_procs):
    self._heart_beat_procs = new_procs

  """from_char(ch)                                       <- upgrades character ch to npc
     write(msg)                                          <- does nothing (see below)
     assign_spec_proc(new_proc)                          <- adds new_proc to self.specs"""
     
  @classmethod
  def from_char(cls, ch):
    ret_val = cls()
    ret_val.entity = ch.entity
    ret_val.ldesc = ch.ldesc
    ret_val.inventory = ch.inventory
    return ret_val

  """it's unclear what should be done with message, but since I'd like pcs and npcs
     to be as interchangeable as possible, this function ought to exist.

     Perhaps this function could:
       -process speech triggers (if such things were to be implemented), or
       -route the message to a player who is controlling the npc (eg. with a spell)?"""
  def write(self, message):
    pass

  def debug(self):
    ret_val = super().debug()

    #TODO: factor this code out into entity (see below)
    #because it also appears in object.debug()
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

