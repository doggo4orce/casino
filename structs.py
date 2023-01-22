from color import *
import dataclasses
import config
import editor
import enum
import logging
import object
import olc
import spec_procs
import string_handling

# (should this be moved?) rooms, npcs, and objects are referenced  by a string of the form: zone_id[id],
@dataclasses.dataclass
class unique_identifier:
  zone_id: str=None
  id:      str=None

  def update(self, zone_id, id):
    self.zone_id = zone_id
    self.id = id

  @classmethod
  def from_string(cls, ref_string):
    zone_id, id = string_handling.parse_reference(ref_string)
    return unique_identifier(zone_id, id)
    
  def __str__(self):
    return f"{self.zone_id}[{self.id}]"

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
     room     = reference to room if it is in one, and None otherwise"""
  name:     str="an unfinished entity"
  # make sure they each get their own copy of the the namelist, not the same namelist
  namelist: list=dataclasses.field(default_factory=lambda:["unfinished", "entity"])
  desc:     editor.display_buffer=editor.display_buffer("It looks unfinished.")
  room:     unique_identifier=dataclasses.field(default_factory=lambda:unique_identifier.from_string(config.VOID_ROOM))

  @property
  def Name(self):
    return self.name.capitalize()

  def has_alias(self, alias):
    return alias in self.namelist

@dataclasses.dataclass
class zedit_save_data:
  """There should be a field here for each of the fields in the main menu for redit.  Then the users
     selection for those fields can be saved here locally until they finish OLC and make their changes permanent.
     their changes and make them permanent."""
  id:          str=None
  zone_name:   str=None
  zone_author: str=None
  zone_folder: str=None

@dataclasses.dataclass
class redit_save_data:
  """There should be a field here for each of the fields in the main menu for redit.  Then the users
     selection for those fields can be saved here locally until they finish OLC and make their changes permanent.
     uid        = unique identifier of room being edited
     room_name  = name of room being edited
     room_desc  = description of room being edited
     room_exits = dictionary of exit vrefs using directions as keys
     dir_edit   = direction specified on previous command to edit an exit"""
  uid:         unique_identifier=None
  room_name:   str="An unfinished room"
  room_desc:   editor.display_buffer=editor.display_buffer("You are in an unfinished room.")
  room_exits:  dict=dataclasses.field(default_factory=lambda:dict())
  dir_edit:    int=None

@dataclasses.dataclass
class medit_save_data:
  """  """
  pass

@dataclasses.dataclass
class olc_data:
  """Interface for descriptor to work with their OLC data
     mode     = which mode, redit, zedit, etc.
     zone_id  = zone_id of room/obj/npc being editted
     state    = which state in the menu system are you in
     data     = temporary parking space for OLC data specific to the object being edited"""
  mode:      int=None
  state:     int=None
  changes:   bool=False
  save_data: ...=None

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

@dataclasses.dataclass # perhaps this should be moved to pc.py
class npc_proto_data:
  entity: entity_data = dataclasses.field(default_factory=lambda:entity_data())
  ldesc: str="An unfinished npc proto_type stands here."
  prefix_command_triggers: list = dataclasses.field(default_factory=lambda:list())
  suffix_command_triggers: list = dataclasses.field(default_factory=lambda:list())
  heart_beat_procs: list = dataclasses.field(default_factory=lambda:list())
  unique_id: unique_identifier = dataclasses.field(default_factory=lambda:unique_identifier())

  # factor an entity.parse_tag function out of all these similar parse_tag functions
  def parse_tag(self, tag, value, rf):
    # name, namelist, desc, ldesc
    if tag == "id":
      self.unique_id.id = value
    elif tag == "ldesc":
      self.ldesc = value
    elif tag == "namelist":
      self.entity.namelist = value.split(' ')
    elif tag == "desc":
      self.entity.desc = editor.display_buffer()
      line = ""
      while line != "~\n":
        line = rf.readline()
        if line != "~\n":
          self.entity.desc.add_line(line)
        else:
          break;
    elif hasattr(self.entity, tag):
      setattr(self.entity, tag, value)
    else:
      logging.warning(f"Ignoring {value} from unrecognized tag {tag} while parsing {rf.name}.")

  def assign_spec_proc(self, spec_proc):
    # will return an empty list() if the function args are correct
    problems = spec_proc.first_fn_arg_error_full()
    for problem in problems:
      logging.warning(problem)
    if len(problems) > 0:
      return
    if type(spec_proc) == spec_procs.prefix_command_trigger:
      self.prefix_command_triggers.append(spec_proc)
    elif type(spec_proc) == spec_procs.suffix_command_trigger:
      self.suffix_command_triggers.append(spec_proc)
    elif type(spec_proc) == spec_procs.heart_beat_proc:
      self.heart_beat_procs.append(spec_proc)
  
  def __str__(self):
    ret_val = f"NPC: {CYAN}{self.entity.name}{NORMAL} "
    ret_val += f"Alias: {CYAN}"
    for name in self.entity.namelist:
      ret_val += name + " "
    ret_val += f"{NORMAL}\r\n"
    self.entity.desc.proc_p_tags(width=65)
    ret_val += f"Desc:\r\n{self.entity.desc.str()}\r\n"
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
    elif tag == "namelist":
      self.entity.namelist = value.split(' ')
    # eventually I can factor this through display_buffer.parse?
    elif tag == "desc":
      line = ""
      self.entity.desc = editor.display_buffer()
      while line != "~\n":
        line = rf.readline()
        if line != "~\n":
          self.entity.desc.add_line(line)
        else:
          break;

    elif hasattr(self.entity, tag):
      setattr(self.entity, tag, value)
    else:
      logging.warning(f"Ignoring {value} from unrecognized tag {tag} while parsing {rf.name}.")

  @property
  def id(self):
    return self.unique_id.id
  @property
  def zone_id(self):
    return self.unique_id.zone_id

@dataclasses.dataclass
class room_attribute_data:
  """name      = the title of the room (displayed first as one line)
     desc      = the longer description of the room (shown as a following paragraph)"""
  name: str="unnamed room"
  desc: editor.display_buffer=editor.display_buffer("undescribed room")

if __name__ == '__main__':
  new_proto = obj_proto_data()

  new_obj = object.object()

  new_obj._entity = dataclasses.replace(new_proto.entity)

  print(new_obj.name)

  new_proto.entity.name = "finished entity"

  print(new_obj.name)
