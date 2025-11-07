import config
import copy
import entity_data
import inventory_data
import mudlog
import unique_id_data

class character_data(entity_data.entity_data):
  """Creates a new character which can act within the world.
    room = uid of room character is in
    inventory = all objects held (private)"""

  def __init__(self):
    super().__init__()
    self.name = "an unfinished character"
    self.desc = "This character looks unfinished."
    self.ldesc = "An unfinished character is here."
    self.room = None
    self.reset_aliases("unfinished", "character")
    self._inventory = inventory_data.inventory_data()

  """copy_from(ch)          <- make a copy, ignores inventory
     object_by_alias(alias) <- check inventory for object with alias
     give_object(obj)       <- add object to inventory
     lose_object(obj)       <- remove object from inventory
     has_object(obj)        <- check if object is in inventory
     transfer_obj(obj, ch)  <- give obj to ch
     transfer_inventory(ch) <- give all inventory to ch
     inventory()            <- copy of self._inventory as list
     write(msg)             <- no operation, should be over-written by derived classes
     debug()                <- returns debugging information as a string"""

  def copy_from(self, ch):
    super().copy_from(ch)
    # copy character specific fields below

  def object_by_alias(self, alias):
    return self._inventory.object_by_alias(alias)

  def give_object(self, obj):
    if not self.has_object(obj):
      self._inventory.add_object(obj)
    else:
      mudlog.error(f"Trying to give {obj} to character {self} who already has it!")

  def lose_object(self, obj):
    if self.has_object(obj):
      self._inventory.remove_object(obj)
    else:
      mudlog.error(f"Character {self} trying to lose {obj} but doesn't have it!")
 
  def has_object(self, obj):
    return self._inventory.has_object(obj)

  def transfer_obj(self, obj, ch):
    self._inventory.transfer_obj(obj, ch._inventory)

  def transfer_inventory(self, ch):
    self._inventory.transfer_all(ch._inventory)

  def inventory(self):
    return self._inventory.contents()

  def write(self, message):
    mudlog.debug(f"Character {self.name}'s write function called with \"{message}\"")
    return

  def debug(self):
    ret_val = super().debug()
    return ret_val

  def __str__(self):
    return self.name
