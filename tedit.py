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
  TEDIT_CONFIRM_DROP = 12

def tedit_display_main_menu(d):
  tedit_save = d.olc.save_data

  out_str = f"-- Table Edit : [{CYAN}{tedit_save.original_name}{NORMAL}]\r\n"
  out_str += f"{GREEN}1{NORMAL}) Name  : {YELLOW}{tedit_save.name}{NORMAL}\r\n"
  out_str += f"{GREEN}2{NORMAL}) Schema\r\n"
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
      tedit_parse_edit_name(d, input, db)
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
    case tedit_state.TEDIT_CONFIRM_DROP:
      tedit_parse_confirm_drop_table(d, input, db)

def tedit_parse_main_menu(d, input, db):
  if input == "":
    d.write("Enter choice : ")
    return

  response = input[0]

  # no changes to save if they quit or drop
  if response.upper() not in {'Q', 'X'}:
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
      d.olc.state = tedit_state.TEDIT_CONFIRM_DROP
      d.write("This action is final and cannot be reversed!\r\n\r\n")

      tedit_save = d.olc.save_data

      if tedit_save.original_name != tedit_save.name:
        d.write("Even though the table name has been changed,\r\n")
        d.write(f"the original table '{tedit_save.original_name}' will be dropped.\r\n\r\n")

      d.write("Are you sure you wish to drop this table? : ")

    case 'Q':
      # check if there is nothing to save
      if not d.olc.changes:
        d.olc = None
        d.state = descriptor_data.descriptor_state.CHATTING
        return

      d.olc.state = tedit_state.TEDIT_CONFIRM_SAVE
      d.write("Save changes? : ")

def tedit_parse_edit_name(d, input, db):
  tedit_save = d.olc.save_data
  if not db_handler.valid_table_name(input):
    d.write("Table names may contain alpha-numeric characters and underscores only.\r\n")
  else:
    tedit_save.name = input
    if not db.table_exists(tedit_save.original_name):
      tedit_save.original_name = input

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
      d.olc.save_data.create_column = False
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

  # if we're editing, make sure it's a change
  if not tedit_save.create_column and input == tedit_save.old_name:
    d.write("That's the same name!\r\n")
    d.olc.state = tedit_state.TEDIT_EDIT_SCHEMA
    tedit_display_schema_menu(d)
    return

  # make sure we don't already have that column
  if input in [col.name for col in column_list]:
    d.write("That column is already in use!\r\n")
    d.olc.state = tedit_state.TEDIT_EDIT_SCHEMA
    tedit_display_schema_menu(d)
    return

  # update the column name
  for col in column_list:
    if col.name == tedit_save.old_name:
      col.name = input
      break

  tedit_save.data.rename_column(tedit_save.old_name, input)

  d.olc.state = tedit_state.TEDIT_EDIT_SCHEMA
  tedit_display_schema_menu(d)

def tedit_parse_drop_column(d, input):
  if input == "":
    d.olc.state = tedit_state.TEDIT_EDIT_SCHEMA
    tedit_display_schema_menu(d)
    return

  tedit_save = d.olc.save_data
  column_list = tedit_save.columns
  data = tedit_save.data

  if input not in [ col.name for col in column_list ]:
    d.olc.state = tedit_state.TEDIT_EDIT_SCHEMA
    d.write("Column not found.\r\n")
    tedit_display_schema_menu(d)
    return

  # drop the column in the schema
  for col in column_list:
    if col.name == input:
      column_list.remove(col)
      break

  # drop the column in our local result set
  data.delete_column(input)

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

def tedit_parse_confirm_drop_table(d, input, db):
  if input == "":
    d.write("Enter yes or no (Y/N) : ")
    return

  response = input[0].upper()

  tedit_save = d.olc.save_data

  match response:
    case 'Y':
      table = db.table_by_name(tedit_save.original_name)
      table.drop()

      d.olc = None
      d.state = descriptor_data.descriptor_state.CHATTING
      d.write("Table deleted from database.\r\n")
    case _:
      d.olc.state = tedit_state.MAIN_MENU
      tedit_display_main_menu(d)

def tedit_parse_confirm_save_table(d, input, db):
  if input == "":
    d.write("Enter yes or no (Y/N) : ")
    return

  response = input[0].upper()

  tedit_save = d.olc.save_data

  match response:
    case 'Y':  # we save changes

      new_name = tedit_save.name
      old_name = tedit_save.original_name

      # if table doesn't exist, then create it
      if not db.has_table(tedit_save.name):
        db.create_table(new_name, *[col.tuple() for col in tedit_save.columns])

      new_table = db.table_by_name(new_name)
      old_table = db.table_by_name(old_name)

      # if we renamed it, there's an old table to worry about
      if new_name != old_name and db.table_exists(old_name):
        old_table.drop()

      # if we made any changes, recreate table with updated schema
      if d.olc.changes:
        new_table.drop()
        db.create_table(new_name, *[col.tuple() for col in tedit_save.columns])

        # unless the table is brand new, we've got data to copy
        if not tedit_save.create_table:
          new_table.trim_insert_many([result.dict() for result in tedit_save.data])

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

  column = tedit_save.column
  column_list = tedit_save.columns
  data = tedit_save.data

  match response:
    case 'Y':
      # add the column to the table if it's new
      if tedit_save.create_column:
        column_list.append(column)
        if not tedit_save.create_table:
          data.add_column(column.name)
      else:
        for col in column_list:
          if col.name == tedit_save.original_col_name:

            changed_name = col.name != column.name
            changed_type = col.type != column.type

            if changed_name and changed_type:
              data.delete_column(col.name)
              data.add_column(column.name, column.type)

            elif changed_name:
              data.rename_column(col.name, column.name)

            elif changed_type:
              data.clear_column(col.name)

          col.name = column.name
          col.type = column.type
          col.is_primary = column.is_primary

    case 'N':
      pass
    case _:
      d.write("Enter yes or no (Y/N) : ")
      return

  tedit_save.column = None

  # reset storage for next edit
  tedit_save.create_column = False
  tedit_save.original_column_name = None
  
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
  column = tedit_save.column

  match response:
    case '1':
      column.type = int
    case '2':
      column.type = str

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
  column = d.olc.save_data.column

  out_str = "-- Column Fields\r\n"
  out_str += f"{GREEN}1{NORMAL}) Name    : {YELLOW}"

  if column.name == None:
    out_str += f"<NONE>"
  else:
    out_str += f"{column.name}"

  out_str += f"{NORMAL}\r\n"
  out_str += f"{GREEN}2{NORMAL}) Type    : {CYAN}{column.sqlite3_type}{NORMAL}\r\n"
  out_str += f"{GREEN}3{NORMAL}) Primary : {CYAN}{string_handling.yesno(column.is_primary)}{NORMAL}\r\n"
  out_str += f"{GREEN}X{NORMAL}) Abort\r\n"
  out_str += f"{GREEN}Q{NORMAL}) Save Column\r\n"
  out_str += "Enter choice : "

  d.write(out_str)
