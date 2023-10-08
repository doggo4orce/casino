@dataclasses.dataclass # perhaps this should be moved to pc.py
class npc_proto_data:
  entity: entity.entity_data = dataclasses.field(default_factory=lambda:entity.entity_data())
  ldesc: str="An unfinished npc proto_type stands here."
  prefix_command_triggers: list = dataclasses.field(default_factory=lambda:list())
  suffix_command_triggers: list = dataclasses.field(default_factory=lambda:list())
  heart_beat_procs: list = dataclasses.field(default_factory=lambda:list())
  unique_id: unique_id.unique_id_data = dataclasses.field(default_factory=lambda:unique_id.unique_id_data())

  def __post_init__(self):
    self.entity.ldesc = "An unfinished npc proto_type stands here."

  # TODO: make this function accept list of spec_procs
  def assign_spec_proc(self, spec_proc):
    # will return an empty list() if the function args are correct
    problems = spec_proc.first_fn_arg_error_full()
    for problem in problems:
      logging.error(problem)
    if len(problems) > 0:
      return
    if type(spec_proc) == spec_procs.prefix_command_trigger:
      self.prefix_command_triggers.append(spec_proc)
    elif type(spec_proc) == spec_procs.suffix_command_trigger:
      self.suffix_command_triggers.append(spec_proc)
    elif type(spec_proc) == spec_procs.heart_beat_proc:
      self.heart_beat_procs.append(spec_proc)

  @property
  def id(self):
    return self.unique_id.id
  @property
  def zone_id(self):
    return self.unique_id.zone_id

  def __str__(self):
    ret_val = f"NPC: {CYAN}{self.entity.name}{NORMAL} "
    ret_val += f"Alias: {CYAN}"
    for name in self.entity.namelist:
      ret_val += name + " "
    ret_val += f"{NORMAL}\r\n"
    ret_val += self.entity.desc.display(width=65, indent=True)
    ret_val += f"Desc:\r\n{self.entity.desc.str()}\r\n"
    ret_val += f"L-Desc: {self.ldesc}\r\n"
    return ret_val