import cmd_trigger_data
import heartbeat_proc_data
from mudlog import mudlog, mudlog_type
import spec_proc_data

class behaviour_data:
  def __init__(self):
    self.prefix_command_triggers = list()
    self.suffix_command_triggers = list()
    self.heart_beat_procs = list()

  @property
  def prefix_command_triggers(self):
    return self._prefix_command_triggers
  @property
  def suffix_command_triggers(self):
    return self._suffix_command_triggers
  @property
  def heart_beat_procs(self):
    return self._heart_beat_procs

  @prefix_command_triggers.setter
  def prefix_command_triggers(self, new_triggers):
    self._prefix_command_triggers = new_triggers
  @suffix_command_triggers.setter
  def suffix_command_triggers(self, new_triggers):
    self._suffix_command_triggers = new_triggers
  @heart_beat_procs.setter
  def heart_beat_procs(self, new_triggers):
    self._heart_beat_procs = new_triggers

  def assign_spec_proc(self, spec_proc):
    if not spec_proc.consistent:
      mudlog(mudlog_type.ERROR, spec_proc.arg_error())
      return
    if isinstance(spec_proc, cmd_trigger_data.prefix_command_trigger):
      self.prefix_command_triggers.append(spec_proc)
    elif isinstance(spec_proc, cmd_trigger_data.suffix_command_trigger):
      self.suffix_command_triggers.append(spec_proc)
    elif isinstance(spec_proc, heartbeat_proc_data.heartbeat_proc_data):
      self.heart_beat_procs.append(spec_proc)
    else:
      mudlog(mudlog_type.ERROR, f"Assigning unrecognized spec_proc type: {spec_proc.name}.")

  def assign_spec_procs(self, spec_procs):
    for spec_proc in spec_procs:
      self.assign_spec_proc(spec_proc)