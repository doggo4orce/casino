# Python Modules
import enum

# Local Modules
from color import *
import db_column
import db_handler
import db_table
import descriptor_data
import string_handling

class tedit_state(enum.IntEnum):
  TEDIT_MAIN_MENU = 1
  TEDIT_EDIT_NAME = 2
  TEDIT_EDIT_SCHEMA = 3
  TEDIT_EDIT_COLUMN = 4
  TEDIT_EDIT_COLUMN_NAME = 5
  TEDIT_EDIT_COLUMN_TYPE = 6
  TEDIT_CONFIRM_SAVE_COLUMN = 7
  TEDIT_RENAME_COLUMN_SELECT = 8
  TEDIT_RENAME_COLUMN_GET_NAME = 9
  TEDIT_DROP_COLUMN = 10
  TEDIT_CONFIRM_SAVE = 11

def tedit_display_main_menu(d):
  tedit_save = d.olc.save_data

  out_str = f"-- Table Edit : [{CYAN}{tedit_save.original_name}{NORMAL}]\r\n"
  out_str += f"{GREEN}1{NORMAL}) Table Name  : {YELLOW}{tedit_save.name}{NORMAL}\r\n"
  out_str += f"{GREEN}2{NORMAL}) Edit Schema\r\n"
  out_str += f"{GREEN}3{NORMAL}) Inspect Records\r\n"
  out_str += f"{GREEN}X{NORMAL}) Drop Table\r\n"
  out_str += f"{GREEN}Q{NORMAL}) Quit\r\n"
  out_str += "Enter choice : "
  d.write(out_str)


# do these functions really need the server object?
def tedit_parse(d, input, db):
  match d.olc.state:
    case tedit_state.TEDIT_MAIN_MENU:
      tedit_parse_main_menu(d, input, db)
    case tedit_state.TEDIT_EDIT_NAME:
      tedit_parse_edit_name(d, input)
    case tedit_state.TEDIT_EDIT_SCHEMA:
      tedit_parse_edit_schema(d, input)
    case tedit_state.TEDIT_EDIT_COLUMN:
      tedit_parse_edit_column(d, input)
    case tedit_state.TEDIT_EDIT_COLUMN_NAME:
      tedit_parse_edit_column_name(d, input)
    case tedit_state.TEDIT_EDIT_COLUMN_TYPE:
      tedit_parse_edit_column_type(d, input)
    case tedit_state.TEDIT_CONFIRM_SAVE_COLUMN:
      tedit_parse_confirm_save_column(d, input)
    case tedit_state.TEDIT_RENAME_COLUMN_SELECT:
      tedit_parse_rename_column_select(d, input)
    case tedit_state.TEDIT_RENAME_COLUMN_GET_NAME:
      tedit_parse_rename_column_get_name(d, input)
    case tedit_state.TEDIT_DROP_COLUMN:
      tedit_parse_drop_column(d, input)
    case tedit_state.TEDIT_CONFIRM_SAVE:
      tedit_parse_confirm_save_table(d, input, db)

def tedit_parse_main_menu(d, input, db):
  if input == "":
    d.write("Enter choice : ")
    return

  response = input[0]

  if response not in {'q', 'Q'}:
    # we've done at least one thing aside from quit
    d.olc.changes = True

  match response.upper():
    case '1':
      d.olc.state = tedit_state.TEDIT_EDIT_NAME
      d.write("Enter new table name : ")
    case '2':
      d.olc.state = tedit_state.TEDIT_EDIT_SCHEMA
      tedit_display_schema_menu(d)
    case 'X':
      d.write("Not available yet.\r\nEnter choice : ")
    case 'Q':
      # check if there is nothing to save
      if not d.olc.changes:
        d.olc = None
        d.state = descriptor_data.descriptor_state.CHATTING
        return

      d.olc.state = tedit_state.TEDIT_CONFIRM_SAVE
      d.write("Save changes? : ")

def tedit_parse_edit_name(d, input):
  if db_handler.valid_table_name(input):
    d.olc.save_data.name = input
    d.olc.state = tedit_state.TEDIT_MAIN_MENU
    tedit_display_main_menu(d)

def tedit_parse_edit_schema(d, input):
  if input == "":
    d.olc.state = tedit_state.TEDIT_MAIN_MENU
    tedit_display_main_menu(d)
    return

  response = input[0].upper()

  match response:
    case '1':
      d.olc.save_data.column = db_column.db_column(None, int, False)
      d.olc.save_data.create_column = True
      d.olc.state = tedit_state.TEDIT_EDIT_COLUMN
      tedit_display_column_menu(d)
    case '2':
      column_list = d.olc.save_data.columns

      if len(column_list) == 0:
        d.write("There are no columns to drop!\r\n")
        d.write("Enter choice : ")
        return

      d.olc.state = tedit_state.TEDIT_DROP_COLUMN
      d.write("Select column to drop : ")
    case '3':
      column_list = d.olc.save_data.columns

      if len(column_list) == 0:
        d.write("There are no columns to rename!\r\n")
        d.write("Enter choice : ")
        return

      d.olc.state = tedit_state.TEDIT_RENAME_COLUMN_SELECT
      d.write("Select column to rename : ")
    case 'Q':
      d.olc.state = tedit_state.TEDIT_MAIN_MENU
      tedit_display_main_menu(d)

def tedit_parse_rename_column_select(d, input):
  if input == "":
    d.olc.state = tedit_state.TEDIT_EDIT_SCHEMA
    tedit_display_schema_menu(d)
    return

  column_list = d.olc.save_data.columns

  if input not in [ col.name for col in column_list ]:
    d.olc.state = tedit_state.TEDIT_EDIT_SCHEMA
    d.write("Column not found.\r\n")
    tedit_display_schema_menu(d)
    return

  d.olc.save_data.old_name = input
  d.olc.state = tedit_state.TEDIT_RENAME_COLUMN_GET_NAME
  d.write("Enter new name : ")

def tedit_parse_rename_column_get_name(d, input):
  if input == "":
    d.olc.state = tedit_state.TEDIT_EDIT_SCHEMA
    tedit_display_schema_menu(d)
    return

  if not db_column.valid_column_name(input):
    d.write("Column names may only contain letters and underscores.\r\n")
    d.olc.state = tedit_state.TEDIT_EDIT_SCHEMA
    tedit_display_schema_menu(d)
    return

  tedit_save = d.olc.save_data
  column_list = tedit_save.columns

  for col in column_list:
    if col.name == tedit_save.old_name:
      tedit_save.renamed_columns[col.name] = input
      col.name = input
      break

  d.olc.state = tedit_state.TEDIT_EDIT_SCHEMA
  tedit_display_schema_menu(d)

def tedit_parse_drop_column(d, input):
  if input == "":
    d.olc.state = tedit_state.TEDIT_EDIT_SCHEMA
    tedit_display_schema_menu(d)
    return

  column_list = d.olc.save_data.columns

  if input not in [ col.name for col in column_list ]:
    d.olc.state = tedit_state.TEDIT_EDIT_SCHEMA
    d.write("Column not found.\r\n")
    tedit_display_schema_menu(d)
    return

  for col in column_list:
    if col.name == input:
      column_list.remove(col)
      break

  d.olc.state = tedit_state.TEDIT_EDIT_SCHEMA
  tedit_display_schema_menu(d)
  
def tedit_parse_edit_column(d, input):
  if input == "":
    d.write("Enter choice : ")
    return

  response = input[0].upper()

  tedit_save = d.olc.save_data
  col = tedit_save.column

  match response:
    case '1':
      d.olc.state = tedit_state.TEDIT_EDIT_COLUMN_NAME
      d.write("Enter column name : ")
    case '2':
      d.olc.state = tedit_state.TEDIT_EDIT_COLUMN_TYPE
      tedit_display_column_type_menu(d)
    case '3':
      col.is_primary = not col.is_primary # toggle
      tedit_display_column_menu(d)
    case 'X':
      tedit_save.column = None
      tedit_save.create_column = False
      d.olc.state = tedit_state.TEDIT_EDIT_SCHEMA
      tedit_display_schema_menu(d)
    case 'Q':
      if col.name == None:
        d.olc.state = tedit_state.TEDIT_EDIT_SCHEMA
        tedit_display_schema_menu(d)
        return

      d.olc.state = tedit_state.TEDIT_CONFIRM_SAVE_COLUMN
      d.write("Save column, are you sure? : ")

def tedit_parse_confirm_save_table(d, input, db):
  if input == "":
    d.write("Enter yes or no (Y/N) : ")
    return

  response = input[0].upper()

  tedit_save = d.olc.save_data

  match response:
    case 'Y':  # we save changes
      tedit_save = d.olc.save_data

      # if table doesn't exist, then create it
      if not db.has_table(tedit_save.name):
        db.create_table(tedit_save.name, *[col.tuple() for col in tedit_save.columns])
      
      table = db.table_by_name(tedit_save.name)

      # if we renamed it, there's an old table to worry about
      if tedit_save.name != tedit_save.original_name and db.table_exists(tedit_save.original_name):
        old_table = db.table_by_name(tedit_save.original_name)
        table = db.table_by_name(tedit_save.name)

        # copy the data, trimming fields if we dropped some columns
        data = [record.dict() for record in old_table.search()]
        table.trim_insert_many(data)

        # delete old table
        old_table.drop()
        return

      # otherwise, only one table to worry about

      # did we add a new private key?
      new_private_key = False

      old_columns = table.list_columns()
      new_columns = tedit_save.columns

      # find out if we need to recreate the table
      for column in new_columns:
        if column.is_primary:
          # we might have added a new column that is a private key
          if column.name not in [col.name for col in old_columns]:
            new_private_key = True
          # or we might changed an existing column into a private key
          elif not next((col.is_primary for col in old_columns if col.name == column.name)):
            new_private_key = True

      # we cannot add a new private key to an existing table, so we must recreate the table
      if new_private_key:
        old_table = db.table_by_name(tedit_save.name)
        table = db.table_by_name(tedit_save.name + 'temp')
      
        data = [record.dict() for record in old_table.search()]
        table.trim_insert_many(data)

        old_table.drop()
        table.rename(tedit_save.name)
        return

      # otherwise, just drop any deleted columns or if we changed the type, drop it and re-add it
      for column in old_columns:
        if column.name not in [col.name for col in new_columns]:
          table.drop_column(column.name)

        elif column.type != next((col.type for col in new_columns if col.name == column.name)):
          table.drop_column(column.name)
          table.add_column(column.name, column.type)

      # and insert any newly created ones
      for column in old_columns:
        if column.name not in [col.name for col in old_columns]:
          table.add_column(column.name, column.type)

      d.olc = None
      d.state = descriptor_data.descriptor_state.CHATTING
      d.write("Table saved to database.\r\n")

    case 'N':
      d.olc = None
      d.state = descriptor_data.descriptor_state.CHATTING
      d.write("Changes discarded.\r\n")

    case _:
      d.write("Enter yes or no (Y/N) : ")
      return

  d.state = descriptor_data.descriptor_state.CHATTING
  return

def tedit_parse_confirm_save_column(d, input):
  if input == "":
    d.write("Enter yes or no (Y/N) : ")
    return

  response = input[0].upper()

  tedit_save = d.olc.save_data

  match response:
    case 'Y':
      # add the column to the table if it's new
      if tedit_save.create_column:
        tedit_save.columns.append(tedit_save.column)

      # TODO: otherwise update the version in the table
    case 'N':
      pass
    case _:
      d.write("Enter yes or no (Y/N) : ")
      return

  tedit_save.col = None
  d.olc.state = tedit_state.TEDIT_EDIT_SCHEMA
  tedit_display_schema_menu(d)

def tedit_parse_edit_column_name(d, input):
  if input == "":
    d.olc.state = tedit_state.TEDIT_EDIT_COLUMN
    tedit_display_column_menu(d)
    return

  if not db_column.valid_column_name(input):
    d.write("Column names may only contain letters and underscores.\r\n")
    d.olc.state = tedit_state.TEDIT_EDIT_COLUMN
    tedit_display_column_menu(d)
    return

  tedit_save = d.olc.save_data

  if input in [col.name for col in tedit_save.columns]:
    d.write("That column already exists!\r\n")
    d.olc.state = tedit_state.TEDIT_EDIT_COLUMN
    tedit_display_column_menu(d)
    return

  col = tedit_save.column
  col.name = input
  tedit_display_column_menu(d)
  d.olc.state = tedit_state.TEDIT_EDIT_COLUMN

def tedit_parse_edit_column_type(d, input):
  if input == "":
    d.olc.state = tedit_state.TEDIT_EDIT_COLUMN
    tedit_display_column_menu(d)
    return

  response = input[0]

  tedit_save = d.olc.save_data
  col = tedit_save.column

  match response:
    case '1':
      col.type = int
    case '2':
      col.type = str

  d.olc.state = tedit_state.TEDIT_EDIT_COLUMN
  tedit_display_column_menu(d)

def tedit_display_column_type_menu(d):
  out_str = f"{GREEN}1{NORMAL}) integer ({CYAN}int{NORMAL})\r\n"
  out_str += f"{GREEN}2{NORMAL}) string  ({CYAN}text{NORMAL})\r\n"
  out_str += "Enter choice : "
  d.write(out_str)

def tedit_display_schema_menu(d):
  tedit_save = d.olc.save_data
  name_width = 1
  
  for col in tedit_save.columns:
    name_width = max(name_width, len(col.name))

  out_str = f"-- Table Schema : [{CYAN}{tedit_save.original_name}{NORMAL}]\r\n"

  if len(tedit_save.columns) > 0:
    out_str += "\r\n"

  for col in tedit_save.columns:
    out_str += f"{col.name:<{name_width}} {col.sqlite3_type:<5}"
    if col.is_primary:
      out_str += f"{RED}PRIMARY KEY{NORMAL}"
    out_str += "\r\n"

  out_str += f"\r\n{GREEN}1{NORMAL}) Add Column\r\n"
  out_str += f"{GREEN}2{NORMAL}) Drop Column\r\n"
  out_str += f"{GREEN}3{NORMAL}) Rename Column\r\n"
  out_str += f"{GREEN}Q{NORMAL}) Main Menu\r\n"
  out_str += "Enter choice : "

  d.write(out_str)

def tedit_display_column_menu(d):
  col = d.olc.save_data.column

  out_str = "-- Column Fields\r\n"
  out_str += f"{GREEN}1{NORMAL}) Name    : {YELLOW}"

  if col.name == None:
    out_str += f"<NONE>"
  else:
    out_str += f"{col.name}"

  out_str += f"{NORMAL}\r\n"
  out_str += f"{GREEN}2{NORMAL}) Type    : {CYAN}{col.sqlite3_type}{NORMAL}\r\n"
  out_str += f"{GREEN}3{NORMAL}) Primary : {CYAN}{string_handling.yesno(col.is_primary)}{NORMAL}\r\n"
  out_str += f"{GREEN}X{NORMAL}) Abort\r\n"
  out_str += f"{GREEN}Q{NORMAL}) Save Column\r\n"
  out_str += "Enter choice : "

  d.write(out_str)
