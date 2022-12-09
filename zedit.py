from color import *
import config
import descriptor
import enum
import os
import string_handling

class zedit_state(enum.IntEnum):
  ZEDIT_MAIN_MENU   = 1
  ZEDIT_EDIT_NAME   = 2
  ZEDIT_EDIT_AUTHOR = 3
  ZEDIT_EDIT_ID     = 4
  ZEDIT_EDIT_FOLDER = 5

def zedit_display_main_menu(d, zone):
  d.write(f"[{GREEN}{zone.id}{NORMAL}] {CYAN}{zone.name}{NORMAL}\r\n")
  d.write(f"\r\n")
  d.write(f"{GREEN}1{NORMAL}) Author       : {YELLOW}{zone.author}{NORMAL}\r\n")
  d.write(f"{GREEN}2{NORMAL}) Zone Name    : {YELLOW}{zone.name}{NORMAL}\r\n")
  d.write(f"{GREEN}3{NORMAL}) Folder Name  : {YELLOW}{zone.folder}{NORMAL}\r\n")
  #d.write(f"{GREEN}3{NORMAL}) Zone ID      : {YELLOW}{zone.id}{NORMAL}\r\n")
  d.write(f"{GREEN}Q{NORMAL}) Quit\r\n")
  d.write(f"\r\nEnter your choice : ")

def zedit_parse(d, input, server, mud):
  if d.olc.state == zedit_state.ZEDIT_MAIN_MENU:
    zedit_parse_main_menu(d, input, server, mud)
  elif d.olc.state == zedit_state.ZEDIT_EDIT_NAME:
    zedit_parse_edit_name(d, input, server, mud)
  elif d.olc.state == zedit_state.ZEDIT_EDIT_AUTHOR:
    zedit_parse_edit_author(d, input, server, mud)
  elif d.olc.state == zedit_state.ZEDIT_EDIT_ID:
    zedit_parse_edit_id(d, input, server, mud)
  elif d.olc.state == zedit_state.ZEDIT_EDIT_FOLDER:
    zedit_parse_edit_folder(d, input, server, mud)

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
  else: #if response in {'q', 'Q'}:
    d.write("Leaving editor.\r\n")
    d.state = descriptor.descriptor_state.CHATTING
    d.olc = None

def zedit_parse_edit_author(d, input, server, mud):
  zone = mud.zone_by_id(d.olc.zone_id)
  zone.author = input
  d.olc.state = zedit_state.ZEDIT_MAIN_MENU
  zedit_display_main_menu(d, zone)

def zedit_parse_edit_name(d, input, server, mud):
  zone = mud.zone_by_id(d.olc.zone_id)
  zone.name = input
  d.olc.state = zedit_state.ZEDIT_MAIN_MENU
  zedit_display_main_menu(d, zone)

def zedit_parse_edit_folder(d, input, server, mud):
  zone = mud.zone_by_id(d.olc.zone_id)
  old_folder = zone.folder

  if not string_handling.alpha_numeric_space(input):
    d.write("Sorry, folder names can only have alphanumeric characters.\r\n")
    d.write("Try again : ")
    return

  zone.folder = input
  os.rename(config.WORLD_FOLDER + old_folder, config.WORLD_FOLDER + input)

  d.olc.state = zedit_state.ZEDIT_MAIN_MENU
  zedit_display_main_menu(d, zone)
  
def zedit_parse_edit_id(d, input, server, mud):
  old_zone_id = d.olc.zone_id
  zone = mud.zone_by_id(old_zone_id)
  args = input.split()

  if zone.id == args[0]:
    d.write("That's the same id!\r\n")
    d.olc.state = ZEDIT_MAIN_MENU
    zedit_display_main_menu(d, zone)
    return
  elif args[0] in mud._zones.keys():
    d.write("That id is already being used for another zone.\r\n")
    d.write("Try again : ")
    return
  
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
  zedit_display_main_menu(d, zone)