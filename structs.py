import dataclasses
import config
import enum
import logging
import typing

# for cleaner type hints
function = typing.NewType('function', typing.Any)

@dataclasses.dataclass
class client:
  """ttype  = client name
     width  = width of terminal window
     length = length of terminal window"""
  term_type:   str=None
  term_width:  int=None
  term_length: int=None
  host_name:   str=None


@dataclasses.dataclass
class entity:
  """name     = what to be referred to as
     namelist = list of keywords to be targetted with
     desc     = shown when closely examined
     ldesc    = when seen in a room
     room     = virtual number if directly in a room"""
  name:     str="an unfinished entity"
  # make sure they each get their own copy of the the namelist, not the same namelist
  namelist: list=dataclasses.field(default_factory=lambda:["unfinished", "entity"])
  desc:     str="It looks unfinished."
  ldesc:    str="An unfinished entity rests here."

  @property
  def Name(self):
    return self.name.capitalize()

  def has_alias(self, alias):
    return alias in self.namelist

@dataclasses.dataclass
class preferences:
  screen_width:  int=config.DEFAULT_SCREEN_WIDTH
  screen_length: int=config.DEFAULT_SCREEN_LENGTH
  color_mode:    str=config.DEFAULT_COLOR_MODE
  active_idle:   str=config.DEFAULT_ACTIVE_IDLE
  brief_mode:    str=config.DEFAULT_BRIEF_MODE
  debug_mode:    int=config.DEFAULT_DEBUG_MODE

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

@dataclasses.dataclass
class special_procedure:
  """name = representation as a string
     func = behaviour function -- returns a set of spec_proc_features with None taken to be empty"""
  name: str="an unnamed spec proc"
  func: function=None

class spec_proc_features(enum.IntEnum):
  BLOCK_INTERPRETER = 1 # command that triggered spec proc is not processed by the command line interpreter
  BLOCK_OTHER_SPECS = 2 # subsequent special procedures are ignored

