import string_handling

# allow characters and underscores only
def valid_field_name(field_name):
  return string_handling.alpha_under_score(field_name)

class db_result:
  """values     = fields and entries key-value pairs"""
  def __init__(self, **field_values):
    self._values = dict()

    for field in field_values:
      self.add_field(field, field_values[field])

  """Properties:

     fields     = return list of fields for which result has entries
     num_fields = number of fields result has non-blank entries for
     is_blank   = check if num_fields is 0"""

  @property
  def fields(self):
    return list(self._values.keys()).copy()

  @property
  def num_fields(self):
    return len(self.fields)

  @property
  def is_blank(self):
    return self.num_fields == 0

  @classmethod
  def from_dict(self, dict):
    ret_val = db_result()
    for field in dict.keys():
      ret_val[field] = dict[field]
    return ret_val

  """has_field(field)           <-- check if the result has an entry for given field
     add_field(field, value)    <-- adds field to result as key-value pair
     update_field(field, value) <-- update existing field
     delete_field(field)        <-- removes the field from the result"""

  def has_field(self, field):
    return field in self.fields

  def add_field(self, field, value):
    if not valid_field_name(field):
      logging.error(f"Trying to add invalid field {field}.")
    else:
      self._values[field] = value

  def update_field(self, field, value):
    if field not in self.fields:
      logging.error(f"Trying to update field {field} that isn't defined.")
      return
    else:
      self._values[field] = value

  def delete_field(self, field):
    del self._values[field]

  def __iter__(self):
    return result_iterator(self)

  def __contains__(self, key):
    return key in self.fields

  def __getitem__(self, key):
    return self._values[key]

  def __setitem__(self, key, value):
    if key not in self.fields:
      self.add_field(key, value)
    else:
      self.update_field(key, value)

  def __str__(self):
    return str(self._values)

class result_iterator:
  def __init__(self, result):
    self._result = result
    self._idx = 0

  def __next__(self):
    if self._idx < self._result.num_fields:
      ret_val = self._result.fields[self._idx]
      self._idx += 1
      return ret_val
    else:
      raise StopIteration