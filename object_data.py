import dataclasses

import actor_data
import entity_data
import spec_proc_data
import unique_id_data

class object_data(actor_data.actor_data, entity_data.entity_data):
  """Creates an object which characters can get, drop, and otherwise interact with.
     entity   = aggregates name, namelist, description, ldesc, and room"""

  """Note: It may seem that nothing distinguishes objects from entities but this is
     not the case.  It's just that those differences have not been implemented yet.
     For example, objects will eventually have stats that do not yet appear here."""
  def __init__(self, proto=None):
    actor_data.actor_data.__init__(self)
    entity_data.entity_data.__init__(self, proto)

    if proto == None:
      self.name = "an unfinished object"
      self.reset_aliases("unfinished", "object")
      self.ldesc = "An unfinished object has been left here."
      self.desc = "This object looks unfinished."

  def copy_from(self, obj):
    entity_data.entity_data.copy_from(self, obj)
    # copy object specific fields here

  def debug(self):
    ret_val = super().debug()
    return ret_val

  def __str__(self):
    return self.name
