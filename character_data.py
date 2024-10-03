import config
import editor
import entity_data
import inventory
import mudlog
import unique_id_data

class character_data(entity_data.entity_data):
  """Creates a new character which can act within the world.

    name      = characters name (wrapped from entity)
    Name      = characters name capitalized (wrapped from entity)
    desc      = characters description as a buffer (wrapped from entity)
    ldesc      = how character is listed in a room to others (wrapped from entity)
    room      = what room character is in (wrapped from entity)
    namelist  = list of aliases for character to be accessed by (wrapped from entity)
    inventory = iterable container consisting of all objects held (see object.py)
    in_zone   = return zone_id of character's location (wrapped from entity)

    Note: This class is meant to encapsulate the functionality shared by pcs/npcs,
    so that they need not be distinguished between throughout this codebase.  While
    there is nothing stopping one from instantiating it directly, such use is not intended."""
  def __init__(self):
    super().__init__()
    self.name = "an unfinished character"
    self.desc = "This character looks unfinished."
    self.ldesc = "An unfinished character is here."
    self.room = unique_id_data.unique_id_data.from_string(config.VOID_ROOM)
    self.reset_alias("unfinished", "character")
    self.inventory = inventory.inventory()

  # Getters
  @property
  def inventory(self):
    return self.inventory
  @property
  def in_zone(self):
    return self.entity.in_zone

  # Setters
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
