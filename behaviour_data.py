import cmd_trig_data
from color import *
import hbeat_proc_data
from mudlog import mudlog, mudlog_type
import spec_proc_data

class behaviour_data:
  """Stores all special procedures for a room/object/character.
     prefix_cmd_trigs = triggered by commands processed before command
     suffix_cmd_trigs = triggered by commands, processed after command
     hbeat_procs = heartbeat procs, called once every heartbeat"""
  def __init__(self):
    self.prefix_cmd_trigs = list()
    self.suffix_cmd_trigs = list()
    self.hbeat_procs = list()

  @property
  def prefix_cmd_trigs(self):
    return self._prefix_cmd_trigs
  @property
  def suffix_cmd_trigs(self):
    return self._suffix_cmd_trigs
  @property
  def hbeat_procs(self):
    return self._hbeat_procs

  @prefix_cmd_trigs.setter
  def prefix_cmd_trigs(self, new_triggers):
    self._prefix_cmd_trigs = new_triggers
  @suffix_cmd_trigs.setter
  def suffix_cmd_trigs(self, new_triggers):
    self._suffix_cmd_trigs = new_triggers
  @hbeat_procs.setter
  def hbeat_procs(self, new_triggers):
    self._hbeat_procs = new_triggers

  def assign(self, spec_proc):
    if not spec_proc.consistent:
      msg = f"Assignment of inconsistent spec_proc '{spec_proc.name}'."
      mudlog(mudlog_type.ERROR, msg)
      return
    if isinstance(spec_proc, cmd_trig_data.prefix_cmd_trig_data):
      self.prefix_cmd_trigs.append(spec_proc)
    elif isinstance(spec_proc, cmd_trig_data.suffix_cmd_trig_data):
      self.suffix_cmd_trigs.append(spec_proc)
    elif isinstance(spec_proc, hbeat_proc_data.hbeat_proc_data):
      self.hbeat_procs.append(spec_proc)
    else:
      mudlog(mudlog_type.ERROR, f"Assignment of unrecognized spec_proc type: '{spec_proc.name}'.")

  def assign_spec_procs(self, spec_procs):
    for spec_proc in spec_procs:
      self.assign_spec_proc(spec_proc)

  def debug(self):
    p_cmd_trigs = ' '.join([spec.name for spec in self.prefix_cmd_trigs])
    s_cmd_trigs = ' '.join([spec.name for spec in self.suffix_cmd_trigs])
    h_procs = ' '.join([spec.name for spec in self.hbeat_procs])

    if len(p_cmd_trigs) == 0:
      p_cmd_trigs = "None"
    if len(s_cmd_trigs) == 0:
      s_cmd_trigs = "None"
    if len(h_procs) == 0:
      h_procs = "None"

    ret_val = f"Prefix Cmd Trigs: {CYAN}{p_cmd_trigs}{NORMAL}\r\n"
    ret_val += f"Suffix Cmd Trigs: {CYAN}{s_cmd_trigs}{NORMAL}\r\n"
    ret_val += f"Heartbeat Procs: {CYAN}{h_procs}{NORMAL}"

    return ret_val