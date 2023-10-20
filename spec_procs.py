import dataclasses
import enum
import inspect
import logging
import string_handling
import typing



# fired on mobs in the room before command is processed
class prefix_command_trigger(command_trigger):
  pass

# fired on mobs in room after command is proceseed
class suffix_command_trigger(command_trigger):
  pass

# TODO: fired when someone enters the room
class room_entry_trigger(command_trigger):
  pass

class heart_beat_proc(spec_proc):
  # this must be the prototype for all command trigger functions
  func_args = ['mud', 'me', 'db']

  def __init__(self, name, func):
    super().__init__(name, func)

  def call(self, mud, me, db):
    return self.func(mud, me, db)
