# once this is done, make sure all of this is factored out of room and redit_save_data
# remember desc is stored as a string, so go and look at the places where buffers are
# used and make sure this class is never expected to give a buffer

# sept 24, 2024, finished transferring code here from room.py
# but now realize i should test exit thoroughly first
# switching to that for now

class room_attribute_data:
  """Creates a room_attribute_data object to store static room data.
      name  = name of the room
      desc  = description of room, stored as a string
      exits = cardinal directions leading to other rooms (identified by vref)"""
  def __init__(self, name=None, desc=None)
    self.name = name
    self.desc = desc
    # change this to a list of exits, and have exits themselves keep track of the associated direction?
    # maybe?
    self.exits = dict()

  @property
  def name(self):
    return self._name

  @property
  def desc(self):
    return self._desc

  @property
  def exits(self):
    return self._exits

  @name.setter
  def name(self, new_name):
    self._name = new_name

  @desc.setter
  def desc(self, new_desc):
    self._desc = new_desc

  @exits.setter
  def exits(self, new_exits):
    for key, value in new_exits.items():
      self.connect(key, value)

  """connect(dir, dest)        <- creates exit to room with vref string dest through direction dir
     disconnect(dir)           <- removes exit with direction dir
     list_exits()              <- shows exit letters, e.g. n s w 
     show_exits()              <- shows exit string, e.g. [ Exits: n s w ]
     exit(dir)                 <- returns exit object leading in direction dir or None
     get_destination(dir)      <- returns vref for room that the exit in direction dir leads to
     exit_exists(dir)          <- checks if the room has an exit leading in direction dir
     direction(self, ex)       <- returns direction of room exit, or None"""

  def connect(self, direction, destination_code):
    # check if we're already connected
    ex = self.exit(direction)
    if ex != None:
      self.disconnect(direction)
    self._exits[direction] = exit.exit(destination_code)

  def disconnect(self, direction):
    if self.exit(direction):
      del self.exits[direction]

  def list_exits(self):
    exit_str = ""
    if len(self.exits) == 0:
      return "None! "
    for dir, ex in self.exits.items():
      exit_str = exit_str + dir.name[0].lower() + ' '
    return exit_str

  def show_exits(self):
    return "[ Exits: {}]".format(self.list_exits())

  def exit(self, direction):
    if direction in self.exits.keys():
      return self.exits[direction]
    return None

  def get_destination(self, direction):
    exit = self.exit(direction)
    if exit == None:
      return None
    return exit.destination

  def exit_exists(self, direction):
    return self.get_destination(direction) != None

  def direction(self, ex):
    direction = None

    # what direction does the exit lead in?
    for dir in exit.direction:
      if self.exit(dir) is ex:
        direction = dir
    
    return direction
