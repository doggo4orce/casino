import enum
import spec_proc_data

"""These are messages which may be returned by func for prefix
   command trigger procs when called by interpret_msg() in nanny.py.  
   Depending on whether and how much this list of messages grows, 
   command_trigger.func might be adjusted to return a set"""
class prefix_command_trigger_messages(enum.IntEnum):
  BLOCK_INTERPRETER = 1 # blocks command and all suffix_command_triggers
  RUN_INTERPRETER   = 2 # run command parser and any suffix_command_triggers

class cmd_trigger_data(spec_proc_data.spec_proc_data):

  # this must be the prototype for all command trigger functions
  expected_args = ['mud', 'me', 'ch', 'command', 'argument', 'db']

  def __init__(self, name, func):
    super().__init__(name, func)