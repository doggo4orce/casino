import dataclasses
import enum
import inspect
import logging
import string_handling
import typing

class spec_proc:
  func_args = []
  """name = representation as a string
     fn   = behaviour function, may return messages"""
  def __init__(self, name, fn):
    self._name = name
    self._func = fn

  def first_fn_arg_error_brief(self):
    actual_args = inspect.getfullargspec(self.func).args
    for idx, arg in enumerate(command_trigger.func_args):
      if actual_args[idx] != arg:
        return f"expecting '{arg}' for {string_handling.ordinal(idx+1)} arg but found '{actual_args[idx]}'"
    return None

  def first_fn_arg_error_full(self):
    arg_error = self.first_fn_arg_error_brief()
    problems = list()
    if arg_error != None:
      problems.append(f"Error: spec_proc({self.name})")
      problems.append(f"  arg error with self.func={self.func.__name__}")
      problems.append(f"  {arg_error}")
    return problems

  def correct_fn_args(self):
    return self.first_fn_arg_error_brief() == None

  @property
  def name(self):
    return self._name
  @property
  def func(self):
    return self._func

  @name.setter
  def name(self, new_name):
    self._name = new_name
  @func.setter
  def func(self, new_func):
    self._func = new_func

class command_trigger(spec_proc):

  # this must be the prototype for all command trigger functions
  func_args = ['mud', 'me', 'ch', 'command', 'argument']

  def __init__(self, name, func):
    super().__init__(name, func)

  def call(self, mud, me, ch, command, argument):
    return self.func(mud, me, ch, command, argument)

class prefix_command_trigger(command_trigger):
  pass

class suffix_command_trigger(command_trigger):
  pass

"""These are messages which may be returned by func for prefix
   command trigger procs when called by interpret_msg() in nanny.py.  
   Depending on whether and how much this list of messages grows, 
   command_trigger.func might be adjusted to return a set
   TODO: consider using exceptions instead?"""
class prefix_command_trigger_messages(enum.IntEnum):
  BLOCK_INTERPRETER = 1 # blocks command and all suffix_command_triggers

class heart_beat_proc(spec_proc):
  # this must be the prototype for all command trigger functions
  func_args = ['mud', 'me']

  def __init__(self, name, func):
    super().__init__(name, func)

  def call(self, mud, me):
    return self.func(mud, me)
