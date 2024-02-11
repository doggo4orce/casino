import entity_data
import unique_id_data

# in the process of re-writing the class below, it's grown beyond being a dataclass, feb 9 2024, 9:40pm
# but do the same for entity_data first, and then make an entity_proto_data class,
# so that we can give obj_proto_Data and entity_proto_data instead of an entity
# so that obj_proto's don't occupy rooms
class obj_proto_data:
  def __init__(self):
    self.entity = entity_data.entity()
    self.prefix_command_triggers = list()
    self.suffix_command_triggers = list()
    self.heart_beat_procs = list()
    self.unique_id = unique_id_data.unique_id()

    self.entity

@dataclasses.dataclass
class obj_proto_data:
  entity: entity_data.entity_data = dataclasses.field(default_factory=lambda:entity_data.entity_data())
  prefix_command_triggers: list = dataclasses.field(default_factory=lambda:list())
  suffix_command_triggers: list = dataclasses.field(default_factory=lambda:list())
  heart_beat_procs: list = dataclasses.field(default_factory=lambda:list())
  unique_id: unique_id_data.unique_id_data = dataclasses.field(default_factory=lambda:unique_id_data.unique_id_data())

  def __post_init__(self):
    self.entity.ldesc ="An unfinished obj proto_type has been left here."

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