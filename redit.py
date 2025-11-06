import buffer_data
from color import *
import descriptor_data
import editor
import enum
import exit_data
import room_data
import string_handling

class redit_state(enum.IntEnum):
  REDIT_MAIN_MENU      = 1
  REDIT_EDIT_NAME      = 2
  REDIT_EDIT_DESC      = 3
  REDIT_EDIT_COPY      = 4
  REDIT_CONFIRM_SAVE   = 5
  REDIT_CHANGE_EXIT    = 6

def redit_display_main_menu(d):
  redit_save = d.olc.save_data
  desc_buffer = buffer_data.buffer_data(redit_save.attributes.desc)

  #todo: make sure zedit_save is structs.redit_save_data
  d.write(f"-- Room ID : [{CYAN}{redit_save.uid.id}{NORMAL}]        Zone ID : [{CYAN}{redit_save.uid.zone_id}{NORMAL}]\r\n")
  d.write(f"{GREEN}1{NORMAL}) Room Name    : {YELLOW}{redit_save.attributes.name}{NORMAL}\r\n")
  d.write(f"{GREEN}2{NORMAL}) Description  :\r\n")
  d.write(f"{desc_buffer.clean_up().display(d.character.page_width, indent=True, color=True)}{NORMAL}\r\n")
  d.write(f"{GREEN}3{NORMAL}) Copy Room\r\n")

  # index through the next 4 - 9 as exits
  k = 4
  for dir in exit_data.direction:
    destination = redit_save.destination(dir)
    if destination is not None:
      d.write(f"{GREEN}{k}{NORMAL}) Exit {dir.name.lower():<8}: {CYAN}{destination}{NORMAL}\r\n")
    else:
      d.write(f"{GREEN}{k}{NORMAL}) Exit {dir.name.lower():<8}: {CYAN}None{NORMAL}\r\n")
    k = k + 1

  d.write(f"{GREEN}X{NORMAL}) Delete Room\r\n")
  d.write(f"{GREEN}Q{NORMAL}) Quit\r\n")
  d.write(f"\r\nEnter your choice : ")

def redit_parse(d, input, server, mud, db):
  if d.olc.state == redit_state.REDIT_MAIN_MENU:
    redit_parse_main_menu(d, input, server, mud) 
  elif d.olc.state == redit_state.REDIT_EDIT_NAME:
    redit_parse_edit_name(d, input, server, mud)
  elif d.olc.state == redit_state.REDIT_EDIT_COPY:
    redit_parse_edit_copy(d, input, server, mud)
  elif d.olc.state == redit_state.REDIT_CONFIRM_SAVE:
    redit_parse_confirm_save(d, input, server, mud, db)
  elif d.olc.state == redit_state.REDIT_CHANGE_EXIT:
    redit_parse_change_exit(d, input, server, mud)

def redit_parse_main_menu(d, input, server, mud):
  if input == "":
    response = 'q'
  else:
    response = input[0]

  if response not in {'q', 'Q'}:
    # we've done at least one thing aside from quit
    d.olc.changes = True

  if response == '1':
    d.write("Enter new room name : ")
    d.olc.state = redit_state.REDIT_EDIT_NAME
  elif response == '2':
    d.write("Instructions: /s to save, /h for more options.")
    redit_save = d.olc.save_data
    d.olc.state = redit_state.REDIT_EDIT_DESC
    d.start_writing(redit_save.attributes.desc)
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
      mud.echo_around(d.character, None, f"{d.character.Name} stops using OLC.\r\n")
      d.state = descriptor_data.descriptor_state.CHATTING
      d.write_buffer = None
      d.olc.save_data = None
      d.olc = None
  else:
    d.write("Returning to main menu.\r\n")
    d.write(f"\r\nEnter your choice : ")
    d.olc.state = redit_state.REDIT_MAIN_MENU

def redit_parse_edit_name(d, input, server, mud):
  d.olc.save_data.attributes.name = input
  d.olc.state = redit_state.REDIT_MAIN_MENU
  redit_display_main_menu(d)

def redit_parse_edit_copy(d, input, server, mud):
  args = input.split()
  new_room_id = args[0]

  d.olc.save_data.room_id = args[0]
  d.olc.state = redit_state.REDIT_MAIN_MENU
  redit_display_main_menu(d)

def redit_parse_confirm_save(d, input, server, mud, db):
  redit_save = d.olc.save_data
  zone_id = redit_save.attributes.uid.zone_id
  room_id = redit_save.attributes.uid.id
  if input == "" or input[0] not in {'n', 'N', 'y', 'Y'}:
    d.write("Returning to main menu.\r\n")
    d.write("Enter your choice : ")
    d.olc.state = redit_state.REDIT_MAIN_MENU
    return
  elif input[0] in {'y','Y'}:
    check_room = mud.room_by_uid(zone_id, room_id)

    if check_room != None:
      # we found an existing room, overwrite it with redit_save
      check_room.zone_id = redit_save.attributes.uid.zone_id
      check_room.name = redit_save.attributes.name
      check_room.id = redit_save.uid.id
      check_room.desc = redit_save.attributes.desc

      for dir in exit_data.direction:
        dest = redit_save.destination(dir)
        if dest is not None:
          check_room.connect(dir, dest.zone_id, dest.id)
        else:
          check_room.disconnect(dir)
    else:
      # ok we're making a brand new room filled from redit save
      new_room = room_data.room_data()
      new_room.zone_id = redit_save.attributes.uid.zone_id
      new_room.name = redit_save.attributes.name
      new_room.id = redit_save.attributes.uid.id
      new_room.desc = redit_save.attributes.desc

      for dir in exit_data.direction:
        dest = redit_save.destination(dir)
        if dest is not None:
          new_room.connect(dir, dest.zone_id, dest.id)

      # insert new room into the zone
      mud.zone_by_id(zone_id).add_room(new_room)
 
    # do a reset for the next time.  This is sloppy and needs to be fixed
    # nov 4, 25: why is this necessary?  shouldn't we create a new blank RSD next time?
    # for dir in exit_data.direction:
    #   redit_save.connect(dir, None, None)

    d.write("Saving changes.\r\n")
    mud.echo_around(d.character, None, f"{d.character.Name} stops using OLC.\r\n")
    d.state = descriptor_data.descriptor_state.CHATTING
    d.olc.save_data = None
    d.olc = None

    db.save_room(check_room)

  elif input[0] in {'n', 'N'}:
    d.write("Discarding changes.\r\n")
    mud.echo_around(d.character, None, f"{d.character.Name} stops using OLC.\r\n")
    d.state = descriptor_data.descriptor_state.CHATTING
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
  
