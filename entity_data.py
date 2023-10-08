import dataclasses
import editor
import unique_id_data

@dataclasses.dataclass
class entity_data:

  """name     = what to be referred to as
     ldesc    = what to see when the entity is in a room
     namelist = list of keywords to be targetted with
     desc     = shown when closely examined
     room     = reference to room if it is in one, and None otherwise
     Name     = same as name but capitalized
     in_zone  = zone_id of entity's location (if any)"""

  name:     str="an unfinished entity"
  ldesc:    str="An unfinished entity is here."
  namelist: list=dataclasses.field(default_factory=lambda:["unfinished", "entity"])
  desc:     editor.buffer=editor.buffer("This entity looks unfinished.")
  room:     unique_id_data.unique_id_data=None

  @property
  def Name(self):
    return self.name.capitalize()

  @property
  def in_zone(self):
    if self.room == None:
      return None
    return self.room.zone_id

  """has_alias(alias) <-- check if alias is in self.namelist
     debug()          <-- display state in readable string"""

  def has_alias(self, alias):
    return alias in self.namelist

  def debug(self):
    ret_val = f"Name: {self.name}\r\n"
    ret_val += f"LDesc: {self.ldesc}\r\n"
    ret_val += f"Alias:\r\n"
    for alias in self.namelist:
      ret_val += f"  {alias}\r\n"
    ret_val += f"Desc: {str(self.desc)[:20]}...\r\n"
    ret_val += f"Room: {self.room}\r\n"
    return ret_val