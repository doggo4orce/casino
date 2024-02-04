import enum
import spec_proc_data

class cmd_trigger_data(spec_proc_data.spec_proc_data):
  """Command Triggers are called every time a player in the room enters a command
     mud = the mud object
     me = the character or object to which the trigger is attached
     ch = the player entering the command
     argument = full arguments following the command
     db = the main database"""
  expected_args = ['mud', 'me', 'ch', 'command', 'argument', 'db']

  def __init__(self, name, func):
    super().__init__(name, func)

"""These are messages which may be returned by func for prefix
   command trigger procs when called by interpret_msg() in nanny.py.  
   Depending on whether and how much this list (and maybe even other
   lists) of messages grow(s), command_trigger.func might be adjusted
   to return a set"""
class prefix_command_trigger_messages(enum.IntEnum):
  BLOCK_INTERPRETER = 1 # blocks command and all suffix_command_triggers
  RUN_INTERPRETER   = 2 # run command parser and any suffix_command_triggers

# fired on mobs in the room before command is processed
class prefix_command_trigger(cmd_trigger_data):
  pass

# fired on mobs in room after command is proceseed
class suffix_command_trigger(cmd_trigger_data):
  pass
