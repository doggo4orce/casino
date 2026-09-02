from color import *

import db_column
import db_handler
import mudlog
import string_handling

class db_table:
  def __init__(self, handler, name):
    """Creates a database table object.
       name             = name of the table
       _handler         = shared (live) db_handler object which tells us what we need to know"""
    self._handler = handler
    self.name = name

  @property
  def has_primary_key(self):
    for column in self.columns:
      if column.is_primary:
        return True
    return False

  @property
  def has_composite_key(self):
    has_primary = False

    for column in self.list_columns():
      if column.is_primary and has_primary:
        return True
      elif column.is_primary:
        has_primary = True
    return False

  """create(*columns)                  <- create table with columns as arguments
     insert(**record)                  <- insert record into table
     delete(**clause)                  <- delete records from table satisfying clause
     rename(new_name)                  <- change only name of table
     primary_fields()                  <- returns (possibly singleton) list
     search(**clause)                  <- look up records from table, return as result set
     get_by_pk(**primary)              <- look up single result primary key
     num_records()                     <- count the number of records in table
     exists()                          <- ask handler if this table has been created
     drop()                            <- CAUTION: does what it says, drop the table
     list_columns()                    <- ask handler to list columns of this table
     add_column(column, type)          <- adds new column to table
     drop_column(column)               <- drops a column from the table
     rename_column(old_name, new_name) <- rename a column in the table
     has_column(name, type, primary)   <- check if column exists"""

  def create(self, *columns):
    self._handler.create_table(self.name, *columns)

  def insert(self, **record):
    self._handler.insert_record(self.name, **record)

  def delete(self, **clause):
    self._handler.delete_records(self.name, **clause)

  def rename(self, new_name):
    if not db_handler.valid_table_name(new_name):
      mudlog.error(f"Passing invalid new_name='{new_name}' to table.rename function.")
      return

    self._handler.rename_table(self.name, new_name)
    self.name = new_name

  def primary_fields(self):

    ret_val = list()

    for column in self.list_columns():
      if column.is_primary:
        ret_val.append(column.name)

    return ret_val

  def search(self, **clause):
    return self._handler.search_table(self.name, **clause)

  def get_by_pk(self, **primary):
    if set(primary.keys()) != set(self.primary_fields()):
      mudlog.error(f"searching table {self.name} with non-primary fields {', '.join(primary.keys())}\r\nactual primary fields are {', '.join(self.primary_fields())}")
      return None

    rs = self.search(**primary)

    if rs.num_results == 0:
      return None

    return rs[0]

  def num_records(self):
    return self._handler.num_records(self.name)

  def exists(self):
    return self._handler.table_exists(self.name)

  def drop(self):
    self._handler.drop_table(self.name)

  def list_columns(self):
    return self._handler.list_columns(self.name)

  def num_columns(self):
    return self._handler.num_columns(self.name)

  def add_column(self, name, type):
    if not db_handler.valid_column_name(name):
      mudlog.error(f"Attempting to add column to table {self.name} with invalid name '{name}'.")
      return

    self._handler.add_column(self.name, name, type)

  def drop_column(self, column):
    self._handler.drop_column(self.name, column)

  def rename_column(self, old_name, new_name):
    self._handler.rename_column(self.name, old_name, new_name)

  def has_column(self, column, type=None, primary=None):
    return self._handler.has_column(self.name, column, type, primary)

  def debug(self):
    ret_val = f"Name: {CYAN}{self.name}{NORMAL}\r\n"
    ret_val += "Columns:"
    columns = self.list_columns()
    if len(columns) == 0:
      ret_val += f"\r\n{CYAN}None{NORMAL}"
    else:
      for col in columns:
        ret_val += f"{CYAN}\r\n{str(col)}{NORMAL}"
    return ret_val