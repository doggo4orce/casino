import dataclasses
import entity_data
import logging
import spec_proc_data

class object_data(entity_data.entity_data):
  """Creates an object which characters can get, drop, and otherwise interact with.
     entity   = aggregates name, namelist, description, ldesc, and room"""

  """Note: It may seem that nothing distinguishes objects from entities but this is
     not the case.  It's just that those differences have not been implemented yet.
     For example, objects will eventually have stats that do not yet appear here."""
  def __init__(self, proto=None):
    super().__init__(proto)

    if proto == None:
      self.name = "an unfinished object"
      self.reset_aliases("unfinished", "object")
      self.ldesc = "An unfinished object has been left here."
      self.desc = "This object looks unfinished."

  def debug(self):
    ret_val = super().debug()
    return ret_val

  def __str__(self):
    return self.name
