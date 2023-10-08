import dataclasses
import logging
import string_handling

def valid_zone_id(zone_id):
  return string_handling.only_alpha_and_under_score(zone_id)

def valid_local_id(local_id):
  return string_handling.only_alpha_and_under_score(local_id)

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
    if not valid_zone_id(new_zone_id):
      logging.warning(f"Trying to set invalid zone_id {new_zone_id}.")
      new_zone_id = None
    self._zone_id = new_zone_id

  @id.setter
  def id(self, new_id):
    if not valid_zone_id(new_id):
      logging.warning(f"Trying to set invalid zone_id {new_id}.")
      new_id = None
    self._id = new_id

  @classmethod
  def from_string(cls, ref_string):
    zone_id, id = string_handling.parse_reference(ref_string)
    return unique_id_data(zone_id, id)
    
  def __str__(self):
    return f"{self.zone_id}[{self.id}]"