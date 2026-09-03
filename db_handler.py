import db_column
import db_result
import db_result_set
import db_table
import mudlog
import string_handling

import sqlite3

# allow characters and underscores only
def valid_table_name(table_name):
  return string_handling.alpha_num_under_score(table_name)

class db_handler:
  def __init__(self):
    self._connection = None
    self._cursor = None

  """connect(db_file)                       <- establish connection with database
     close()                                <- close connection to database
     execute(query, params)                 <- execute raw SQL query
     execute_many(query, params)            <- execute(many) raw SQL query
     commit()                               <- not necessary (due to auto-commit)
     create_table(name, *columns)           <- create new table with given columns
     drop_table(name)                       <- delete table
     copy_table(old, new)                   <- copy contents of old table to new table
     rename_table(table, name)              <- rename a table
     create_backup(file)                    <- dump all contents into new database file
     drop_all_tables()                      <- back anything up you might be attached to!
     add_column(table, name, type)          <- add new column to table
     drop_column(table, name)               <- delete column from table
     rename_column(table, old, new)         <- rename column in a table
     has_column(table, name, type, primary) <- check if table has column (type and primary optional)
     column_type(table, name)               <- check data type of column in field
     list_columns(table)                    <- show actual columns in a table
     list_column_names(table)               <- show column names in table
     num_columns(table)                     <- count columns in table
     num_tables()                           <- count tables in database
     num_records(table)                     <- count records in a table
     list_records(table)                    <- return table as result set
     insert_record(table, **record)         <- insert record to table
     delete_records(table, **record)        <- delete records from table
     list_tables()                          <- returns list of tables created
     list_table_names()                     <- returns list of names of tables created
     table_by_name(name)                    <- look up table in database by its name
     table_exists(name)                     <- check if a table has already been created
     fetch_one()                            <- fetch one result
     fetch_all()                            <- fetch all results
     show_table(name)                       <- display table as a string
     search_table(table, **clause)          <- search table for records, returns result set
     get_record(table, **key)               <- 
     verify_columns(table, *columns)        <- add columns to table if missing"""

  def close(self):
    self._connection.close()

  def connect(self, db_file=":memory:"):
    self._connection = sqlite3.connect(db_file)

    # results are dicts instead of tuples
    self._connection.row_factory = sqlite3.Row

    # must change row_factory before cursor creation
    self._cursor = self._connection.cursor()

  def execute(self, query, parameters = ()):
    return self._cursor.execute(query, parameters)

  def execute_many(self, query, parameter_list):
    return self._cursor.executemany(query, parameter_list)

  def commit(self):
    self._connection.commit()

  def create_table(self, table_name, *column_tuples):
    has_primary = False
    has_composite = False

    def sql_type(python_type):
      if python_type == int:
        return "int"
      if python_type == str:
        return "text"

    if self.table_exists(table_name):
      mudlog.error(f"tried to create table '{table_name}' which already exists")
      raise RuntimeError

    # sanity checks
    if not valid_table_name(table_name):
      mudlog.error(f"Trying to create table with invalid name '{table_name}'.")
      return

    if len(column_tuples) == 0:
      mudlog.error(f"Trying to create table '{table_name}' without any columns.")
      raise RuntimeError

    for tuple in column_tuples:
      if not db_column.valid_column_name(tuple[0]):
        mudlog.error(f"Trying to create table '{table_name}' with invalid column name '{tuple[0]}'.")
        return

    # determine if composite key
    for tuple in column_tuples:
      if has_primary and tuple[2]:
        has_composite = True
        break
      elif tuple[2]:
        has_primary = True

    # if table_name has already been used, abort
    if self.table_exists(table_name):
      mudlog.error(f"Trying to create table '{table_name}' which already exists.")
      return

    query = f"CREATE TABLE {table_name} ("

    if has_composite:
      primary_key_fields = []

      # column is a db_column object
      for tuple in column_tuples:
        query += f"\r\n  {tuple[0]} {sql_type(tuple[1])},"

        if tuple[2]:
          primary_key_fields.append(tuple[0])

      query += f"\r\n  PRIMARY KEY ({', '.join(primary_key_fields)})"
    
    else:
      for tuple in column_tuples:
        query += f"\r\n  {tuple[0]} {sql_type(tuple[1])}"

        if tuple[2]:
          query += " PRIMARY KEY"

        query += ","

      # there will be one too many columns
      query = query[:-1]

    query += "\r\n);"
    print(query)
    self.execute(query)
    
  def drop_table(self, table_name):
    sql = f"DROP TABLE {table_name};"
    self.execute(sql)

  # def copy_table(self, old, new):
  #   rs = self.search_table(old)

  #   for result in rs:
  #     return

  def rename_table(self, old, new):
    if not valid_table_name(new):
      mudlog.error(f"Passing invalid new='{new}' to handler.rename_table function.")
      return

    query = f"ALTER TABLE '" + old + "' RENAME TO '" + new + "';"
    self.execute(query)

  def add_column(self, table, name, type):
    column = db_column.db_column(name, type)
    sql = f"ALTER TABLE {table} ADD {column.name} {column.sqlite3_type};"
    self.execute(sql)

  def drop_column(self, table, name):
    sql = f"ALTER TABLE {table} DROP COLUMN {name};"
    self.execute(sql)

  def rename_column(self, table, old, new):
    if not db_column.valid_column_name(new):
      mudlog.error(f"Trying to rename column '{old}' in table '{self.name}' to invalid name '{new}'.")
      return

    sql = f"ALTER TABLE {table} RENAME COLUMN {old} TO {new};"
    self.execute(sql)

  def has_column(self, table, name, type=None, primary=None):
    for column in self.list_columns(table):
      if primary is not None and column.is_primary != primary:
        continue

      if type is not None and column.type != type:
        continue

      if column.name != name:
        continue

      # if we made it this far we found a match
      return True

    return False

  def column_type(self, table, name):
    if not name in self.list_column_names(table):
      return None

    for column in self.list_columns(table):
      if name == column.name:
        return column.type

  def list_columns(self, table_name):
    ret_val = list()

    # make sure table actually exists

    if not self.table_exists(table_name):
      mudlog.error(f"Trying to list columns of table {table_name}, which does not exist.")
      return None

    # TODO: write pragma function?
    sql = f"PRAGMA table_info({table_name});"

    self.execute(sql)
    self.commit()

    for result in self.fetch_all():
      new_column = db_column.db_column(result["name"], result["type"], result["pk"])
      ret_val.append(new_column)
      mudlog.debug(f"Found column {new_column} in table {table_name}.")

    return ret_val

  def list_column_names(self, table):
    return [column.name for column in self.list_columns(table)]

  def num_columns(self, table):
    return len(self.list_columns(table))

  def num_records(self, table):
    return self.search_table(table).num_results

  def num_tables(self):
    return len(self.list_tables())

  def insert_record(self, table, **record):
    table_columns = self.list_columns(table)
    column_names = [col.name for col in table_columns]
    num_fields = len(column_names)
    extra_fields = [field for field in record.keys() if field not in column_names]

    # do not accept a record with an extra field
    # TODO: instead of checking for extra fields, we could just catch an
    # exception:
    # eg.
    # sqlite3.OperationalError: table testtable has no column named father
    if len(extra_fields) > 0:
      mudlog.error(f"Trying to insert record\r\n{str(record)}\r\ninto table '{table}' with unexpected field '{extra_fields[0]}'.")
      return

    for column in table_columns:
      # if record has missing fields are missing pad them with null values
      if column.name not in record.keys():
        record[column.name] = None
        continue

      if type(record[column.name]) != column.type:
        mudlog.error(f"Trying to insert record into table {table}, but {record[column.name]} is not of type {column.type}.")
        return

    columns = ', '.join(record.keys())
    values = ', '.join('?' * num_fields)

    syntax = f"INSERT INTO {table} ({columns}) VALUES ({values});"

    self.execute(syntax, tuple(record.values()))
    self.commit()

  def insert_records(self, table, record_list):
    table_columns = self.list_columns(table)
    column_names = [col.name for col in table_columns]

    if len(record_list) == 0:
      return

    num_fields = len(column_names)

    for record in record_list:
      for column in table_columns:
        extra_fields = [field for field in record.keys() if field not in column_names]

        # do not accept a record with an extra field
        # TODO: instead of checking for extra fields, we could just catch an
        # exception:
        # eg.
        # sqlite3.OperationalError: table testtable has no column named father
        if len(extra_fields) > 0:
          mudlog.error(f"Trying to insert record\r\n{str(record)}\r\ninto table '{table}' with unexpected field '{extra_fields[0]}'.")
          return

        # if record has missing fields are missing pad them with null values
        if column.name not in record.keys():
          record[column.name] = None
          continue

        if type(record[column.name]) != column.type:
          mudlog.error(f"Trying to insert record into table {table}, but {record[column.name]} is not of type {column.type}.")
          return

    columns = ', '.join(column_names)
    values = ', '.join('?' * num_fields)
    
    syntax = f"INSERT INTO {table} ({columns}) VALUES ({values});"

    self.execute_many(syntax, [tuple(record.values()) for record in record_list])

  def delete_records(self, table, **record):
    sql = f"DELETE FROM {table}"
    filter_list = list()
    
    if len(record.keys()) != 0:

      for field in record:
        if type(record[field]) == int:
          filter_list.append(f"{field}={record[field]}")
        elif type(record[field]) == str:
          filter_list.append(f"{field}='{record[field]}'")

      filter_str = " AND ".join(filter_list)
    
      
      sql += f" WHERE {filter_str}"

    self.execute(sql)

  def list_tables(self):
    ret_val = list()

    for result in self.search_table("sqlite_master", type='table'):
      ret_val.append(db_table.db_table(self, result['name']))

    return ret_val

  def list_table_names(self):
    return [table.name for table in self.list_tables()]

  def table_by_name(self, table_name):
    if table_name not in self.list_table_names():
      return None

    return db_table.db_table(self, table_name)

  def table_exists(self, table_name):
    return self.table_by_name(table_name) is not None

  def fetch_one(self):
    fetch = self._cursor.fetchone()

    if fetch != None:
      return db_result.db_result.from_dict(dict(fetch))
    else:
      return None

  def fetch_all(self):
    ret_val = db_result_set.db_result_set()

    result = self.fetch_one()

    # returns empty result set
    if result is None:
      return ret_val

    # otherwise base result set upon fields of first result
    for field in result.fields:
      ret_val.add_column(field)

    # add the first result
    ret_val.add_result(result)

    # then add the rest
    while (True):
      result = self.fetch_one()
      if result == None:
        break
      else:
        ret_val.add_result(result)

    return ret_val

  def show_table(self, name):
    return str(self.search_table(name))

  def search_table(self, table, **clause):
    sql = f"SELECT * FROM {table}"
    filter_list = list()
    
    if len(clause.keys()) != 0:

      for field in clause:
        if type(clause[field]) == int:
          filter_list.append(f"{field}={clause[field]}")
        elif type(clause[field]) == str:
          filter_list.append(f"{field}='{clause[field]}'")

      filter_str = " AND ".join(filter_list)
    
      sql += f" WHERE {filter_str}"

    self.execute(sql)
    return self.fetch_all()

  def get_record(self, table, **primary):
    rs = self.search_table(table, **primary)
    if rs.num_results > 1:
      mudlog.error(f"Trying to access record with non-unique identifiers {str(primary)}.")
    elif rs.num_results == 0:
      return None
    else:
      return rs[0]

  def verify_columns(self, table, *columns):
    # if the table doesn't exist, simply create it
    if not self.table_exists(table):
      self.create_table(table, *columns)
      return

    # otherwise, add missing columns
    for column in columns:
      if not self.has_column(table, column[0], column[1]):
        self.add_column(table, column[0], column[1])


