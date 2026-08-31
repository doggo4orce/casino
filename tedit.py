# Python Modules
import enum

# Local Modules
from color import *
import db_column
import db_handler
import descriptor_data
import string_handling

class tedit_state(enum.IntEnum):
  TEDIT_MAIN_MENU = 1
  TEDIT_EDIT_NAME = 2
  TEDIT_EDIT_SCHEMA = 3
  TEDIT_EDIT_COLUMN = 4
  TEDIT_EDIT_COLUMN_NAME = 5
  TEDIT_EDIT_COLUMN_TYPE = 6

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
      # here is where the saving will take place
      d.olc = None
      d.state = descriptor_data.descriptor_state.CHATTING

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

  response = input[0]

  match response:
    case '1':
      d.olc.save_data.column = db_column.db_column(None, int, False)
      d.olc.save_data.create_column = True
      d.olc.state = tedit_state.TEDIT_EDIT_COLUMN
      tedit_display_column_menu(d)
    case '2':
      d.olc.state = tedit_state.TEDIT_MAIN_MENU
      tedit_display_main_menu(d)
    case '3':
      d.olc.state = tedit_state.TEDIT_MAIN_MENU
      tedit_display_main_menu(d)
    case '4':
      d.olc.state = tedit_state.TEDIT_MAIN_MENU
      tedit_display_main_menu(d)

def tedit_parse_edit_column(d, input):
  if input == "":
    d.write("Enter choice : ")
    return

  response = input[0].upper()

  tedit_save = d.olc.save_data

  match response:
    case '1':
      d.olc.state = tedit_state.TEDIT_EDIT_COLUMN_NAME
      d.write("Enter column name : ")
    case '2':
      d.olc.state = tedit_state.TEDIT_EDIT_COLUMN_TYPE
      tedit_display_column_type_menu(d)
    case '3':
      col = tedit_save.column
      col.is_primary = not col.is_primary # toggle
      tedit_display_column_menu(d)
    case 'X':
      tedit_save.column = None
      tedit_save.create_column = False
      d.olc.state = tedit_state.TEDIT_EDIT_SCHEMA
      tedit_display_schema_menu(d)
    case 'Q':
      pass

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

  out_str = f"-- Table Schema : [{CYAN}{tedit_save.original_name}{NORMAL}]\r\n\r\n"
  for col in tedit_save.columns:
    out_str += f"{col.name:<{name_width}} {col.sqlite3_type:<5}"
    if col.is_primary:
      out_str += f"{RED}PRIMARY KEY{NORMAL}"
    out_str += "\r\n"

  out_str += f"\r\n{GREEN}1{NORMAL}) Add Column\r\n"
  out_str += f"{GREEN}2{NORMAL}) Drop Column\r\n"
  out_str += f"{GREEN}3{NORMAL}) Rename Column\r\n"
  out_str += f"{GREEN}4{NORMAL}) Main Menu\r\n"
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
  out_str += f"{GREEN}Q{NORMAL}) Save Changes\r\n"
  out_str += "Enter choice : "

  d.write(out_str)
