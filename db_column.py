import string_handling

# allow characters and underscores only
def valid_column_name(column_name):
  return string_handling.alpha_under_score(column_name)

class db_column:
  """name = name of the column as string
     type = datatype for column, e.g. str, int, or bool
     sqlite3_type = returns "text" or "int", etc. """

  def __init__(self, name, type, primary=False):
    self.name = name
    self.type = None
    self.is_primary = bool(primary)

    if type in [int, str]:
      self.type = type
    elif type.lower() == 'int':
      self.type = int
    elif type.lower() == 'text':
      self.type = str

  
  @property
  def sqlite3_type(self):
    if self.type == int:
      return "int"
    elif self.type == str:
      return "text"
    else:
      return None # throw exception?

  # TODO : this was quick and dirty, make it so columns can accept
  # subscripts like col[0], col[1], col[2] so this function isn't needed
  def tuple(self):
    return (self.name, self.type, self.is_primary)
    
  def __str__(self):
    ret_val = f"('{self.name}', {self.sqlite3_type}"
    if self.is_primary:
      ret_val += f", PRIMARY KEY"
    ret_val += ")"
    return ret_val