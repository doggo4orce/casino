import buffer_data
import character_data
from color import *
import exit_data
import inventory_data
import object_data
import pc_data
import room_attribute_data
import string_handling
import unique_id_data

class room_data:
  """Creates a new room which may be occupied by characters and objects (eventually)
      attributes = contains static data of room
      people     = list of characters in the room
      contents   = list of objects on the ground"""
  def __init__(self):
    self._attributes = room_attribute_data.room_attribute_data()
    self.name = "Unfinished Room"
    self.desc = "<p>This room has no description.  Use the REDIT command while standing inside this room to give it one!</p>"
    self._people = list()
    self._contents = inventory_data.inventory_data()

  # Getters
  @property
  def attributes(self):
    return self._attributes
  @property
  def id(self):
    return self.attributes.id
  @property
  def zone_id(self):
    return self.attributes.zone_id
  @property
  def unique_id(self):
    return self.attributes.uid
  @property
  def name(self):
    return self.attributes.name
  @property
  def desc(self):
    return self.attributes.desc
  @property
  def exits(self):
    return self.attributes.exits
  @property
  def people(self):
    return self._people
  @property
  def contents(self):
    return self._contents

  # Setters
  @attributes.setter
  def attributes(self, new_attributes):
    self._attributes = new_attributes
  @id.setter
  def id(self, new_id):
    self.attributes.id = new_id
  @zone_id.setter
  def zone_id(self, new_zone_id):
    self.attributes.zone_id = new_zone_id
  @unique_id.setter
  def unique_id(self, new_unique_id):
    self.attributes.uid = new_uid
  @name.setter
  def name(self, new_name):
    self.attributes.name = new_name
  @desc.setter
  def desc(self, new_desc):
    self.attributes.desc = new_desc

  """add_entity(entity)        <- (internal) add entity to room
     remove_entity(entity)     <- (internal) remove entity from room
     add_char(ch)              <- adds character to this room
     remove_char(ch)           <- removes character ch from this room
     add_object(obj)           <- add object to room
     remove_object(obj)        <- remove object from room
     has_object(obj)           <- check if obj is in character's inventory
     char_by_alias(name)       <- look for char in room with name (prioritizes pc)
     pc_by_name(name)          <- look for pc in room with name
     npc_by_alias(alias)       <- looks for npc in room with alias
     obj_by_alias(alias)       <- looks for obj in room with alias
     connect(dir, zone_id, id) <- creates exit to another room
     disconnect(dir)           <- removes exit
     display_exits()           <- shows exits to be displayed with room description
     echo(msg)                 <- sends msg to every character in the room
     exit(dir)                 <- returns exit object leading in direction dir or None
     get_destination(dir)      <- returns exit.destination for exit in direction dir
     has_exit(dir)             <- checks if the room has an exit leading in direction dir"""

  def _add_entity(self, entity):
    entity.room = self.unique_id
    if isinstance(entity, character_data.character_data):
      self._people.append(entity)
    elif isinstance(entity, object_data.object_data):
      self._contents.add_object(entity)

  def _remove_entity(self, entity):
    entity.room = None
    if isinstance(entity, character_data.character_data):
      self._people.remove(entity)
    elif isinstance(entity, object_data.object_data):
      self._contents.remove_object(entity)

  def _has_entity(self, entity):
    if isinstance(entity, character_data.character_data):
      return entity in self._people
    elif isinstance(entity, object_data.object_data):
      return entity in self._contents

  def add_char(self, ch):
    self._add_entity(ch)

  def remove_char(self, ch):
    self._remove_entity(ch)

  def has_char(self, ch):
    return self._has_entity(ch)

  def add_obj(self, obj):
    self._add_entity(obj)

  def remove_object(self, obj):
    self._remove_entity(obj)

  def has_object(self, obj):
    return self._has_entity(obj)

  def char_by_alias(self, name):
    # first check for pc
    tch = self.pc_by_name(name)
    if tch != None:
      return tch
    # if nothing found, then check for npc
    tch = self.npc_by_alias(name)
    if tch != None:
      return tch
    # by now we have nothing
    return None

  def pc_by_name(self, name):
    for ch in self._people:
      if isinstance(ch, pc.pc) and ch.has_alias(name):
        return ch
    return None

  def npc_by_alias(self, alias):
    for ch in self.people:
      if isinstance(ch, pc.npc) and ch.has_alias(alias):
        return ch
    return None

  def obj_by_alias(self, alias):
    for obj in self.inventory:
      if obj.has_alias(alias):
        return obj
    return None

  def connect(self, direction, zone_id, room_id):
    self.attributes.connect(direction, zone_id, room_id)

  def disconnect(self, direction):
    self.attributes.disconnect(direction)

  def display_exits(self):
    return self.attributes.display_exits

  def echo(self, msg, **kwargs):
    exceptions = list()

    if "exceptions" in kwargs:
      exceptions = kwargs["exceptions"]

    for ch in self._people:
      if ch not in exceptions:
        ch.write(msg)

  def exit(self, direction):
    return self.attributes.exit(direction)

  def get_destination(self, direction):
    exit = self.exit(direction)
    if exit == None:
      return None
    return exit.destination

  def has_exit(self, direction):
    return self.attributes.has_exit(direction)

  def debug(self):
    ret_val = self.attributes.debug()
    if len(self._people) > 0:
      ret_val += "People:\r\n"
      for ch in self._people:
        ret_val += f"  {CYAN}{ch}{NORMAL}\r\n"
    if len(self._contents) > 0:
      ret_val += "Contents:\r\n"
      for obj in self._contents:
        ret_val += f"  {CYAN}{obj}{NORMAL}\r\n"
    return ret_val