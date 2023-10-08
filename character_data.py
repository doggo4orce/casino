import config
import editor
import entity_data
import inventory
import logging
import structs
import unique_id_data

class character_data:
  """Creates a new char(acter) which can act within the world.

    entity    = dataclass encapsulating name, appearance and location (see structs.py)
    name      = characters name (wrapped from entity)
    Name      = characters name capitalized (wrapped from entity)
    desc      = characters description as a buffer (wrapped from entity)
    ldec      = how character is listed in a room to others (wrapped from entity)
    room      = what room character is in (wrapped from entity)
    namelist  = list of aliases for character to be accessed by (wrapped from entity)
    inventory = iterable container consisting of all objects held (see object.py)
    in_zone   = return zone_id of character's location (wrapped from entity)

    Note: This class is meant to encapsulate the functionality shared by pcs/npcs,
    so that they need not be distinguished between throughout this codebase.  While
    there is nothing stopping one from instantiating it directly, such use is not intended."""
  def __init__(self):
    self.entity = entity_data.entity_data()
    self.name = "an unfinished character"
    self.desc = editor.buffer("This character looks unfinished.")
    self.ldesc = "An unfinished character is here."
    self.room = unique_id_data.unique_id_data.from_string(config.VOID_ROOM)
    self.namelist = ["unfinished", "character"]
    self.inventory = inventory.inventory()

  # Getters
  @property
  def entity(self):
    return self._entity
  @property
  def name(self):
    return self.entity.name
  @property
  def Name(self):
    return self.entity.Name
  @property
  def desc(self):
    return self.entity.desc
  @property
  def ldesc(self):
    return self.entity.ldesc
  @property
  def room(self):
    return self.entity.room
  @property
  def namelist(self):
    return self.entity.namelist
  @property
  def inventory(self):
    return self.inventory
  @property
  def in_zone(self):
    return self.entity.in_zone

  # Setters
  @entity.setter
  def entity(self, new_ent):
    self._entity = new_ent
  @name.setter
  def name(self, new_name):
    self._entity.name = new_name
  @desc.setter
  def desc(self, new_desc):
    self.entity.desc = new_desc
  @ldesc.setter
  def ldesc(self, new_ldesc):
    self.entity.ldesc = new_ldesc
  @room.setter
  def room(self, new_room):
    self.entity.room = new_room
  @namelist.setter
  def namelist(self, new_namelist):
    self.entity.namelist = new_namelist
  @inventory.setter
  def inventory(self, new_inventory):
    self._inventory = new_inventory

  """write(message)   <-- no operation, should be over-written by derived classes
     in_zone()        <-- return zone_id of character's location
     has_alias(alias) <-- check if alias is in self.namelist (wrapped from entity)
     debug()          <-- display state in readable string"""

  def write(self, message):
    logging.warning(f"Attempting to send message {message} to character {self.entity.name}")
    return

  def has_alias(self, alias):
    return self._entity.has_alias(alias)

  def debug(self):
    ret_val = self.entity.debug()
    ret_val += f"Type: {type(self)}\r\n"
    return ret_val

  def __str__(self):
    return self.name
