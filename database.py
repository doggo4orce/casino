import db_column
import db_result
import mudlog
import string_handling

import sqlite3

# allow characters and underscores only
def valid_table_name(table_name):
  return string_handling.alpha_under_score(table_name)

class database:
  def __init__(self):
    self._connection = None
    self._cursor = None

  def connect(self, db_file=":memory:"):
    self._connection = sqlite3.connect(db_file)
    self._connection.row_factory = sqlite3.Row
    self._cursor = self._connection.cursor()

  def execute(self, query, parameters = ()):
    return self._cursor.execute(query, parameters)

  def commit(self):
    self._connection.commit()

  def create_table(self, table_name, *columns):
    # if table_name is invalid, abort
    if not valid_table_name(table_name):
      logging.error(f"Trying to create table with invalid name '{table_name}'.")
      return

    # require non-zero number of columns
    if len(columns) == 0:
      mudlog.error(f"Trying to create table '{table_name}' without any columns.")
      return

    # all column names must be valid
    for pair in columns:
      col = db_column.db_column(pair[0], pair[1])
      if not db_column.valid_column_name(col.name):
        mudlog.error(f"Trying to create table '{table_name}' with invalid column name '{col.name}'.")
        return

    # if table_name has already been used, abort
    if self.table_exists(table_name):
      mudlog.error(f"Trying to create table '{table_name}' which already exists.")
      return
		
    column_string = ""

    # turn ("column1", str), ("column2", int) into "column1 text, column2 int,"
    for pair in columns:
      col = db_column.db_column(pair[0], pair[1])
      column_string += f"{col.name} {col.sqlite3_type},"

    # this adds one too many commas at the very end
    column_string = column_string[:-1]

    sql = f"CREATE TABLE {table_name}({column_string})"
    self.execute(sql)

  def insert(self, table, **record):

    for field in record.keys():
      if type(record[field]) == str:
        record[field] = f"'{record[field]}'"
      elif type(record[field]) == int:
        record[field] = f"{record[field]}"

    columns = ', '.join(record.keys())
    values = ', '.join([record[field] for field in record.keys()])

    syntax = f"INSERT INTO {table} ({columns}) VALUES ({values})"

    self.execute(f"INSERT INTO {table} ({columns}) VALUES ({values})")
    self.commit()

  def list_tables(self):
    ret_val = list()

    sql = "SELECT * FROM sqlite_master WHERE type='table'"

    self.execute(sql)
    self.commit()

    for line in self.fetch_all():
      ret_val.append(line[1])

    return ret_val

  def table_exists(self, table_name):
    return table_name in self.list_tables()

  def fetch_one(self):
    # TODO: should return db_result()
    return self._cursor.fetchone()

  def fetch_all(self):
    # TODO: should return db_result_set()
    #  - then going to have to adjust list_tables() function
    return self._cursor.fetchall()