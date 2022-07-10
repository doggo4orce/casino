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
     pc_save_data_numerical or pc_save_data_non_numerical
   will be automatically saved."""
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

