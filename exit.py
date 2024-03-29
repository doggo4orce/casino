import database
import enum
import string_handling
import structs

class direction(enum.IntEnum):
  NORTH = 0
  EAST  = 1
  SOUTH = 2
  WEST  = 3
  UP    = 4
  DOWN  = 5

class exit:
  """Creates an exit which characters may use to travel between rooms.
    destination = string reference to another room"""
  def __init__(self, dest_ref):
    # this should be handled more cleanly, but who has the time?
    # why not just use regex and search for (\w\w*)[(\w\w*)]
    if string_handling.valid_id(dest_ref):
      self._destination = structs.unique_identifier(None, dest_ref)
    else:
      zone_id, room_id = string_handling.parse_reference(dest_ref)
      self._destination = structs.unique_identifier(zone_id, room_id)

  @property
  def zone_id(self):
    return self._destination.zone_id
  @property
  def room_id(self):
    return self._destination.id
  @property
  def internal(self):
    return self.zone_id == None
  @property
  def destination(self):
    if self.internal:
      return self.room_id
    else:
      return f"{self.zone_id}[{self.room_id}]"

  def save_to_db(self, rm, c):
    """Saves the exit through to the database through connection c"""

    # check if the room already exists in the database
    if database.ex_table_contains_exit(c, rm, self):
      # if so, then delete it so we can re-add it below
      database.ex_table_delete_exit(c, rm, self)

    database.ex_table_add_exit(c, rm, self)

  @zone_id.setter
  def zone_id(self, new_zone_id):
    self._destination.zone_id = new_zone_id
