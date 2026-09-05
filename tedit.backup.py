# Python Modules
import enum

# Local Modules
from color import *
import db_column
import db_handler
import descriptor_data

class tedit_state(enum.IntEnum):
  TEDIT_MAIN_MENU = 1
  TEDIT_EDIT_NAME = 2
  TEDIT_EDIT_SCHEMA = 3
  TEDIT_EDIT_COLUMN = 4
  TEDIT_EDIT_COLUMN_NAME = 5

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

# TODO: do these functions really need the server object?
def tedit_parse(d, input, db):
  match d.olc.state:
    case tedit_state.TEDIT_MAIN_MENU:
      tedit_parse_main_menu(d, input)
    case tedit_state.TEDIT_EDIT_NAME:
      tedit_parse_edit_name(d, input)
    case tedit_state.TEDIT_EDIT_SCHEMA:
      tedit_parse_edit_schema(d, input)
    case tedit_state.TEDIT_EDIT_COLUMN:
      tedit_parse_edit_column(d, input)
    case tedit_state.TEDIT_EDIT_COLUMN_NAME:
      tedit_parse_edit_column_name(d, input)

def tedit_parse_main_menu(d, input):
  if input == "":
    d.write("Enter choice : ")
    return

  response = input[0]

  if response not in {'q', 'Q'}:
    # we've done at least one thing aside from quit
    d.olc.changes = True

  match response.upper():
    case '1':
      d.write("Enter new table name : ")
      d.olc.state = tedit_state.TEDIT_EDIT_NAME
    case '2':
      tedit_display_schema_menu(d)
      d.olc.state = tedit_state.TEDIT_EDIT_SCHEMA
    case 'X':
      d.write("Not available yet.\r\nEnter choice : ")
    case 'Q':
      d.olc = None
      d.state = descriptor_data.descriptor_state.CHATTING

def tedit_parse_edit_name(d, input):
  if db_handler.valid_table_name(input):
    d.olc.save_data.name = input
    d.olc.state = tedit_state.TEDIT_MAIN_MENU
    tedit_display_main_menu(d)

def tedit_display_schema_menu(d):
  tedit_save = d.olc.save_data
  name_width = -1
  
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
  out_str += f"{GREEN}3{NORMAL}) Edit Column\r\n"
  out_str += f"{GREEN}4{NORMAL}) Main Menu\r\n"
  out_str += "Enter choice : "
  d.write(out_str)

def tedit_display_edit_column_menu(d):
  new_column = d.olc.save_data.new_column

  out_str = f"{GREEN}1{NORMAL}) Name    : {CYAN}"
  if new_column.name == None:
    out_str += f"(none)"
  else:
    out_str += f"{new_column.name}"
  out_str += f"{NORMAL}\r\n{GREEN}2{NORMAL}) Type    : {CYAN}{new_column.sqlite3_type}{NORMAL}\r\n"
  out_str += f"\r\n{GREEN}3{NORMAL}) Primary : {CYAN}{string_handling.yesno(new_column.is_primary)}{NORMAL}\r\n"
  d.write(out_str)

def tedit_parse_edit_schema(d, input):
  if input == "":
    d.write("Enter choice : ")
    return

  response = input[0]

  match response:
    case '1':
      d.olc.save_data.new_column = db_column(None, int, False)
      d.olc.state = tedit_state.TEDIT_EDIT_COLUMN
      tedit_display_new_column_menu(d)
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
  pass

def tedit_parse_column_name(d, input):
  if input == "":
    d.olc.state = tedit_state.TEDIT_MAIN_MENU
    tedit_display_main_menu(d)
    return

  if not string_handling.valid_column_name(input):
    d.write("Column names may only contain alpha-numeric characters and underscores.\r\n")
    tedit_display_main_menu(d)
    return

  tedit_save = d.olc.save_data
  tedit_save.column_name = input
  tedit_display_schema_type_menu(d)
  d.olc.state = tedit_state.TEDIT_EDIT_SCHEMA_TYPE


