from color import *
import descriptor
import enum
import logging
import string_handling

class olc_mode(enum.IntEnum):
  OLC_MODE_ZEDIT = 0
  OLC_MODE_REDIT = 1

class redit_state(enum.IntEnum):
  REDIT_MAIN_MENU = 1
  REDIT_EDIT_NAME = 2
  REDIT_EDIT_DESC = 3
  REDIT_EDIT_EXIT = 4

class zedit_state(enum.IntEnum):
  ZEDIT_MAIN_MENU   = 1
  ZEDIT_EDIT_NAME   = 2
  ZEDIT_EDIT_AUTHOR = 3
  ZEDIT_EDIT_ID     = 4

def zedit_display_main_menu(d, zone):
  d.write(f"[{GREEN}{zone.id}{NORMAL}] {CYAN}{zone.name}{NORMAL}\r\n")
  d.write(f"\r\n")
  d.write(f"{GREEN}1{NORMAL}) Author       : {YELLOW}{zone.author}{NORMAL}\r\n")
  d.write(f"{GREEN}2{NORMAL}) Zone Name    : {YELLOW}{zone.name}{NORMAL}\r\n")
  d.write(f"{GREEN}3{NORMAL}) Zone ID      : {YELLOW}{zone.id}{NORMAL}\r\n")
  d.write(f"{GREEN}Q{NORMAL}) Quit\r\n")
  d.write(f"Enter your choice : ")

def handle_input(d, input, server, mud):

  if d.olc.mode == olc_mode.OLC_MODE_ZEDIT:
  	zedit_parse(d, input, server, mud)
  elif d.olc.mode == olc_mode.OLC_MODE_REDIT:
    redit_parse(d, input, server, mud)

def zedit_parse(d, input, server, mud):
  if d.olc.state == zedit_state.ZEDIT_MAIN_MENU:
  	zedit_parse_main_menu(d, input, server, mud)
  elif d.olc.state == zedit_state.ZEDIT_EDIT_NAME:
  	zedit_parse_edit_name(d, input, server, mud)
  elif d.olc.state == zedit_state.ZEDIT_EDIT_AUTHOR:
  	zedit_parse_edit_author(d, input, server, mud)
  elif d.olc.state == zedit_state.ZEDIT_EDIT_ID:
  	zedit_parse_edit_id(d, input, server, mud)

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
    d.write("Enter new id : ")
    d.olc.state = zedit_state.ZEDIT_EDIT_ID
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
  
  new_zone_id = args[0]
  del mud._zones[old_zone_id]
  zone.id = new_zone_id
  mud._zones[zone.id] = zone
  d.olc.zone_id = zone.id

  # go through all mobs/characters that are in that zone, and move them to the new copy
  for ch in mud._chars:
    zone_id, room_id = string_handling.parse_reference(ch.room)

    if zone_id == old_zone_id:
      ch.room = f"{new_zone_id}[{room_id}]"

  # go through all exits from zones (including this one) that lead into that zone and update them
  for zone in mud._zones.values():
    for room in zone._world.values():
      for exit in room._exits:
        if exit.zone == old_zone_id:
          exit.zone = new_zone_id
      
  d.olc.state = zedit_state.ZEDIT_MAIN_MENU
  zedit_display_main_menu(d, zone)