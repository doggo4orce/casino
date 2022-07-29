from color import *
import dataclasses
import config
import enum
import logging
import object
import string_handling
import typing

# for cleaner type hints
function = typing.NewType('function', typing.Any)

@dataclasses.dataclass
class client:
  """ttype     = client name
     width     = width of terminal window
     length    = length of terminal window
     host_name = name of client"""
  term_type:   str=None
  term_width:  int=None
  term_length: int=None
  host_name:   str=None

@dataclasses.dataclass
class entity_data:
  """name     = what to be referred to as
     namelist = list of keywords to be targetted with
     desc     = shown when closely examined (this should be moved since pc's dont need them)
     room     = reference to room if it is in one"""
  name:     str="an unfinished entity"
  # make sure they each get their own copy of the the namelist, not the same namelist
  namelist: list=dataclasses.field(default_factory=lambda:["unfinished", "entity"])
  desc:     str="It looks unfinished."
  room:     str=config.VOID_ROOM

  @property
  def Name(self):
    return self.name.capitalize()

  def has_alias(self, alias):
    return alias in self.namelist

@dataclasses.dataclass
class preferences:
  """Caution: any new fields added below will be automatically saved.  But unless an
     exception is added to load_char_by_name, as is done for screen_width and
     screen_length, they will be loaded as strings.  Depending on how many numerical
     values end up being added here, it may make sense to split this into two classes."""
  screen_width:  int=config.DEFAULT_SCREEN_WIDTH
  screen_length: int=config.DEFAULT_SCREEN_LENGTH
  color_mode:    str=config.DEFAULT_COLOR_MODE
  active_idle:   str=config.DEFAULT_ACTIVE_IDLE
  brief_mode:    str=config.DEFAULT_BRIEF_MODE
  debug_mode:    str=config.DEFAULT_DEBUG_MODE

  def set(self, field, value):
    setattr(self, field, value)

  def flip(self, field, on, off):
    if getattr(self, field) == on:
      setattr(self, field, off)
    elif getattr(self, field) == off:
      setattr(self, field, on)
    else:
      logging.warning(f"switch function called on {field}, which was neither {on} nor {off} - turning {off}.")
      setattr(self, field, off)

"""Note: any new fields added to
     pc_save_data_numerical or pc_save_data_non_numerical will be automatically saved."""
@dataclasses.dataclass
class pc_save_data_numerical:
  hp: int=1

@dataclasses.dataclass
class pc_save_data_strings:
  title: str=config.DEFAULT_TITLE

@dataclasses.dataclass
class pc_save_data:
  numerical: pc_save_data_numerical=dataclasses.field(default_factory=lambda:pc_save_data_numerical())
  non_numerical: pc_save_data_strings=dataclasses.field(default_factory=lambda:pc_save_data_strings())

@dataclasses.dataclass
class command_trigger:
  """name = representation as a string
     func = behaviour function -- returns one of the messages below"""
  name: str="an unnamed spec proc"
  func: function=None

"""These are messages which may be returned by command_trigger.func when called by
   interpret_msg() in nanny.py.  Depending on whether and how much this list of
   messages grows, command_trigger.func might be adjusted to return a set"""
class command_trigger_messages(enum.IntEnum):
  BLOCK_INTERPRETER = 1 # command to be ignored by the command line interpreter

@dataclasses.dataclass
class heart_beat_proc:
  """name = representation as a string
     func = behaviour function"""
  name: str="an unnamed spec proc"
  func: function=None

# rooms, npcs, and objects are referenced  by a string of the form: zone_id[id]
@dataclasses.dataclass
class unique_identifier:
  zone_id: str=None
  id:      str=None

  def update(self, zone_id, id):
    self.zone_id = zone_id
    self.id = id
    
  def __str__(self):
    return f"{self.zone_id}[{self.id}]"

@dataclasses.dataclass # perhaps this should be moved to pc.py
class npc_proto_data:
  entity: entity_data = dataclasses.field(default_factory=lambda:entity_data())
  ldesc: str="An unfinished npc proto_type stands here."
  command_triggers: list = dataclasses.field(default_factory=lambda:list())
  heart_beat_procs: list = dataclasses.field(default_factory=lambda:list())
  unique_id: unique_identifier = dataclasses.field(default_factory=lambda:unique_identifier())

  def parse_tag(self, tag, value, rf):
    # name, namelist, desc, ldesc
    if tag == "id":
      self.unique_id.id = value
    elif tag == "ldesc":
      self.ldesc = value
    elif hasattr(self.entity, tag):
      setattr(self.entity, tag, value)
    else:
      logging.warning(f"Ignoring {value} from unrecognized tag {tag} while parsing {rf.name}.")
  
  def __str__(self):
    ret_val = f"NPC: {CYAN}{self.entity.name}{NORMAL} "
    ret_val += f"Alias: {CYAN}"
    for name in self.entity.namelist:
      ret_val += name + " "
    ret_val += f"{NORMAL}\r\n"
    ret_val += f"Desc:\r\n{string_handling.paragraph(self.entity.desc, 65, True)}\r\n"
    ret_val += f"L-Desc: {self.entity.ldesc}\r\n"
    return ret_val

@dataclasses.dataclass
class obj_proto_data:
  entity: entity_data = dataclasses.field(default_factory=lambda:entity_data())
  ldesc: str="An unfinished obj proto_type has been left here."
  unique_id: unique_identifier = dataclasses.field(default_factory=lambda:unique_identifier())

  def parse_tag(self, tag, value, rf):
    if tag == "id":
      self.unique_id.id = value
    elif tag == "ldesc":
      self.ldesc = value
    elif hasattr(self.entity, tag):
      setattr(self.entity, tag, value)
    else:
      logging.warning(f"Ignoring {value} from unrecognized tag {tag} while parsing {rf.name}.")

"""name      = the title of the room (displayed first as one line)
   desc      = the longer description of the room (shown as a following paragraph)"""
@dataclasses.dataclass
class room_attribute_data:
  name: str="unnamed room"
  desc: str="undescribed room"

if __name__ == '__main__':
  new_proto = obj_proto_data()

  new_obj = object.object()

  new_obj._entity = dataclasses.replace(new_proto.entity)

  print(new_obj.name)

  new_proto.entity.name = "finished entity"

  print(new_obj.name)
