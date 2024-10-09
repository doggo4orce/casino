import string_handling

# allow characters and underscores only
def valid_column_name(column_name):
  return string_handling.alpha_under_score(column_name)

class db_column:
  """name = name of the column as string
     type = datatype for column, e.g. str, int, or bool
     sqlite3_type = returns "text" or "int", etc. """

  def __init__(self, name, type):
    self._name = name
    self._type = None

    if type in [int, str]:
      self._type = type

  @property
  def name(self):
    return self._name

  @property
  def type(self):
    return self._type
  
  @property
  def sqlite3_type(self):
    if self.type == int:
      return "int"
    elif self.type == str:
      return "text"
    else:
      return None # throw exception?

  def __str__(self):
    return f"('{self.name}', {self.sqlite3_type})"