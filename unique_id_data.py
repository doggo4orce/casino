import dataclasses
from mudlog import mudlog_type, mudlog
import string_handling

class unique_id_data:
  """A unique_identifier is essentially an address for rooms 
     and proto types for objects and npcs.
     zone_id = zone to which the address can be looked up
     id      = identifier within zone associated with zone_id"""
  def __init__(self, zone_id=None, id=None):
    self.zone_id=zone_id
    self.id=id

  @property
  def zone_id(self):
    return self._zone_id
  @property
  def id(self):
    return self._id

  @zone_id.setter
  def zone_id(self, new_zone_id):
    if new_zone_id == None:
      self._zone_id = None
    elif not string_handling.valid_id(new_zone_id):
      mudlog(mudlog_type.ERROR, f"trying to set invalid zone_id {new_zone_id}.")
      new_zone_id = None
    self._zone_id = new_zone_id

  @id.setter
  def id(self, new_id):
    if new_id == None:
      self._id = None
    elif not string_handling.valid_id(new_id):
      mudlog(mudlog_type.ERROR, f"trying to set invalid zone_id {new_id}.")
      new_id = None
    self._id = new_id

  # TODO: get rid of the tag[tag] format and just reference stuff with two separate strings
  @classmethod
  def from_string(cls, ref_string):
    zone_id, id = string_handling.parse_reference(ref_string)
    return unique_id_data(zone_id, id)

  # TODO:  if zone_id == None, should this just return self.id?
  # ALSO: should this be renamed to def vref(self) ?
  def __str__(self):
    return f"{self.zone_id}[{self.id}]"