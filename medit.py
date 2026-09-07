# Python Modules
import copy

# Local Modules
from color import *
import buffer_data
import descriptor_data
import enum
import npc_data
import npc_proto_data

class medit_state(enum.IntEnum):
  MEDIT_MAIN_MENU      = 1
  MEDIT_EDIT_NAME      = 2
  MEDIT_CONFIRM_SAVE   = 3
  MEDIT_EDIT_DESC      = 4
  MEDIT_EDIT_LDESC     = 5
  MEDIT_EDIT_ALIAS     = 6

def medit_display_main_menu(d):
  medit_save = d.olc.save_data
  desc_buffer = buffer_data.buffer_data(medit_save.desc.text)

  out_str = f"-- NPC ID : [{CYAN}{medit_save.uid.id}{NORMAL}]"
  out_str += f"        Zone ID : [{CYAN}{medit_save.uid.zone_id}{NORMAL}]\r\n"
  out_str += f"{GREEN}1{NORMAL}) NPC Name: {YELLOW}{medit_save.name}{NORMAL}\r\n"
  out_str += f"{GREEN}2{NORMAL}) Description:-\r\n"
  out_str += f"{desc_buffer.clean_up().display(d.character.page_width, indent=True, color=True)}{NORMAL}\r\n"
  out_str += f"{GREEN}3{NORMAL}) L-Desc:-\r\n{YELLOW}{medit_save.ldesc}{NORMAL}\r\n"
  out_str += f"{GREEN}4{NORMAL}) Aliases: {YELLOW}{', '.join(medit_save.aliases)}{NORMAL}\r\n"
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
      medit_parse_edit_name(d, input)
    case medit_state.MEDIT_CONFIRM_SAVE:
      medit_parse_confirm_save(d, input, mud, db)
    case medit_state.MEDIT_EDIT_LDESC:
      medit_parse_edit_ldesc(d, input)
    case medit_state.MEDIT_EDIT_ALIAS:
      medit_parse_edit_alias(d, input)

def medit_parse_edit_alias(d, input):
  if input == "":
    d.write("That won't do.  You must have at least one alias.\r\nEnter aliases, separated by spaces : ")
    return

  medit_save = d.olc.save_data
  medit_save.aliases = input.split(' ')
  d.olc.state = medit_state.MEDIT_MAIN_MENU
  medit_display_main_menu(d)

def medit_parse_main_menu(d, input):
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
      d.olc.state = medit_state.MEDIT_EDIT_NAME
      d.write("Enter new name : ")
    case '2':
      medit_save = d.olc.save_data
      d.olc.state = medit_state.MEDIT_EDIT_DESC
      d.start_writing(medit_save.desc.text, medit_save.desc)
    case '3':
      medit_save = d.olc.save_data
      d.olc.state = medit_state.MEDIT_EDIT_LDESC
      d.write("Enter new L-Desc : ")
    case '4':
      medit_save = d.olc.save_data
      d.olc.state = medit_state.MEDIT_EDIT_ALIAS
      d.write("Enter aliases, separated by spaces : ")
    case 'Q':
      if d.olc.changes:
        d.olc.state = medit_state.MEDIT_CONFIRM_SAVE
        d.write("Save changes? : ")
      else:
        d.olc = None
        d.state = descriptor_data.descriptor_state.CHATTING
    case _:
      d.write("Enter choice : ")

def medit_parse_edit_name(d, input):
  medit_save = d.olc.save_data
  medit_save.name = input
  d.olc.state = medit_state.MEDIT_MAIN_MENU
  medit_display_main_menu(d)

def medit_parse_edit_ldesc(d, input):
  medit_save = d.olc.save_data
  medit_save.ldesc = input
  d.olc.state = medit_state.MEDIT_MAIN_MENU
  medit_display_main_menu(d)

def medit_parse_confirm_save(d, input, mud, db):
  if input == "":
    d.olc.state = medit_state.MEDIT_MAIN_MENU
    medit_display_main_menu(d)
    return

  response = input[0].upper()

  match response:
    case 'Y':
      medit_save = d.olc.save_data

      zone_id = medit_save.uid.zone_id
      id = medit_save.uid.id

      npcp = mud.npc_by_uid(zone_id, id)

      # if its not found, we're working on a new npc
      if npcp == None:
        npcp = npc_proto_data.npc_proto_data()

        npcp.zone_id = zone_id
        npcp.id = id

      # update in game npc_proto
      npcp.name = medit_save.name
      npcp.desc = medit_save.desc.text
      npcp.ldesc = medit_save.ldesc
      
      npcp.remove_all_aliases()
      for alias in medit_save.aliases:
        npcp.add_alias(alias)

      # update database entry
      db.save_npc_proto(npcp)
      d.write("NPC saved to database.\r\n")

      # update corresponding npcs
      for char in mud.list_characters():
        if isinstance(char, npc_data.npc_data):
          if char.id == id and char.zone_id == zone_id:
            char.name = npcp.name
            char.desc = npcp.desc
            char.ldesc = npcp.ldesc

      d.olc = None
      d.state = descriptor_data.descriptor_state.CHATTING
    case 'N':
      d.olc = None
      d.state = descriptor_data.descriptor_state.CHATTING