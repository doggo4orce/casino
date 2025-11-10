from color import *

import db_column
import string_handling

class db_table:
  def __init__(self, handler, name):
    self._handler = handler
    self.name = name
    self._pending_columns = list()

  @property
  def has_primary_key(self):
    for column in self.columns:
      if column.is_primary:
        return True
    return False

  @property
  def has_composite_key(self):
    has_primary = False
    if self._has_pending_columns():
      columns = self._pending_columns
    else:
      columns = self.list_columns()

    for column in columns:
      if column.is_primary and has_primary:
        return True
      elif column.is_primary:
        has_primary = True
    return False

  def _has_pending_columns(self):
    return self._pending_columns is not None

  def list_columns(self):
    return self._handler.list_columns(self.name)

  def create(self, *columns):
    query = f"CREATE TABLE {self.name} ("
    table_columns = list()

    if len(columns) == 0:
      return None

    # column is a tuple passed as argument to create()
    for column in columns:
      self._pending_columns.append(db_column.db_column(*column))

    if self.has_composite_key:
      primary_key_fields = []

      # column is a db_column object
      for column in self._pending_columns:
        query += f"\r\n  {column.name} {column.sqlite3_type},"

        if column.is_primary:
          primary_key_fields.append(column.name)

      query += f"\r\n  PRIMARY KEY ({', '.join(primary_key_fields)})"
    
    else:
      for column in self._pending_columns:
        query += f"\r\n  {column.name} {column.sqlite3_type}"

        if column.is_primary:
          query += " PRIMARY KEY"

        query += ","

      query = query[:-1]

    query += "\r\n);"

    print(query)
    self._handler.execute(query)

  def add_column(self, column):
    self._handler.add_column(column)

  def debug(self):
    ret_val = f"Name: {CYAN}{self.name}{NORMAL}\r\n"
    ret_val += "Columns:"
    if len(self.columns) == 0:
      ret_val += f"\r\n{CYAN}None{NORMAL}"
    else:
      for col in self.columns:
        ret_val += f"{CYAN}\r\n{str(col)}{NORMAL}"
    return ret_val