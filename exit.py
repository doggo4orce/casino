import enum
import string_handling

class direction(enum.IntEnum):
  NORTH = 0
  EAST  = 1
  SOUTH = 2
  WEST  = 3
  UP    = 4
  DOWN  = 5

class exit:
  """Creates an exit which characters may use to travel between rooms.
    destination = vref to a room that this exit connects to"""
  def __init__(self, vref):
    self.destination = unique_id.unique_id(string_handling.parse_reference(vref))

  @property
  def destination(self):
    return self._destination

  @property
  def zone_id(self):
    return self.destination.zone_id
  @property
  def room_id(self):
    return self.destination.id

  @property
  def internal(self):
    return self.zone_id == None

  # TODO: see comment in unique_id_data.__str__()
  @property
  def vref(self):
    if self.internal:
      return self.room_id
    else:
      return f"{self.zone_id}[{self.room_id}]"

  @destination.setter
  def destination(self, new_dest):
    self._destination = new_dest

  @zone_id.setter
  def zone_id(self, new_zone_id):
    # sanity check handled internally to unique_id_data class
    self._destination.zone_id = new_zone_id

  @room_id.setter
  def room_id(self, new_room_id):
    # sanity check handled internally to unique_id_data class
    self._destination.room_id = new_room_id


