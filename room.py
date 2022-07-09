import enum
import object
import pc

from color import *

class direction(enum.IntEnum):
  NORTH = 0
  EAST  = 1
  SOUTH = 2
  WEST  = 3
  UP    = 4
  DOWN  = 5

class exit:
  def __init__(self, dir, vnum):
    self._direction = dir
    self._vnum = vnum

  @property
  def direction(self):
    return self._direction
  @property
  def vnum(self):
    return self._vnum

class room:
  """Creates a new room which may be occupied by characters and objects (eventually)
      name     = the title of the room (displayed first as one line)
      vnum     = key to access rooms as values in the in game.world dictionary
      desc     = the longer description of the room (shown as a following paragraph)
      exits    = exits in the cardinal directions leading to other rooms (identified by vnum)
      people   = list of characters in the room
      contents = list of objects on the ground"""
  def __init__(self):
    self._name      = "Unfinished Room"
    self._vnum      = None
    self._desc      = "  It looks unfinished."
    self._exits     = [ ]
    self._people    = [ ]
    self._inventory = object.inventory()

  # Getters
  @property
  def name(self):
    return self._name
  @property
  def vnum(self):
    return self._vnum
  @property
  def desc(self):
    return self._desc
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
  @name.setter
  def name(self, new_name):
    self._name = new_name
  @vnum.setter
  def vnum(self, new_vnum):
    self._vnum = new_vnum
  @desc.setter
  def desc(self, new_desc):
    self._desc = new_desc

  """add_char(ch)         <-
     remove_char(ch)      <-
     char_by_name(ch)     <-
     pc_by_name(name)     <-
     npc_by_alias(alias)  <-
     connect(dir, dest)   <-
     disconnect(dir)      <-
     list_exits()         <-
     show_exits()         <-
     echo(msg)            <-
     get_destination(dir) <-
     exit_exists(dir)     <-"""
  def add_char(self, ch):
    ch.room = self.vnum
    self._people.append(ch)

  def remove_char(self, ch):
    ch.room = None
    self._people.remove(ch)

  def char_by_name(self, name):
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

  def connect(self, direction, destination):
    self._exits.append(exit(direction, destination))

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

  def get_destination(self, direction):
    for ex in self._exits:
      if direction == ex.direction:
        return ex.vnum
    return None

  def exit_exists(self, direction):
    return self.get_destination(direction) != -1