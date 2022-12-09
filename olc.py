from color import *
import descriptor
import enum
import logging
import string_handling
import structs
import zedit

class olc_mode(enum.IntEnum):
  OLC_MODE_ZEDIT = 0
  OLC_MODE_REDIT = 1

def handle_input(d, input, server, mud):
  if d.olc.mode == olc_mode.OLC_MODE_ZEDIT:
  	zedit.zedit_parse(d, input, server, mud)
  elif d.olc.mode == olc_mode.OLC_MODE_REDIT:
    zedit.redit_parse(d, input, server, mud)

def do_zlist(ch, scmd, argument, server, mud):

  ch.write(f"             ID Zone Name                      Author\r\n")
  ch.write(f"--------------- ------------------------------ ------\r\n")
  for zone in mud._zones.values():
    ch.write(f"[{GREEN}{zone.id:>13}{NORMAL}] {CYAN}{zone.name:<30}{NORMAL} {YELLOW}{zone.author.capitalize()}{NORMAL}\r\n")

  ch.write(f"\r\nThere are a total of {len(mud._zones)} zones loaded into memory.\r\n")

def do_zedit(ch, scmd, argument, server, mud):
  here = mud.room_by_code(ch.room)
  args = argument.split()
  num_args = len(args)

  if num_args < 1:
    ch.write("Usage: zedit <zone_id>\r\n")
    return

  if args[0] not in mud._zones.keys():
    ch.write("Sorry, that zone wasn't found!\r\n")
    return

  mud.echo_around(ch, None, f"{ch} starts using OLC.\r\n")

  d = ch.d

  d.state = descriptor.descriptor_state.OLC
  d.olc = structs.olc_data(olc_mode.OLC_MODE_ZEDIT, args[0], None, zedit.zedit_state.ZEDIT_MAIN_MENU)
  zedit.zedit_display_main_menu(d, mud.zone_by_id(args[0]))

def do_rlist(ch, scmd, argument, server, mud):
  args = argument.split()
  num_args = len(args)

  if (num_args < 1):
    ch.write("Usage: rlist <zone_id>\r\n")
    return

  if args[0] not in mud._zones.keys():
    ch.write("Sorry, that zone wasn't found!\r\n")
    return

  zone = mud.zone_by_id(args[0])

  num_rooms = len(zone._world.items())

  if num_rooms == 0:
    ch.write("This zone has no rooms!\r\n")
    return

  ch.write(f"             ID Room Name                      Exit\r\n")
  ch.write(f"--------------- ------------------------------ ------\r\n")

  for id,room in zone._world.items():
    ch.write(f"[{GREEN}{id:>13}{NORMAL}] {CYAN}{room.name:<30}{NORMAL}\r\n")

def do_zcreate(ch, scmd, argument, server, mud):
  args = argument.split()
  num_args = len(args)

  if (num_args) < 2:
    ch.write("Usage: zcreate <zone_id> <zone_name>\r\n")
    return;

  new_zone = zone.zone()

  new_zone.author = ch.name
  new_zone.id = args[0]
  new_zone.name = argument[(len(new_zone.id) + 1):]

  ch.write(f"You create zone[{GREEN}{new_zone.id}{NORMAL}] {CYAN}{new_zone.name}{NORMAL}.")
  mud._zones[new_zone.id] = new_zone