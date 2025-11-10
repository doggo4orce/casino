from color import *

import db_column
import string_handling

class db_table:
  def __init__(self, name, *columns):
    self.name = name
    self.columns = list()

    for column in columns:
      self.columns.append(db_column.db_column(*column))

  @property
  def has_primary_key(self):
    for column in self.columns:
      if column.is_primary:
        return True
    return False

  @property
  def has_composite_key(self):
    has_primary = False

    for column in self.columns:
      if column.is_primary and has_primary:
        return True
      elif column.is_primary:
        has_primary = True

    return False

  def creation_syntax(self):
    ret_val = f"CREATE TABLE {self.name} ("

    if self.has_composite_key:
      primary_key_fields = []

      for column in self.columns:
        ret_val += f"\r\n  {column.name} {column.sqlite3_type},"

        if column.is_primary:
          primary_key_fields.append(column.name)

      ret_val += f"\r\n  PRIMARY KEY ({', '.join(primary_key_fields)})"
    
    else:
      for column in self.columns:
        ret_val += f"\r\n  {column.name} {column.sqlite3_type}"

        if column.is_primary:
          ret_val += " PRIMARY KEY"

        ret_val += ","

    ret_val += "\r\n);"

    return ret_val

  def debug(self):
    ret_val = f"Name: {CYAN}{self.name}{NORMAL}\r\n"
    ret_val += "Columns:"
    if len(self.columns) == 0:
      ret_val += f"\r\n{CYAN}None{NORMAL}"
    else:
      for col in self.columns:
        ret_val += f"{CYAN}\r\n{str(col)}{NORMAL}"
    return ret_val