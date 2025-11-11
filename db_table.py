from color import *

import db_column
import mudlog
import string_handling

class db_table:
  def __init__(self, handler, name):
    """Creates a database table object.
       name             = name of the table
       _handler         = shared (live) db_handler object which tells us what we need to know
       _pending_columns = used internally to detect composite key before creation"""
    self._handler = handler
    self.name = name
    self._pending_columns = None

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

  """create(*columns)                  <- create table with columns as arguments
     insert(**record)                  <- insert record into table
     delete(**clause)                  <- delete records from table satisfying clause
     primary_fields()                  <- returns (possibly singleton) list
     search(**clause)                  <- look up records from table, return as result set
     get_by_pk(**primary)              <- look up single result primary key
     num_records()                     <- count the number of records in table
     load()                            <- ask handler to load table from database
     exists()                          <- ask handler if this table has been created
     drop()                            <- CAUTION: does what it says, drop the table
     list_columns()                    <- ask handler to list columns of this table
     add_column(column, type)          <- adds new column to table
     drop_column(column)               <- drops a column from the table
     has_column(name, type, primary)   <- check if column exists"""

  def create(self, *columns):
    if self.exists():
      mudlog.error(f"tried to create table {self.name} which already exists")
      raise RuntimeError

    table_columns = list()

    if len(columns) == 0:
      mudlog.error(f"tried to create table {self.name} with no columns")
      raise RuntimeError

    # we keep track of pending columns because has_composite_key will need to check
    # them before creating the table.  this needs to be set to None immediately
    # afte the table is created 
    self._pending_columns = list()

    # column is a tuple passed as argument to create()
    for column in columns:
      self._pending_columns.append(db_column.db_column(*column))

    query = f"CREATE TABLE {self.name} ("

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

    self._pending_columns = None
    self._handler.execute(query)

  def insert(self, **record):
    self._handler.insert_record(self.name, **record)

  def delete(self, **clause):
    self._handler.delete_records(self.name, **clause)

  def primary_fields(self):
    if self._has_pending_columns():
      columns = self._pending_columns
    else:
      columns = self.list_columns()

    ret_val = list()

    for column in columns:
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

  def add_column(self, field, type):
    self._handler.add_column(column)

  def drop_column(self, column):
    self._handler.drop_column(self.name, column)

  def has_column(self, column, type=None, primary=None):
    return self._handler.has_column(self.name, column, type, primary)

  def _has_pending_columns(self):
    return self._pending_columns is not None

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