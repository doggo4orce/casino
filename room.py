from color import *
import database
import enum
import editor
import exit_data
import inventory
import object_data
import pc
import room_attribute_data
import string_handling
import unique_id_data

class room:
  """Creates a new room which may be occupied by characters and objects (eventually)
      attributes =
      people     = list of characters in the room
      contents   = list of objects on the ground"""
  def __init__(self):
    self._attributes = room_attribute_data.room_attribute_data("Unfinished Room", "It looks unfinished.")
    self._people    = list()
    self._contents = inventory.inventory()

  # Getters
  @property
  def attributes(self):
    return self._attributes
  @property
  def name(self):
    return self.attributes.name
  @property
  def unique_id(self):
    return self.attributes.uid
  @property
  def id(self):
    return self.attributes.id
  @property
  def zone_id(self):
    return self.attributes.zone_id
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

  @name.setter
  def name(self, new_name):
    self.attributes.name = new_name

  @unique_id.setter
  def unique_id(self, new_unique_id):
    self.attributes.uid = new_uid

  @id.setter
  def id(self, new_id):
    self.attributes.id = new_id

  @zone_id.setter
  def zone_id(self, new_zone_id):
    self.attributes.zone_id = new_zone_id

  @desc.setter
  def desc(self, new_desc):
    self.attributes.desc = new_desc

  """add_char(ch)              <- adds character to this room
     remove_char(ch)           <- removes character ch from this room
     char_by_alias(name)       <- look for char in room with name (prioritizes pc)
     pc_by_name(name)          <- look for pc in room with name
     npc_by_alias(alias)       <- looks for npc in room with alias
     obj_by_alias(alias)       <- looks for obj in room with alias
     connect(dir, zone_id, id) <- creates exit to another room
     disconnect(dir)           <- removes exit
     display_exits()           <- shows exits to be displayed with room description
     echo(msg)                 <- sends msg to every character in the room
     exit(dir)                 <- returns exit object leading in direction dir or None
     get_destination(dir)      <- returns vref for room that the exit in direction dir leads to
     has_exit(dir)             <- checks if the room has an exit leading in direction dir
     save_to_db(c)             <- saves the room to cursor c"""
  def add_char(self, ch):
    ch.room = self.unique_id
    self._people.append(ch)

  def remove_char(self, ch):
    ch.room = None
    self._people.remove(ch)

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
    if direction in self._exits.keys():
      return self._exits[direction]
    return None

  def get_destination(self, direction):
    exit = self.exit(direction)
    if exit == None:
      return None
    return exit.destination

  def has_exit(self, direction):
    return self.attributes.has_exit(direction)

  # TODO: doesn't look like this is called anywhere, delete it if not
  def save_to_db(self, c):
    """Saves the room and calls corresponding function for each exit through to database connection c"""

    # check if the room already exists in the database
    if database.wld_table_contains_room(c, self):
      # if so, then delete it so we can re-add it below
      database.wld_table_delete_room(c, self)

    database.wld_table_add_room(c, self)

    for ex in self.exits.values():
      ex.save_to_db(self, c)

  def __str__(self):
    ret_val = f"Name: {CYAN}{self.name}{NORMAL}\r\n"
    ret_val += f"Description:\r\n{string_handling.paragraph(self.desc, 65, True)}\r\n"
    ret_val += "Exits:\r\n"

    for ex in self.exits:
      ret_val += "  " + str(ex)

    return ret_val