from color import *
import descriptor
import enum
import room
import string_handling
import structs

class redit_state(enum.IntEnum):
  REDIT_MAIN_MENU    = 1
  REDIT_EDIT_NAME    = 2
  REDIT_EDIT_DESC    = 3
  REDIT_EDIT_ID      = 4
  REDIT_CONFIRM_SAVE = 5

def redit_display_main_menu(d):
  redit_save = d.olc.save_data
  #todo: make sure zedit_save is structs.redit_save_data
  d.write(f"-- Room ID : [{CYAN}{redit_save.room_id}{NORMAL}]        Zone ID : [{CYAN}{redit_save.zone_id}{NORMAL}]\r\n")
  d.write(f"{GREEN}1{NORMAL}) Room Name    : {YELLOW}{redit_save.room_name}{NORMAL}\r\n")
  d.write(f"{GREEN}2{NORMAL}) Description  :\r\n")
  d.write(f"{YELLOW}{string_handling.paragraph(redit_save.room_desc, d.char.prefs.screen_width, True)}{NORMAL}\r\n")
  d.write(f"{GREEN}3{NORMAL}) Room ID      : {YELLOW}{redit_save.room_id}{NORMAL}\r\n")
  d.write(f"{GREEN}Q{NORMAL}) Quit\r\n")
  d.write(f"\r\nEnter your choice : ")

def redit_parse(d, input, server, mud):
  if d.olc.state == redit_state.REDIT_MAIN_MENU:
    redit_parse_main_menu(d, input, server, mud)
    return

  # we've hit at least one "non-main" menu, so there are unsaved changes
  d.olc.changes = True

  if d.olc.state == redit_state.REDIT_EDIT_NAME:
    redit_parse_edit_name(d, input, server, mud)
  elif d.olc.state == redit_state.REDIT_EDIT_DESC:
    redit_parse_edit_desc(d, input, server, mud)
  elif d.olc.state == redit_state.REDIT_EDIT_ID:
    redit_parse_edit_id(d, input, server, mud)
  elif d.olc.state == redit_state.REDIT_CONFIRM_SAVE:
    redit_parse_confirm_save(d, input, server, mud)

def redit_parse_main_menu(d, input, server, mud):
  if input == "":
    response = 'q'
  else:
    response = input[0]

  if response == '1':
    d.write("Enter new room name : ")
    d.olc.state = redit_state.REDIT_EDIT_NAME
  elif response == '2':
    d.write("Enter new room description : ")
    d.olc.state = redit_state.REDIT_EDIT_DESC
  elif response == '3':
    d.write("Enter new room id : ")
    d.olc.state = redit_state.REDIT_EDIT_ID
  elif response in {'q', 'Q'}:
    if d.olc.changes:
      d.write("Save internally? : ")
      d.olc.state = redit_state.REDIT_CONFIRM_SAVE
    else:
      d.write("No changes to save.\r\n")
      mud.echo_around(d.char, None, f"{d.char.name} stops using OLC.\r\n")
      d.state = descriptor.descriptor_state.CHATTING
      d.olc.save_data = None
      d.olc = None
  else:
    d.write("Returning to main menu.\r\n")
    d.write(f"\r\nEnter your choice : ")
    d.olc.state = redit_state.REDIT_MAIN_MENU

def redit_parse_edit_name(d, input, server, mud):
  d.olc.save_data.room_name = input
  d.olc.state = redit_state.REDIT_MAIN_MENU
  redit_display_main_menu(d)

def redit_parse_edit_desc(d, input, server, mud):
  d.olc.save_data.room_desc = input
  d.olc.state = redit_state.REDIT_MAIN_MENU
  redit_display_main_menu(d)

def redit_parse_edit_id(d, input, server, mud):
  args = input.split()
  new_room_id = args[0]

  d.olc.save_data.room_id = args[0]
  d.olc.state = redit_state.REDIT_MAIN_MENU
  redit_display_main_menu(d)

def redit_parse_confirm_save(d, input, server, mud):
  redit_save = d.olc.save_data
  zone_id = redit_save.zone_id
  room_id = redit_save.room_id
  if input == "" or input[0] not in {'n', 'N', 'y', 'Y'}:
    d.write("Returning to main menu.\r\n")
    d.write("Enter your choice : ")
    d.olc.state = redit_state.REDIT_MAIN_MENU
    return
  elif input[0] in {'y','Y'}:
    check_room = mud.room_by_code(structs.unique_identifier(zone_id, room_id))

    if check_room != None:
      # we found an existing room, overwrite it with redit_save
      check_room.zone_id = redit_save.zone_id
      check_room.name = redit_save.room_name
      check_room.id = redit_save.room_id
      check_room.desc = redit_save.room_desc
    else:
      # ok we're making a brand new room filled from redit save
      new_room = room.room()
      new_room.zone_id = redit_save.zone_id
      new_room.name = redit_save.room_name
      new_room.id = redit_save.room_id
      new_room.desc = redit_save.room_desc

      # insert new room into the zone
      # todo make this a function for zone class (add_room)
      mud.zone_by_id(zone_id)._world[room_id] = new_room
    
    d.write("Saving changes.\r\n")
    mud.zone_by_id(zone_id).save_to_folder()
    mud.echo_around(d.char, None, f"{d.char.name} stops using OLC.\r\n")
    d.state = descriptor.descriptor_state.CHATTING
    d.olc.save_data = None
    d.olc = None


def zedit_parse_confirm_save(d, input, server, mud):
  zone_id = d.olc.save_data.zone_id

  if input == "" or input[0] not in {'n', 'N', 'y', 'Y'}:
    d.write("Returning to main menu.\r\n")
    d.write("Enter your choice : ")
    d.olc.state = zedit_state.ZEDIT_MAIN_MENU
    return
  elif input[0] in {'y','Y'}:
    check_zone = mud.zone_by_id(zone_id)

    zedit_save = d.olc.save_data
    
    if check_zone != None:
      # we found an existing zone, overwrite it with zedit_save
      zone.name = zedit_save.zone_name
      zone.id = zedit_save.zone_id
      zone.author = zedit_save.zone_author
      zone.folder = zedit_save.zone_folder
    else:
      # ok we're making a brand new zone filled from zedit save
      new_zone = zone.zone()
      new_zone.name = zedit_save.zone_name
      new_zone.id = zedit_save.zone_id
      new_zone.author = zedit_save.zone_author
      new_zone.folder = zedit_save.zone_folder

      # insert new zone into the world
      mud._zones[zone_id] = new_zone
    
    d.write("Saving changes internally.\r\n")
    mud.echo_around(d.char, None, f"{d.char.name} stops using OLC.\r\n")
    d.state = descriptor.descriptor_state.CHATTING
    d.olc.save_data = None
    d.olc = None

  elif input[0] in {'n', 'N'}:
    d.write("Discarding unsaved changes.\r\n")
    mud.echo_around(d.char, None, f"{d.char.name} stops using OLC.\r\n")
    d.state = descriptor.descriptor_state.CHATTING
    d.olc.save_data = None
    d.olc = None

  d.write("")


