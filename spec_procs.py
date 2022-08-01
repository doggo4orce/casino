import dataclasses
import enum
import typing

# for cleaner type hints
function = typing.NewType('function', typing.Any)

@dataclasses.dataclass
class prefix_command_trigger:
  """name = representation as a string
     func = behaviour function -- returns one of the messages below"""
  name: str="an unnamed spec proc"
  func: function=None

@dataclasses.dataclass
class suffix_command_trigger:
  """name = representation as a string
     func = behaviour function -- returns one of the messages below"""
  name: str="an unnamed spec proc"
  func: function=None

"""These are messages which may be returned by prefix_command_trigger.func when called by
   interpret_msg() in nanny.py.  Depending on whether and how much this list of
   messages grows, command_trigger.func might be adjusted to return a set
   TODO: consider using exceptions instead?"""
class prefix_command_trigger_messages(enum.IntEnum):
  BLOCK_INTERPRETER = 1 # command to be ignored by the command line interpreter

@dataclasses.dataclass
class heart_beat_proc:
  """name = representation as a string
     func = behaviour function"""
  name: str="an unnamed spec proc"
  func: function=None