import cmd_trig_data
from color import *
import copy
import hbeat_proc_data
import mudlog
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

  """assign_proc(proc)         <- assign spec proc
     assign_procs(spec_procs)  <- assign list of spec procs
     copy_from(behaviour)      <- copy all spec procs
     remove_spec_procs()       <- remove all spec procs
     remove_prefix_trigs()     <- remove all prefix_cmd_trigs
     remove_suffic_trigs()     <- remove all suffix_cmd_trigs
     remove_hbeat_procs()      <- remove all heartbeat procs
     remove_all_procs()        <- remove all procs"""

  def assign_proc(self, spec_proc):
    if not spec_proc.consistent:
      msg = f"Attempting to assign inconsistent spec_proc '{spec_proc.name}'."
      mudlog.error(msg)
      return
    if isinstance(spec_proc, cmd_trig_data.prefix_cmd_trig_data):
      self.prefix_cmd_trigs.append(spec_proc)
    elif isinstance(spec_proc, cmd_trig_data.suffix_cmd_trig_data):
      self.suffix_cmd_trigs.append(spec_proc)
    elif isinstance(spec_proc, hbeat_proc_data.hbeat_proc_data):
      self.hbeat_procs.append(spec_proc)
    else:
      msg = f"Attempting to assign unrecognized spec_proc type: '{spec_proc.name}'."
      mudlog.error(msg)

  def assign_procs(self, procs):
    for proc in procs:
      self.assign_spec_proc(proc)

  def copy_from(self, behaviour):
    self.prefix_cmd_trigs = copy.copy(behaviour.prefix_cmd_trigs)
    self.suffix_cmd_trigs = copy.copy(behaviour.suffix_cmd_trigs)
    self.hbeat_procs = copy.copy(behaviour.hbeat_procs)

  def remove_prefix_trigs(self):
    self.prefix_cmd_trigs = list()

  def remove_suffix_trigs(self):
    self.suffix_cmd_trigs = list()

  def remove_hbeat_procs(self):
    self.hbeat_procs = list()

  def remove_all_procs(self):
    self.remove_prefix_trigs()
    self.remove_suffix_trigs()
    self.remove_hbeat_procs()

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