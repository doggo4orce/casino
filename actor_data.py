import behaviour_data
import cmd_trig_data

class actor_data:
  def __init__(self, behaviour=None):
    self._behaviour = behaviour_data.behaviour_data()

    if behaviour != None:
      for proc in behaviour.prefix_cmd_trigs():
        self._behaviour.assign_proc(proc)
      for proc in behaviour.suffix_cmd_trigs():
        self._behaviour.assign_proc(proc)
      for proc in behaviour.hbeat_procs():
        self._behaviour.assign_proc(proc)

  """assign_proc(spec_proc)     <- assign spec proc to behaviour
     assign_procs(spec_procs)   <- assign list of procs to behaviour
     copy_from(actor)           <- copy behaviour from actor
     remove_procs()             <- remove all procs from behaviour
     copy_from(actor)           <- copy actor fields
     call_prefix_triggers(args) <- calls all prefix_cmd_trigs
     call_suffix_triggers(args) <- calls all suffix_cmd_trigs
     call_hbeat_procs(args)     <- calls all hbeat_procs"""

  def assign_proc(self, spec_proc):
    self._behaviour.assign_proc(spec_proc)

  def assign_procs(self, spec_procs):
    for spec_proc in spec_procs:
      self._behaviour.assign_proc(spec_proc)

  def copy_from(self, actor):
    self._behaviour.copy_from(actor._behaviour)

  def remove_procs(self):
    self._behaviour.remove_all_procs()

  def call_prefix_cmd_trigs(self, mud, ch, command, argument, db):
    block_interpreter = False
    for proc in self._behaviour.prefix_cmd_trigs:
      if proc.call(mud, self, ch, command, argument, db) == cmd_trig_data.prefix_cmd_trig_messages.BLOCK_INTERPRETER:
        # we let other procs fire before blocking
        block_interpreter = True
    return block_interpreter

  def call_suffix_cmd_trigs(self, mud, ch, command, argument, db):
    for proc in self._behaviour.suffix_cmd_trigs:
      proc.call(mud, self, ch, command, argument, db)

  def call_hbeat_procs(self, mud, db):
    for proc in self._behaviour.hbeat_procs:
      proc.call(mud, self, db)

  def debug(self):
    ret_val = self._behaviour.debug()
    return ret_val