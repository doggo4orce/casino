import dataclasses
import string_handling
import sqlite3

class column:
  """name = name of the column, e.g. 'first_name' or 'age'
     type = datatype for column, e.g. str or int, also accepts "str", "text", or "int"
  Properties:
     sqlite3_type = returns "text" or "int", etc. """

  def __init__(self, name, typ):
    self.name = name
    # we flexibly allow caller to pass strings into typ if they intelligently describe a data-type
    if type(typ) == str:
      if typ.lower() in ["str", "text"]:
        self.type = str
      elif typ.lower() == "int":
        self.type = int
    elif typ in [int, str]:
      self.type = typ
    else:
      self.type = str # throw exception?

  @property
  def sqlite3_type(self):
    if self.type == int:
      return "int"
    elif self.type == str:
      return "text"
    else:
      return None # throw exception?

  def __str__(self):
    return f"('{self.name}', '{self.sqlite3_type}')"

class result:
  """value = stores the record in dictionary: e.g. values["name"] = "bob", values["age"] = 25"""
  def __init__(self, **fields):
    # no caution needed until its plugged into a result_set
    self._values = dict(fields)

    for key in fields:
      self._values[key] = fields[key]

    def __getitem__(self, key):
      return self._values[key]

    def __setitem__(self, key, value):
      self._values[key] = value

class result_set:
  def __init__(self, *column_names):
    self._column_names = column_names

class orm:
  """connection = connection used to connect to a database and commit changes
     cursor = cursor used to read/write to a database"""
  def __init__(self, db_file):
    self._connection = sqlite3.connect(db_file)
    self._cursor = self._connection.cursor()

  """execute(query, params)                 <-- pass arguments directly to _cursor.execute
     commit()                               <-- calls _connection.commit
     fetchone()                             <-- returns _cursor.fetchone()
     fetchall()                             <-- returns _cursor.fetchall()
     valid_table_name()                     <-- decides which table names are acceptable
     valid_column_name()                    <-- decides which column names are acceptable
     list_tables()                          <-- returns list of tables which have been created
     list_columns(name)                     <-- lists columns of table with given name
     column_type(col_name, tab_name)        <-- returns data type of column from table
     column_in_table(col_name, tab_name)    <-- decides if given table has given column
     table_exists(tab_name)                 <-- check if table with given name has been created
     create_table(tab_name, *columns)       <-- create_table("employee", ("name", str), ("salary", int))
     valid_field(tab_name, col_name, field) <-- check if field is appropropriate data type for column
     insert(tab_name, **kwargs)             <-- insert("employee", name="bob", salary="50000")"""

  def execute(self, query, params = ()):
    self._cursor.execute(query, params)

  def commit(self):
    self._connection.commit()

  def fetchone(self):
    return self._cursor.fetchone()

  def fetchall(self):
    return self._cursor.fetchall()

  def valid_table_name(self, name):
    for char in name:
      # only accept letters and underscores
      if not char.isalpha() and char != '_':
        return False
    return True

  def valid_column_name(self, name):
    # for now use the same rule
    return self.valid_table_name(name)

  def list_tables(self):
    ret_val = list()

    sql = "SELECT * FROM sqlite_master WHERE type='table'"

    self.execute(sql)
    self.commit()

    for line in self.fetchall():
      ret_val.append(line[1])

    return ret_val

  def list_columns(self, table_name):
    ret_val = list()

    # make sure table actually exists

    if not self.table_exists(table_name):
      print(f"Trying to list columns of table {table_name}, which does not exist.")
      return None

    sql = f"PRAGMA table_info({table_name})"

    self.execute(sql)
    self.commit()

    for line in self.fetchall():
      ret_val.append(column(line[1], line[2]))

    return ret_val

  def column_type(self, column_name, table_name):
    if not self.column_in_table(column_name, table_name):
      return None

    for column in self.list_columns(table_name):
      if column_name == column.name:
        return column.type

  def column_in_table(self, column_name, table_name):
    for column in self.list_columns(table_name):
      if column_name == column.name:
        return True
    return False

  def table_exists(self, table_name):
    return table_name in self.list_tables()

  def create_table(self, table_name, *columns):
    # if table_name is invalid, abort
    if not self.valid_table_name(table_name):
      print(f"Trying to create table with invalid name '{table_name}'.")
      return

    # require non-zero number of columns
    if len(columns) == 0:
      print(f"Trying to create table '{table_name}' without any columns.")
      return

    # all column names must be valid
    for pair in columns:
      col = column(pair[0], pair[1])
      if not self.valid_column_name(col.name):
        print(f"Trying to create table '{table_name}' with invalid column name '{col.name}'.")
        return

    # if table_name has already been used, abort
    if self.table_exists(table_name):
      print(f"Trying to create table '{table_name}' which already exists.")
      return
		
    column_string = ""

    # turn ("column1", str), ("column2", int) into "column1 text, column2 int,"
    for pair in columns:
      col = column(pair[0], pair[1])
      column_string += f"{col.name} {col.sqlite3_type},"

    # this adds one too many commas at the very end
    column_string = column_string[:-1]

    sql = f"CREATE TABLE {table_name}({column_string})"
    self.execute(sql)
    self.commit()

  def valid_field(self, table_name, column_name, field):
    if not self.table_exists(table_name):
      return False
    if not self.column_in_table(column_name, table_name):
      return False
    return self.column_type(column_name, table_name) == type(field)

  def insert(self, table_name, **values):
    column_string = ""
    value_string = ""

    if not self.table_exists(table_name):
      print(f"Trying to insert row to table {table_name}, which does not exist.")
      return

    for key in values:
      if not self.column_in_table(key, table_name):
        print(f"Trying to insert row to table {table_name} with invalid column {key}.")
        return

      if not self.valid_field(table_name, key, values[key]):
        print(f"Trying to insert row to table {table_name} with invalid field {values[key]} for column {key}.")
        return

      column_string += f"{key},"

      # enclose in quotations if the field is a string
      if type(values[key]) == str:
        value_string += f"'{values[key]}',"
      elif type(values[key]) == int:
        value_string += f"{values[key]},"

    # peel final commas
    column_string = column_string[:-1]
    value_string = value_string[:-1]

    sql = f"INSERT INTO {table_name} ({column_string}) VALUES({value_string})"

    self.execute(sql)
    self.commit()

  # select("employee", ("first_name", "last_name"), 
  def select(self, *args):
    pass
    
# db = orm(":memory:")

# #db.create_table2("employees", ("first_name", str), ("last_name", str), ("age", int))
# # db.insert("employees", first_name="bob", last_name="ross", age=39)
# # db.insert("employees", first_name="dylan", last_name="wannabang", age=12)
# db.create_table("employee", ("first_name", str), ("age", int))
# db.insert("employee", first_name="kyle", age=39)
# db.execute("""SELECT * FROM employee""")
# print(db.fetchall())
