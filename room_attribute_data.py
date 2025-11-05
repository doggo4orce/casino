from color import *
import exit_data
import mudlog
import unique_id_data

# once this is done, make sure all of this is factored out of room and redit_save_data
# remember desc is stored as a string, so go and look at the places where buffers are
# used and make sure this class is never expected to give a buffer

class room_attribute_data:
  """Creates a room_attribute_data object to store static room data.
      uid       = unique identifier of room
      name      = name of the room
      desc      = description of room, stored as a string
      exits     = cardinal directions leading to other rooms"""
  def __init__(self, zone_id=None, id=None, name=None, desc=None):
    self.uid = unique_id_data.unique_id_data(zone_id, id)
    self.name = name
    self.desc = desc
    self._exits = list()

  @property
  def uid(self):
    return self._uid

  @property
  def id(self):
    return self.uid.id

  @property
  def zone_id(self):
    return self.uid.zone_id

  @property
  def name(self):
    return self._name

  @property
  def desc(self):
    return self._desc

  @property
  def exits(self):
    return self._exits

  @uid.setter
  def uid(self, new_uid):
    self._uid = new_uid

  @id.setter
  def id(self, new_id):
    self.uid.id = new_id

  @zone_id.setter
  def zone_id(self, new_zone_id):
    self.uid.zone_id = new_zone_id

  @name.setter
  def name(self, new_name):
    self._name = new_name

  @desc.setter
  def desc(self, new_desc):
    self._desc = new_desc

  """connect(dir, zone_id, id) <- creates exit to room with zone_id and id
     connect(dir, uid)         <- creates exit to room with uid
     disconnect(dir)           <- removes exit in specified dir
     exit_letters              <- shows all exits abbreviated as letters "n s w" 
     display_exits             <- displays all exits in string "[ Exits: n s w ]"
     num_exits                 <- number of exits connected
     exit(dir)                 <- returns exit object leading in dir
     has_exit(dir)             <- checks if the room has an exit leading in direction dir
     destination(dir)          <- returns uid of room dir leads to"""

  def connect(self, direction, *args):
    if len(args) == 1:
      zone_id = args[0].zone_id
      id = args[0].id
    elif len(args) == 2:
      zone_id = args[0]
      id = args[1]
    else:
      mudlog.error(f"Bad arguments {', '.join(args)} passed to method room_attributes.connect")

    # cant have an exit without a direction
    if direction is None:
      warning = f"Trying to connect room {self.zone_id}:{self.id} in non-existant direction."
      mudlog.mudlog(mudlog.mudlog_type.WARNING, warning)
      return

    # neither zone_id nor id can be null
    if id is None or zone_id is None:
      warning = f"Trying to connect {self.zone_id}:{self.id} ({exit_data.direction(direction).name[0]}) to non-existant room."
      mudlog.warning(warning)
      return

    # in case we're already connected
    self.disconnect(direction)

    # perform the connection
    self._exits.append(exit_data.exit_data(direction, zone_id, id))

  # def connect(self, direction, zone_id, id):
  #   # cant have an exit without a direction
  #   if direction == None:
  #     warning = f"Trying to connect room {self.zone_id}:{self.id} in non-existant direction."
  #     mudlog.mudlog(mudlog.mudlog_type.WARNING, warning)
  #     return

  #   # zone_id can be null, but not id
  #   if id == None:
  #     warning = f"Trying to connect {self.zone_id}:{self.id} ({exit_data.direction(direction).name[0]}) to non-existant room."
  #     mudlog.mudlog(mudlog.mudlog_type.WARNING, warning)
  #     return

  #   # in case we're already connected
  #   self.disconnect(direction)

  #   # perform the connection
  #   self._exits.append(exit_data.exit_data(direction, zone_id, id))

  def disconnect(self, direction):
    # if we're connected
    for ex in self.exits:
      if ex.direction == direction:
        # then disconnect
        self.exits.remove(ex)

  @property
  def exit_letters(self):
    exit_str = ""
    if len(self.exits) == 0:
      return "None! "

    for dir in exit_data.direction:
      if self.has_exit(dir):
        exit_str = exit_str + dir.name[0].lower() + ' '

    return exit_str

  @property
  def display_exits(self):
    return f"[ Exits: {self.exit_letters}]"

  @property
  def num_exits(self):
    return len(self._exits)

  def exit(self, direction):
    for ex in self.exits:
      if ex.direction == direction:
        return ex

  def has_exit(self, direction):
    return self.exit(direction) != None

  def destination(self, direction):
    ex = self.exit(direction)
    if ex == None:
      return None
    return ex.destination

  def debug(self):
    ret_val = f"UID: {CYAN}{self.uid}{NORMAL}\r\n"
    ret_val += f"Name: {CYAN}{self.name}{NORMAL}\r\n"
    ret_val += f"Desc: {CYAN}{self.desc}{NORMAL}\r\n"

    for ex in self._exits:
      ret_val += ex.debug()

    return ret_val




