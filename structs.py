from color import *
import dataclasses
import config
import editor
import enum
import entity_data
import logging
import object_data
import olc
import spec_procs
import string_handling
import unique_id_data

@dataclasses.dataclass
class redit_save_data:
  """There should be a field here for each of the fields in the main menu for redit.  Then the users
     selection for those fields can be saved here locally until they finish OLC and make their changes permanent.
     uid        = unique identifier of room being edited
     room_name  = name of room being edited
     room_desc  = description of room being edited
     room_exits = dictionary of exit vrefs using directions as keys
     dir_edit   = direction specified on previous command to edit an exit"""
  uid:         unique_id_data.unique_id_data=None
  room_name:   str="An unfinished room"
  room_desc:   str="You are in an unfinished room."
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
      super().set(field, val)

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
  entity: entity_data.entity_data = dataclasses.field(default_factory=lambda:entity_data.entity_data())
  ldesc: str="An unfinished npc proto_type stands here."
  prefix_command_triggers: list = dataclasses.field(default_factory=lambda:list())
  suffix_command_triggers: list = dataclasses.field(default_factory=lambda:list())
  heart_beat_procs: list = dataclasses.field(default_factory=lambda:list())
  unique_id: unique_id_data.unique_id_data = dataclasses.field(default_factory=lambda:unique_id_data.unique_id_data())

  def __post_init__(self):
    self.entity.ldesc = "An unfinished npc proto_type stands here."

  # TODO: make this function accept list of spec_procs
  def assign_spec_proc(self, spec_proc):
    # will return an empty list() if the function args are correct
    problems = spec_proc.first_fn_arg_error_full()
    for problem in problems:
      logging.error(problem)
    if len(problems) > 0:
      return
    if type(spec_proc) == spec_procs.prefix_command_trigger:
      self.prefix_command_triggers.append(spec_proc)
    elif type(spec_proc) == spec_procs.suffix_command_trigger:
      self.suffix_command_triggers.append(spec_proc)
    elif type(spec_proc) == spec_procs.heart_beat_proc:
      self.heart_beat_procs.append(spec_proc)

  @property
  def id(self):
    return self.unique_id.id
  @property
  def zone_id(self):
    return self.unique_id.zone_id

  def __str__(self):
    ret_val = f"NPC: {CYAN}{self.entity.name}{NORMAL} "
    ret_val += f"Alias: {CYAN}"
    for name in self.entity.namelist:
      ret_val += name + " "
    ret_val += f"{NORMAL}\r\n"
    ret_val += self.entity.desc.display(width=65, indent=True)
    ret_val += f"Desc:\r\n{self.entity.desc.str()}\r\n"
    ret_val += f"L-Desc: {self.ldesc}\r\n"
    return ret_val

@dataclasses.dataclass
class room_attribute_data:
  """name      = the title of the room (displayed first as one line)
     desc      = the longer description of the room (shown as a following paragraph)"""
  name: str="unnamed room"
  desc: editor.buffer=editor.buffer("undescribed room")

if __name__ == '__main__':

  flag_prefs = pref_data_flags()
