from color import *
import enum
import object
import pc
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

class room:
  """Creates a new room which may be occupied by characters and objects (eventually)
      unique_id = for easy look-up, of the form zone[room]
      exits     = exits in the cardinal directions leading to other rooms (identified by vnum)
      people    = list of characters in the room
      contents  = list of objects on the ground"""
  def __init__(self):
    self._unique_id = structs.unique_identifier()
    self._attributes = structs.room_attribute_data("Unfinished Room", "It looks unfinished.")
    self._exits     = [ ]
    self._people    = [ ]
    self._inventory = object.inventory()

  # Getters
  @property
  def attributes(self):
    return self._attributes
  @property
  def name(self):
    return self.attributes.name
  @property
  def unique_id(self):
    return self._unique_id
  @property
  def id(self):
    return self._unique_id.id
  @property
  def zone_id(self):
    return self._unique_id.zone_id
  @property
  def desc(self):
    return self._attributes.desc
  @property
  def exits(self):
    return self._exits
  @property
  def people(self):
    return self._people
  @property
  def inventory(self):
    return self._inventory

  # Setters
  @attributes.setter
  def attributes(self, new_attributes):
    self._attributes = new_attributes
  @name.setter
  def name(self, new_name):
    self._attributes.name = new_name
  @unique_id.setter
  def unique_id(self, new_unique_id):
    self._unique_id = new_unique_id
  @id.setter
  def id(self, new_id):
    self._unique_id.id = new_id
  @zone_id.setter
  def zone_id(self, new_zone_id):
    self._unique_id.zone_id = new_zone_id
  @desc.setter
  def desc(self, new_desc):
    self._attributes.desc = new_desc

  """add_char(ch)          <- adds character ch from the room      (does not modify ch.room)
     remove_char(ch)       <- removes character ch from the room   (does not modify ch.room)
     char_by_alias(name)   <- scans through people in room looking for character with name, prioritizes pc's
     pc_by_name(name)      <- scans through pcs in room with argument as name
     npc_by_alias(alias)   <- scans through npcs in room with argument as alias
     connect(dir, dest)    <- creates exit to room with code dest through direction dir
     disconnect(dir)       <- removes exit with direction dir
     list_exits()          <- shows exit letters, e.g. n s w 
     parse_tag(tag, value) <- used to iterate through .room files
     show_exits()          <- shows exit string, e.g. [ Exits: n s w ]
     echo(msg)             <- sends msg to every character in the room
     exit(dir)             <- returns exit object leading in direction dir
     get_destination(dir)  <- returns code for room that the exit in direction dir leads to
     exit_exists(dir)      <- checks if the room has an exit leading in direction dir"""
  def add_char(self, ch):
    ch.room = f"{self.zone_id}[{self.id}]"
    self._people.append(ch)

  def remove_char(self, ch):
    ch.room = None
    self._people.remove(ch)

  def char_by_alias(self, name):
    # first check for pc
    tch = self.pc_by_name(name)
    if tch != None:
      return tch
    # if nothing found, then check for npc
    tch = self.npc_by_alias(name)
    if tch != None:
      return tch
    # by now we have nothing
    return None

  def pc_by_name(self, name):
    for ch in self._people:
      if isinstance(ch, pc.pc) and ch.name.lower() == name:
        return ch

  def npc_by_alias(self, alias):
    for ch in self._people:
      if isinstance(ch, pc.npc) and alias in ch.entity.namelist:
        return ch

  def connect(self, direction, destination_code):
    # if it's a local exit, prepend the zone_id
    if destination_code.find('[') == -1:
      destination_code = f"{self.zone_id}[{destination_code}]"
    self._exits.append(exit(direction, destination_code))

  def disconnect(self, direction):
    target = False
    for ex in self._exits:
      if ex.direction == direction:
        target = ex; break
    if target:
      self._exits.remove(target)

  def list_exits(self):
    exit_str = ""
    if len(self._exits) == 0:
      return "None! "
    for ex in self._exits:
      exit_str = exit_str + ex.direction.name[0].lower() + ' '
    return exit_str

  def show_exits(self):
    return "[ Exits: {}]".format(self.list_exits())

  def echo(self, msg, **kwargs):
    exceptions = list()

    if "exceptions" in kwargs:
      exceptions = kwargs["exceptions"]

    for ch in self._people:
      if ch not in exceptions:
        ch.write(msg)

  def exit(self, direction):
    for ex in self._exits:
      if direction == ex.direction:
        return ex
    return None

  def parse_tag(self, tag, value):
    dir_tags = [dir.name for dir in direction]

    if tag == "id":
        self.unique_id.id = value
    elif tag.upper() in dir_tags:
      # found an exit
      self.connect(direction(direction[tag.upper()]), value)
    # name, desc
    elif hasattr(self.attributes, tag):
      setattr(self.attributes, tag, value)
    else:
      pass# change the line below to throwing an exception
      #logging.warning(f"Ignoring {value} from unrecognized tag {tag} while parsing {rf.name}.")

  def get_destination(self, direction):
    exit = self.exit(direction)
    if exit == None:
      return None
    return exit.destination

  def exit_exists(self, direction):
    return self.get_destination(direction) != -1

  def __str__(self):
    ret_val = f"Name: {CYAN}{self.name}{NORMAL}\r\n"
    ret_val += f"Description:\r\n{string_handling.paragraph(self.desc, 65, True)}\r\n"
    ret_val += "Exits:\r\n"

    for ex in self.exits:
      ret_val += "  " + str(ex)

    return ret_val