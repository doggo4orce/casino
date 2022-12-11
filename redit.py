from color import *
import descriptor
import enum
import exit
import room
import string_handling
import structs

class redit_state(enum.IntEnum):
  REDIT_MAIN_MENU      = 1
  REDIT_EDIT_NAME      = 2
  REDIT_EDIT_DESC      = 3
  REDIT_EDIT_COPY      = 4
  REDIT_CONFIRM_SAVE   = 5
  REDIT_CHANGE_EXIT    = 6

def redit_display_main_menu(d):
  redit_save = d.olc.save_data
  #todo: make sure zedit_save is structs.redit_save_data
  d.write(f"-- Room ID : [{CYAN}{redit_save.room_id}{NORMAL}]        Zone ID : [{CYAN}{redit_save.zone_id}{NORMAL}]\r\n")
  d.write(f"{GREEN}1{NORMAL}) Room Name    : {YELLOW}{redit_save.room_name}{NORMAL}\r\n")
  d.write(f"{GREEN}2{NORMAL}) Description  :\r\n")
  d.write(f"{YELLOW}{string_handling.paragraph(redit_save.room_desc, d.char.prefs.screen_width, True)}{NORMAL}\r\n")
  d.write(f"{GREEN}3{NORMAL}) Copy Room\r\n")

  # index through the next 4 - 9 as exits
  k = 4
  for dir in exit.direction:
    if dir in redit_save.room_exits.keys():
      d.write(f"{GREEN}{k}{NORMAL}) Exit {dir.name.lower():<8}: {CYAN}{redit_save.room_exits[dir]}{NORMAL}\r\n")
    else:
      d.write(f"{GREEN}{k}{NORMAL}) Exit {dir.name.lower():<8}: {CYAN}None{NORMAL}\r\n")
    k = k + 1

  d.write(f"{GREEN}X{NORMAL}) Delete Room\r\n")
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
  elif d.olc.state == redit_state.REDIT_EDIT_COPY:
    redit_parse_edit_copy(d, input, server, mud)
  elif d.olc.state == redit_state.REDIT_CONFIRM_SAVE:
    redit_parse_confirm_save(d, input, server, mud)
  elif d.olc.state == redit_state.REDIT_CHANGE_EXIT:
    redit_parse_change_exit(d, input, server, mud)

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
    d.write("Will create duplicate room with new id : ")
    d.olc.state = redit_state.REDIT_EDIT_COPY

  elif response in {'4', '5', '6', '7', '8', '9'}:
    # this is a bit sloppy but it works for now
    d.write(f"Enter new room to the {exit.direction(int(response) - 4).name.lower()} : ")
    d.olc.state = redit_state.REDIT_CHANGE_EXIT
    d.olc.save_data.dir_edit = exit.direction(int(response) - 4)
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

def redit_parse_edit_copy(d, input, server, mud):
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

      for dir in exit.direction:
        dest = redit_save.room_exits[dir]
        if dest != None:
          check_room.connect(dir, dest)
        else:
          for ex in check_room.exits:
            if ex.direction == dir:
              check_room.disconnect(dir)
              

    else:
      # ok we're making a brand new room filled from redit save
      new_room = room.room()
      new_room.zone_id = redit_save.zone_id
      new_room.name = redit_save.room_name
      new_room.id = redit_save.room_id
      new_room.desc = redit_save.room_desc

      for dir in exit.direction:
        dest = redit_save.room_exits[dir]
        if dest != None:
          new_room.connect(dir, dest)
        else:
          for ex in new_room.exits:
            if ex.direction == dir:
              new_room.disconnect(dir)

      # insert new room into the zone
      # todo make this a function for zone class (add_room)
      mud.zone_by_id(zone_id)._world[room_id] = new_room
    
    d.write("Saving changes.\r\n")
    mud.zone_by_id(zone_id).save_to_folder()
    mud.echo_around(d.char, None, f"{d.char.name} stops using OLC.\r\n")
    d.state = descriptor.descriptor_state.CHATTING
    d.olc.save_data = None
    d.olc = None

  elif input[0] in {'n', 'N'}:
    d.write("Discarding changes.\r\n")
    mud.echo_around(d.char, None, f"{d.char.name} stops using OLC.\r\n")
    d.state = descriptor.descriptor_state.CHATTING
    d.olc.save_data = None
    d.olc = None

def redit_parse_change_exit(d, input, server, mud):
  # figure out which exit we're changing
  dir_edit = d.olc.save_data.dir_edit

  if input == "":
    # give up editing direction for now
    d.olc.save_data.dir_edit = None

    # send them back to main menu
    d.olc.state = redit_state.REDIT_MAIN_MENU
    d.write("Returning to main menu.\r\n")
    d.write("Enter your choice : ")
    return

  args = input.split()
  num_args = len(args)

  # for now let it be the wild west
  d.olc.save_data.room_exits[dir_edit] = args[0]

  if args[0] == "none":
    d.olc.save_data.room_exits[dir_edit] = None

  d.olc.save_data.dir_edit = None

  d.olc.state = redit_state.REDIT_MAIN_MENU
  redit_display_main_menu(d)
  
