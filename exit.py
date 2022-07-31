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
    direction = 
    destination = """
  def __init__(self, dir, code):
    self._direction = dir

    zone_id, room_id = string_handling.parse_reference(code)
    
    self._destination = structs.unique_identifier(zone_id, room_id)

  @property
  def direction(self):
    return self._direction
  @property
  def zone(self):
    return self._destination.zone_id
  @property
  def room(self):
    return self._destination.id
  @property
  def destination(self):
    return f"{self.zone}[{self.room}]"

  def __str__(self):
    if self.local():
      return f"{self.direction.name.lower()}: {CYAN}{self.room}{NORMAL}\r\n"
    else:
      return f"{self.direction.name.lower()}: {CYAN}{self.zone}{NORMAL}[{CYAN}{self.room}{NORMAL}]\r\n"