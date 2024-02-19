import copy
import dataclasses
import unique_id_data
  
class entity_data:
  """name     = what to be referred to as
     ldesc    = what to see when the entity is in a room
     namelist = list of keywords to be targetted with
     desc     = shown when closely examined
     room     = reference to room if it is in one, and None otherwise"""
  def __init__(self, proto=None):
    if proto == None:
      self.name = "an unfinished entity"
      self.namelist = ["unfinished", "entity"]
      self.ldesc = "An unfinished entity is here."
      self.desc = "This entity looks unfinished."
    else:
      self.name = proto.name
      self.namelist = copy.copy(proto.namelist)
      self.ldesc = proto.ldesc
      self.desc = proto.desc
    self.room = None

  @property
  def name(self):
    return self._name
  @property
  def namelist(self):
    return self._namelist
  @property
  def ldesc(self):
    return self._ldesc
  @property
  def desc(self):
    return self._desc
  @property
  def room(self):
    return self._room

  @name.setter
  def name(self, new_name):
    self._name = new_name
  @namelist.setter
  def namelist(self, new_namelist):
    self._namelist = list()
    for alias in new_namelist:
      self.add_alias(alias)
  @ldesc.setter
  def ldesc(self, new_ldesc):
    self._ldesc = new_ldesc
  @desc.setter
  def desc(self, new_desc):
    self._desc = new_desc
  @room.setter
  def room(self, new_room):
    self._room = new_room

  """Additional Properties:
     Name     = same as name but capitalized
     in_zone  = zone_id of entity's location (if any)"""

  @property
  def Name(self):
    return self.name.capitalize()

  @property
  def in_zone(self):
    if self.room == None:
      return None
    return self.room.zone_id

  """has_alias(alias)    <- check if alias is in self.namelist
     add_alias(alias)    <- adds a new alias to self.namelist
     remove_alias(alias) <- removes alias from self.namelist
     debug()             <- display state in readable string"""

  def has_alias(self, alias):
    return alias in self.namelist

  def add_alias(self, alias):
    if not self.has_alias(alias):
      self.namelist.append(alias)
      
  def remove_alias(self, alias):
    if self.has_alias(alias):
      self.namelist.remove(alias)

  def debug(self):
    ret_val = f"Name: {self.name}\r\n"
    ret_val += f"LDesc: {self.ldesc}\r\n"
    ret_val += f"Alias:\r\n"
    for alias in self.namelist:
      ret_val += f"  {alias}\r\n"
    ret_val += f"Desc: {str(self.desc)[:20]}...\r\n"
    ret_val += f"Room: {self.room}\r\n"
    return ret_val