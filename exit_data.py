import enum
import string_handling
import unique_id_data

class direction(enum.IntEnum):
  NORTH = 0
  EAST  = 1
  SOUTH = 2
  WEST  = 3
  UP    = 4
  DOWN  = 5

class exit_data:
  """Creates an exit which characters may use to travel between rooms.
    direction   = the direction the exit leads in
    destination = vref to the room that this exit leads to"""
  def __init__(self, direction=None, zone_id=None, id=None):
    self.direction = direction
    self.destination = unique_id_data.unique_id_data(zone_id, id)

  @property
  def direction(self):
    return self._direction
  @property
  def destination(self):
    return self._destination

  @property
  def zone_id(self):
    return self.destination.zone_id
  @property
  def id(self):
    return self.destination.id

  @property
  def internal(self):
    return self.zone_id == None and self.id != None

  @direction.setter
  def direction(self, new_direction):
    self._direction = new_direction

  @destination.setter
  def destination(self, new_dest):
    self._destination = new_dest

  @zone_id.setter
  def zone_id(self, new_zone_id):
    # sanity check handled internally to unique_id_data class
    self.destination.zone_id = new_zone_id

  @id.setter
  def id(self, new_id):
    # sanity check handled internally to unique_id_data class
    self.destination.id = new_id


