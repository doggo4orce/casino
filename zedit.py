from color import *
import config
import descriptor
import enum
import os
import string_handling
import room
import zone

class zedit_state(enum.IntEnum):
  ZEDIT_MAIN_MENU    = 1
  ZEDIT_EDIT_NAME    = 2
  ZEDIT_EDIT_AUTHOR  = 3
  ZEDIT_EDIT_COPY    = 4
  ZEDIT_EDIT_FOLDER  = 5
  ZEDIT_CONFIRM_SAVE = 6

def zedit_display_main_menu(d):
  zedit_save = d.olc.save_data
  #todo: make sure zedit_save is structs.zedit_save_data

  d.write(f"[{GREEN}{zedit_save.zone_id}{NORMAL}] {CYAN}{zedit_save.zone_name}{NORMAL}\r\n")
  d.write(f"\r\n")
  d.write(f"{GREEN}1{NORMAL}) Author       : {YELLOW}{zedit_save.zone_author}{NORMAL}\r\n")
  d.write(f"{GREEN}2{NORMAL}) Zone Name    : {YELLOW}{zedit_save.zone_name}{NORMAL}\r\n")
  d.write(f"{GREEN}3{NORMAL}) Folder Name  : {YELLOW}lib/world/{BRIGHT_YELLOW}{zedit_save.zone_folder}{NORMAL}{YELLOW}/{NORMAL}\r\n")
  d.write(f"{GREEN}4{NORMAL}) Copy Zone\r\n")
  d.write(f"{GREEN}Q{NORMAL}) Quit\r\n")
  d.write(f"\r\nEnter your choice : ")

def zedit_parse(d, input, server, mud):
  if d.olc.state == zedit_state.ZEDIT_MAIN_MENU:
    zedit_parse_main_menu(d, input, server, mud)
    return

  # we've hit at least one "non-main" menu, so there are unsaved changes
  d.olc.changes = True

  if d.olc.state == zedit_state.ZEDIT_EDIT_NAME:
    zedit_parse_edit_name(d, input, server, mud)
  elif d.olc.state == zedit_state.ZEDIT_EDIT_AUTHOR:
    zedit_parse_edit_author(d, input, server, mud)
  elif d.olc.state == zedit_state.ZEDIT_EDIT_COPY:
    zedit_parse_edit_copy(d, input, server, mud)
  elif d.olc.state == zedit_state.ZEDIT_EDIT_FOLDER:
    zedit_parse_edit_folder(d, input, server, mud)
  elif d.olc.state == zedit_state.ZEDIT_CONFIRM_SAVE:
    zedit_parse_confirm_save(d, input, server, mud)

def zedit_parse_main_menu(d, input, server, mud):
  # simple way to handle null input for now
  if input == "":
    response = 'q'
  else:
    response = input[0]

  if response == '1':
    d.write("Enter new author : ")
    d.olc.state = zedit_state.ZEDIT_EDIT_AUTHOR
  elif response == '2':
    d.write("Enter new name : ")
    d.olc.state = zedit_state.ZEDIT_EDIT_NAME
  elif response == '3':
    d.write("Enter new folder name : ")
    d.olc.state = zedit_state.ZEDIT_EDIT_FOLDER
  elif response == '4':
    d.write("Will create duplicate zone with new id : ")
    d.olc.state = zedit_state.ZEDIT_EDIT_COPY
  elif response in {'q', 'Q'}:
    if d.olc.changes:
      d.write("Save internally? : ")
      d.olc.state = zedit_state.ZEDIT_CONFIRM_SAVE
    else:
      d.write("No changes to save.\r\n")
      mud.echo_around(d.char, None, f"{d.char.name} stops using OLC.\r\n")
      d.state = descriptor.descriptor_state.CHATTING
      d.olc.save_data = None
      d.olc = None
  else:
    d.write("Returning to main menu.\r\n")
    d.write(f"\r\nEnter your choice : ")
    d.olc.state = zedit_state.ZEDIT_MAIN_MENU

def zedit_parse_edit_author(d, input, server, mud):
  d.olc.save_data.zone_author = input
  d.olc.state = zedit_state.ZEDIT_MAIN_MENU
  zedit_display_main_menu(d)

def zedit_parse_edit_name(d, input, server, mud):
  d.olc.save_data.zone_name = input
  d.olc.state = zedit_state.ZEDIT_MAIN_MENU
  zedit_display_main_menu(d)

def zedit_parse_edit_folder(d, input, server, mud):
  if not string_handling.alpha_numeric_space(input):
    d.write("Sorry, folder names can only have alphanumeric characters.\r\n")
    d.write("Try again : ")
    return
  d.olc.save_data.zone_folder = input
  d.olc.state = zedit_state.ZEDIT_MAIN_MENU
  zedit_display_main_menu(d)
  
def zedit_parse_edit_copy(d, input, server, mud):
  args = input.split()
  new_zone_id = args[0]
  old_zone_id = d.olc.save_data.zone_id
  if new_zone_id == old_zone_id:
    d.write("That's the same id!\r\n")
    d.olc.state = ZEDIT_MAIN_MENU
    zedit_display_main_menu(d)
    return
  elif new_zone_id in mud._zones.keys():
    d.write("That id is already being used for another zone.\r\n")
    d.write("Try again : ")
    return

  d.olc.save_data.zone_id = new_zone_id
  d.olc.save_data.zone_name = "copy of " + d.olc.save_data.zone_name
  d.olc.save_data.zone_folder = "copy of " + d.olc.save_data.zone_folder

  # make the new zone
  new_zone = zone.zone()

  # copy main attributes
  new_zone.name = d.olc.save_data.zone_name
  new_zone.id = new_zone_id
  new_zone.author = d.olc.save_data.zone_author
  new_zone.folder = d.olc.save_data.zone_folder
  
  # going through each of the rooms in the old zone
  for rm in mud._zones[old_zone_id]._world.values():
    # make 
    rm2 = room.room()

    # copy basic attributes
    rm2.zone_id = new_zone_id
    rm2.id = rm.id
    rm2.name = rm.name
    rm2.desc = rm.desc

    # copy all the exits
    for ex in rm.exits:
      # just copying all the destinations, which is easily breakable
      rm2.connect(ex.direction, ex.destination)

    # insert the new room into the zone
    new_zone._world[rm.id] = rm2

  # insert the new zone into the world  
  mud._zones[new_zone_id] = new_zone
  d.olc.state = zedit_state.ZEDIT_MAIN_MENU
  zedit_display_main_menu(d)

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
      check_zone.name = zedit_save.zone_name
      check_zone.id = zone_id
      check_zone.author = zedit_save.zone_author
      check_zone.folder = zedit_save.zone_folder
      check_zone.save_to_folder()
    else:
      # ok we're making a brand new zone filled from zedit save
      new_zone = zone.zone()
      new_zone.name = zedit_save.zone_name
      new_zone.id = zedit_save.zone_id
      new_zone.author = zedit_save.zone_author
      new_zone.folder = zedit_save.zone_folder
      new_zone.save_to_folder()

      # insert new zone into the world
      mud._zones[zone_id] = new_zone
    
    d.write("Saving changes.\r\n")
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

  d.write("")


# for handling the actual saved changes
def or_dont_call_this_function_either(d, input, server, mud):
  os.rename(config.WORLD_FOLDER + old_folder, config.WORLD_FOLDER + input)

def dont_call_this_function(d, input, server, mud):
  # move zone to have new key
  new_zone_id = args[0]
  del mud._zones[old_zone_id]
  zone.id = new_zone_id
  mud._zones[zone.id] = zone
  d.olc.zone_id = zone.id

  # go through all characters that are in that zone, and move them to the new copy
  for ch in mud._chars:
    room_unique_id = ch.room
    if ch.room.zone_id == old_zone_id:
      ch.room = f"{new_zone_id}[{room_id}]"

      

  for obj in mud._objects:
    zone_id, room_id = string_handling.parse_reference()

  # go through all exits from zones (including this one) that lead into that zone and update them
  for zone in mud._zones.values():
    for room in zone._world.values():
      for exit in room._exits:
        if exit.zone == old_zone_id:
          exit.zone = new_zone_id
      
  d.olc.state = zedit_state.ZEDIT_MAIN_MENU
  zedit_display_main_menu(d)