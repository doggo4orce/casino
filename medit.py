from color import *

import buffer_data
import enum

class medit_state(enum.IntEnum):
  MEDIT_MAIN_MENU      = 1
  MEDIT_EDIT_NAME      = 2
  MEDIT_CONFIRM_SAVE   = 3

def medit_display_main_menu(d):
  medit_save = d.olc.save_data
  desc_buffer = buffer_data.buffer_data(medit_save.desc.text)

  out_str = f"-- NPC ID : [{CYAN}{medit_save.uid.id}{NORMAL}]"
  out_str += f"        Zone ID : [{CYAN}{medit_save.uid.zone_id}{NORMAL}]\r\n"
  out_str += f"{GREEN}1{NORMAL}) NPC Name    : {YELLOW}{medit_save.name}{NORMAL}\r\n"
  out_str += f"{GREEN}2{NORMAL}) Description :\r\n"
  out_str += f"{desc_buffer.clean_up().display(d.character.page_width, indent=True, color=True)}{NORMAL}\r\n"
  out_str += f"{GREEN}3{NORMAL}) L-Desc      : {YELLOW}{medit_save.ldesc}{NORMAL}\r\n"
  out_str += f"{GREEN}C{NORMAL}) Copy NPC\r\n"
  out_str += f"{GREEN}X{NORMAL}) Delete NPC\r\n"
  out_str += f"{GREEN}Q{NORMAL}) Quit\r\n"
  out_str += "Enter choice : "
  d.write(out_str)

def medit_parse(d, input, mud, db):
  match d.olc.state:
    case medit_state.MEDIT_MAIN_MENU:
      medit_parse_main_menu(d, input)
    case medit_state.MEDIT_EDIT_NAME:
      medit_parse_edit_name(d, input, mud, db)
    case medit_state.MEDIT_CONFIRM_SAVE:
      medit_parse_confirm_save(d, input, mud, db)

def medit_parse_main_menu(d, input):
  if input == "":
    d.write("Enter choice : ")
    return

  # no changes to save if they quit or drop
  if response.upper() not in {'Q', 'X'}:
    # we've done at least one thing aside from quit
    d.olc.changes = True

  response = input[0]

  match response.upper():
    case '1':
      d.olc.state = medit_state.MEDIT_EDIT_NAME
      d.write("Enter new name :")
    case 'Q':
      if d.olc.changes:
        d.olc.state = medit_state.MEDIT_CONFIRM_SAVE
        d.write("Save changes? : ")
    case _:
      d.write("Enter choice : ")

def medit_parse_edit_name(d, input, mud, db):
  medit_save = d.olc.save_data
  medit_save.name = input
  d.olc.state = medit_state.MEDIT_MAIN_MENU
  medit_display_main_menu(d)

def medit_parse_confirm_save(d, input, mud, db):
  pass
