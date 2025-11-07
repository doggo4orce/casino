from color import *
import config
import descriptor_data
import enum
import exit_data
import os
import string_handling
import room_data
import zone_data

class zedit_state(enum.IntEnum):
  ZEDIT_MAIN_MENU    = 1
  ZEDIT_EDIT_NAME    = 2
  ZEDIT_EDIT_AUTHOR  = 3
  ZEDIT_EDIT_COPY    = 4
  ZEDIT_CONFIRM_SAVE = 5

def zedit_display_main_menu(d):
  zedit_save = d.olc.save_data
  #todo: make sure zedit_save is structs.zedit_save_data

  d.write(f"[{GREEN}{zedit_save.id}{NORMAL}] {CYAN}{zedit_save.name}{NORMAL}\r\n")
  d.write(f"\r\n")
  d.write(f"{GREEN}1{NORMAL}) Author       : {YELLOW}{zedit_save.author}{NORMAL}\r\n")
  d.write(f"{GREEN}2{NORMAL}) Zone Name    : {YELLOW}{zedit_save.name}{NORMAL}\r\n")
  d.write(f"{GREEN}3{NORMAL}) Copy Zone\r\n")
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
  d.olc.save_data.author = input
  d.olc.state = zedit_state.ZEDIT_MAIN_MENU
  zedit_display_main_menu(d)

def zedit_parse_edit_name(d, input, server, mud):
  d.olc.save_data.name = input
  d.olc.state = zedit_state.ZEDIT_MAIN_MENU
  zedit_display_main_menu(d)
  
def zedit_parse_edit_copy(d, input, server, mud):
  args = input.split()
  new_zone_id = args[0]
  old_zone_id = d.olc.save_data.id
  if new_zone_id == old_zone_id:
    d.write("That's the same id!\r\n")
    d.olc.state = ZEDIT_MAIN_MENU
    zedit_display_main_menu(d)
    return
  elif new_zone_id in mud._zones.keys():
    d.write("That id is already being used for another zone.\r\n")
    d.write("Try again : ")
    return

  d.olc.save_data.id = new_zone_id
  d.olc.save_data.name = "copy of " + d.olc.save_data.name

  # make the new zone
  new_zone = zone.zone()

  # copy main attributes
  new_zone.name = d.olc.save_data.name
  new_zone.id = new_zone_id
  new_zone.author = d.olc.save_data.author
  
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
    for dir in exit.direction:
      if dir in rm.exits.keys():
        # TODO: this will eventually cause a crash because
        # the connect function will be re-written to accept an exit
        # object rather than a direction and a vref
        rm2.connect(dir, rm.get_destination(dir))

    # insert the new room into the zone
    new_zone._world[rm.id] = rm2

  # todo: do the same thing for objects and npcs

  # insert the new zone into the world  
  mud._zones[new_zone_id] = new_zone
  d.olc.state = zedit_state.ZEDIT_MAIN_MENU
  zedit_display_main_menu(d)

def zedit_parse_confirm_save(d, input, server, mud, db):
  zone_id = d.olc.save_data.id

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
      check_zone.name = zedit_save.name
      check_zone.id = zone_id
      check_zone.author = zedit_save.author

    else:
      # ok we're making a brand new zone filled from zedit save
      new_zone = zone_data.zone_data()
      new_zone.name = zedit_save.name
      new_zone.id = zedit_save.id
      new_zone.author = zedit_save.author

      # insert new zone into the world
      mud._zones[zone_id] = new_zone
    
    d.write("Saving changes.\r\n")
    mud.echo_around(d.character, None, f"{d.character.name} stops using OLC.\r\n")
    d.state = descriptor_data.descriptor_state.CHATTING
    d.olc.save_data = None
    d.olc = None

  elif input[0] in {'n', 'N'}:
    d.write("Discarding changes.\r\n")
    mud.echo_around(d.character, None, f"{d.character.name} stops using OLC.\r\n")
    d.state = descriptor_data.descriptor_state.CHATTING
    d.olc.save_data = None
    d.olc = None

  d.write("")
