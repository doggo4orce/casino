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
     desc     = shown when closely examined
     room     = reference to room if it is in one, and None otherwise"""
  name:     str="an unfinished entity"
  # make sure they each get their own copy of the the namelist, not the same namelist
  namelist: list=dataclasses.field(default_factory=lambda:["unfinished", "entity"])
  desc:     editor.buffer=editor.buffer("It looks unfinished.")
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
  room_desc:   editor.buffer=editor.buffer("You are in an unfinished room.")
  room_exits:  dict=dataclasses.field(default_factory=lambda:dict())
  dir_edit:    int=None

@dataclasses.dataclass
class medit_save_data:
  """ fill this in when medit is developed """
  pass

@dataclasses.dataclass
class oedit_save_data:
  """ fill this in when oedit is developed """
  pass

@dataclasses.dataclass
class olc_data:
  """Interface for descriptor to work with their OLC data
     mode      = which mode, redit, zedit, etc.
     zone_id   = zone_id of room/obj/npc being editted
     state     = which state in the menu system are you in
     save_data = temporary parking space for OLC data specific to the object being edited"""
  mode:      int=None
  state:     int=None
  changes:   bool=True
  save_data: ...=None

@dataclasses.dataclass
class pref_data:
  def get(self, field):
    if hasattr(self, field):
      return getattr(self, field)
    else:
      logging.warning(f"Trying to access preference field {field} which is not defined.")

  def set(self, field, value):
    if hasattr(self, field):
      setattr(self, field, value)
    else:
      logging.warning(f"Trying to set {field} to {value}, but {field} is not defined.")

@dataclasses.dataclass
class pref_data_numeric(pref_data):
  screen_width:  int=config.DEFAULT_SCREEN_WIDTH
  screen_length: int=config.DEFAULT_SCREEN_LENGTH

@dataclasses.dataclass
class pref_data_text(pref_data):
  color_mode:    str=config.DEFAULT_COLOR_MODE

@dataclasses.dataclass
class pref_data_flags(pref_data):
  active_idle:   int=config.DEFAULT_ACTIVE_IDLE
  brief_mode:    int=config.DEFAULT_BRIEF_MODE
  debug_mode:    int=config.DEFAULT_DEBUG_MODE

  def set(self, field, val):
    if val not in [0,1]:
      logging.warning(f"set function called on {field} flag with value {val} which is neither 0 nor 1.")
    else:
      super().set(self, field, str)

  def flip(self, field):
    if getattr(self, field) == True:
      setattr(self, field, False)
    elif getattr(self, field) == False:
      setattr(self, field, True)
    else:
      logging.warning(f"switch function called on {field}, which was neither on nor off, turning off.")
      setattr(self, field, False)

@dataclasses.dataclass
class preferences:
  numeric: pref_data_numeric=dataclasses.field(default_factory=lambda:pref_data_numeric())
  text:    pref_data_text=dataclasses.field(default_factory=lambda:pref_data_text())
  flags:   pref_data_flags=dataclasses.field(default_factory=lambda:pref_data_flags())

  def set(self, field, value):
    if hasattr(field, self.numeric):
      self.numeric.set(field, value)
    elif hasattr(field, self.text):
      self.text.set(field, value)
    elif hasattr(field, self.flags):
      self.flags.set(field, value)
    else:
      logging.warning(f"trying to set {field} to {value} but {field} is not defined.")

  def flip(self, field):
    if hasattr(field, self.flags):
      self.flags.flip(field)

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
    # TODO: write buffer.parse() function to take over here
    elif tag == "desc":
      self.entity.desc = editor.buffer()
      line = ""
      while line != "~":
        line = rf.readline()
        line = line.rstrip()
        if line != "~":
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
    ret_val += self.entity.desc.display(width=65, indent=True)
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
    # TODO: write buffer.parse() function to take over here
    elif tag == "desc":
      line = ""
      self.entity.desc = editor.buffer()
      while line != "~":
        line = rf.readline()
        line = line.rstrip()
        if line != "~":
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
  desc: editor.buffer=editor.buffer("undescribed room")

if __name__ == '__main__':
  pref = preferences()

  print(pref.numeric.__dataclass_fields__)
