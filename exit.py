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
    direction = one of the directions listed above
    destination = string reference to another room"""
  def __init__(self, dir, dest_ref):
    self._direction = dir

    if dest_ref.isalnum():
      self._destination = structs.unique_identifier(None, dest_ref)
    else:
      zone_id, room_id = string_handling.parse_reference(dest_ref)
      self._destination = structs.unique_identifier(zone_id, room_id)

  @property
  def direction(self):
    return self._direction
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


  @zone_id.setter
  def zone_id(self, new_zone_id):
    self._destination.zone_id = new_zone_id
