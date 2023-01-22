from color import *
import enum
import editor
import exit
import inventory
import object
import pc
import string_handling
import structs

class room:
  """Creates a new room which may be occupied by characters and objects (eventually)
      unique_id = for easy look-up, of the form zone[room]
      exits     = exits in the cardinal directions leading to other rooms (identified by vref)
      people    = list of characters in the room
      contents  = list of objects on the ground"""
  def __init__(self):
    self._unique_id = structs.unique_identifier()
    self._attributes = structs.room_attribute_data("Unfinished Room", "It looks unfinished.")
    self._exits     = dict()
    self._people    = list()
    self._inventory = inventory.inventory()

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

  """add_char(ch)              <- adds character ch from the room      (does not modify ch.room)
     remove_char(ch)           <- removes character ch from the room   (does not modify ch.room)
     char_by_alias(name)       <- scans through people (pc's first) looking for name
     pc_by_name(name)          <- scans through pcs in room with argument as name
     npc_by_alias(alias)       <- scans through npcs in room with argument as alias
     connect(dir, dest)        <- creates exit to room with vref string dest through direction dir
     disconnect(dir)           <- removes exit with direction dir
     list_exits()              <- shows exit letters, e.g. n s w 
     parse_tag(tag, value, rf) <- used to iterate through .room files via filestream rf
     show_exits()              <- shows exit string, e.g. [ Exits: n s w ]
     echo(msg)                 <- sends msg to every character in the room
     exit(dir)                 <- returns exit object leading in direction dir
     get_destination(dir)      <- returns vref for room that the exit in direction dir leads to
     exit_exists(dir)          <- checks if the room has an exit leading in direction dir
     save(path)                <- saves the room to a file with given path"""
  def add_char(self, ch):
    ch.room = self.unique_id
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
      if isinstance(ch, pc.pc) and ch.has_alias(name):
        return ch

  def npc_by_alias(self, alias):
    for ch in self._people:
      if isinstance(ch, pc.npc) and ch.has_alias(alias):
        return ch

  def connect(self, direction, destination_code):
    # check if we're already connected
    ex = self.exit(direction)
    if ex != None:
      self.disconnect(direction)
    self._exits[direction] = exit.exit(direction, destination_code)

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

  def echo(self, msg, **kwargs):
    exceptions = list()

    if "exceptions" in kwargs:
      exceptions = kwargs["exceptions"]

    for ch in self._people:
      if ch not in exceptions:
        ch.write(msg)

  def exit(self, direction):
    for dir, ex in self.exits.items():
      if direction == ex.direction:
        return ex
    return None

  def parse_tag(self, tag, value, rf):
    dir_tags = [dir.name for dir in exit.direction]

    if tag == "id":
      self.unique_id.id = value
    elif tag == "desc":
      self.desc = editor.display_buffer()
      line = ""
      while line != "~":
        line = rf.readline()
        line = line.strip()
        if line != "~":
          self.desc.add_line(line)
        else:
          break
    elif tag.upper() in dir_tags:
      self.connect(exit.direction(exit.direction[tag.upper()]), value)
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
    return self.get_destination(direction) != None

  # def save(self, path):
  #   with open(path, "w+") as wf:
  #     wf.write(f"Name: {self.name}\n")
  #     wf.write(f"id: {self.id}\n")
  #     wf.write(f"Desc:\n")
  #     wf.write(f"{self.desc.raw_str()}\n")
  #     wf.write(f"~\n")

  #     for ex in self._exits:
  #       wf.write(f"{ex.direction.name.capitalize()}: {ex.destination}")

        

  def __str__(self):
    ret_val = f"Name: {CYAN}{self.name}{NORMAL}\r\n"
    ret_val += f"Description:\r\n{string_handling.paragraph(self.desc, 65, True)}\r\n"
    ret_val += "Exits:\r\n"

    for ex in self.exits:
      ret_val += "  " + str(ex)

    return ret_val