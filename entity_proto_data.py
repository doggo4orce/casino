import dataclasses
import namelist_data

class entity_proto_data:
  """Used as blueprints to create entities."""
  def __init__(self):
    self.name ="an unfinished entity proto"
    self.namelist = namelist_data.namelist_data("unfinished", "entity", "proto")
    self.ldesc = "An unfinished entity proto is here."
    self.desc = "This entity proto looks unfinished."

  # Wrapped Properties
  @property
  def name(self):
    return self._name
  @property
  def namelist(self):
    return self._namelist
  @property
  def ldesc(self):
    return self._ldesc
  @property
  def desc(self):
    return self._desc

  # Wrapped Setters
  @name.setter
  def name(self, new_name):
    self._name = new_name
  @namelist.setter
  def namelist(self, new_namelist):
    self._namelist = new_namelist
  @ldesc.setter
  def ldesc(self, new_ldesc):
    self._ldesc = new_ldesc
  @desc.setter
  def desc(self, new_desc):
    self._desc = new_desc