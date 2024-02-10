from color import *
import config
import descriptor
import enum
import exit
import logging
import redit
import string_handling
import structs
import zedit

class olc_mode(enum.IntEnum):
  OLC_MODE_ZEDIT = 0
  OLC_MODE_REDIT = 1

def handle_input(d, input, server, mud, db):
  if d.olc.mode == olc_mode.OLC_MODE_ZEDIT:
  	zedit.zedit_parse(d, input, server, mud)
  elif d.olc.mode == olc_mode.OLC_MODE_REDIT:
    redit.redit_parse(d, input, server, mud, db)

def olc_writing_follow_up(d):
  if d.olc.mode == olc_mode.OLC_MODE_REDIT:
    if d.olc.state == redit.redit_state.REDIT_MAIN_MENU:
      redit.redit_display_main_menu(d)
  else:
    d.write("You shouldn't see this!\r\n")
    
def do_mlist(ch, scmd, argument, server, mud, db):
  args = argument.split()
  num_args = len(args)

  if num_args == 0:
    zone_id = ch.room.zone_id
    zone = mud.zone_by_id(zone_id)
  elif num_args == 1:
    if args[0] not in mud._zones.keys():
      ch.write("Sorry, that zone wasn't found.\r\n")
      return
    zone = mud.zone_by_id(args[0])

  num_npcs = len(zone._npc_proto.items())

  if num_npcs == 0:
    ch.write("This zone has no npcs!\r\n")
    return

  ch.write(f"ID{(1 + config.MAX_NPC_ID_LENGTH)*' '}Room Name{(config.MAX_NPC_NAME_LENGTH)*' '}\r\n")
  ch.write(f"{(2 + config.MAX_NPC_ID_LENGTH)*'-'} {config.MAX_NPC_NAME_LENGTH*'-'}\r\n")

  for id, npc in zone._npc_proto.items():
    ch.write(f"[{GREEN}{id:>{config.MAX_NPC_ID_LENGTH}}{NORMAL}] {CYAN}{npc.entity.name:<30}{NORMAL}\r\n")

def do_olist(ch, scmd, argument, server, mud, db):
  args = argument.split()
  num_args = len(args)

  if num_args == 0:
    zone_id = ch.room.zone_id
    zone = mud.zone_by_id(zone_id)
  elif num_args == 1:
    if args[0] not in mud._zones.keys():
      ch.write("Sorry, that zone wasn't found.\r\n")
      return
    zone = mud.zone_by_id(args[0])

  num_objs = len(zone._obj_proto.items())

  if num_objs == 0:
    ch.write("This zone has no objects!\r\n")
    return

  ch.write(f"ID{(1 + config.MAX_OBJECT_ID_LENGTH)*' '}Room Name{(config.MAX_OBJECT_NAME_LENGTH)*' '}\r\n")
  ch.write(f"{(2 + config.MAX_OBJECT_ID_LENGTH)*'-'} {config.MAX_OBJECT_NAME_LENGTH*'-'}\r\n")

  for id, obj in zone._obj_proto.items():
    ch.write(f"[{GREEN}{id:>{config.MAX_OBJECT_ID_LENGTH}}{NORMAL}] {CYAN}{obj.entity.name:<30}{NORMAL}\r\n")

def do_rlist(ch, scmd, argument, server, mud, db):
  Usage = "Usage: rlist [zone_id]\r\n"
  args = argument.split()
  num_args = len(args)


  if num_args == 0:
    zone_id = ch.room.zone_id
    zone = mud.zone_by_id(zone_id)
  elif num_args == 1:
    if args[0] not in mud._zones.keys():
      ch.write("Sorry, that zone wasn't found.\r\n")
      return
    zone = mud.zone_by_id(args[0])
  else:
    ch.write(Usage)
    return

  num_rooms = len(zone._world)

  if num_rooms == 0:
    ch.write("This zone has no rooms!\r\n")
    return

  ch.write(f"ID{(1 + config.MAX_ROOM_ID_LENGTH)*' '}Room Name{(config.MAX_ROOM_NAME_LENGTH - 8)*' '}Exit\r\n")
  ch.write(f"{(2 + config.MAX_ROOM_ID_LENGTH)*'-'} {config.MAX_ROOM_NAME_LENGTH*'-'} {(2 + config.MAX_ZONE_ID_LENGTH)*'-'}\r\n")

  for id, room in zone._world.items():
    ch.write(f"[{GREEN}{id:>{config.MAX_ROOM_ID_LENGTH}}{NORMAL}] {CYAN}{room.name:<30}{NORMAL}\r\n")

def do_redit(ch, scmd, argument, server, mud, db):
  Usage = "Usage: redit [[zone_id ]room_id]"

  zone_id = ch.room.zone_id
  room_id = ch.room.id

  args = argument.split()
  num_args = len(args)

  redit_save = structs.redit_save_data()

  # in this case it's redit <zone_id> <room_id>
  if num_args == 2:
    zone_id = args[0]
    room_id = args[1]
  # in this case it's redit <room_id>
  elif num_args == 1:
    room_id = args[0]
    # zone_id = ch.room.zone_id  (just copied as reminded, this is default value)
  elif num_args == 0:
    # zone_id and room_id are already set to appropriate default values
    pass
  else:
    ch.write(Usage)
    return

  # either it was specified as an argument, or its the zone we're in
  zone = mud.zone_by_id(zone_id)

  # so the only way this could happen is if it was specified as an argument
  if zone == None:
    ch.write("Sorry, that zone was not found, you'll have to create it first with ZEDIT.\r\n")
    return

  # not finished with sanity checks!
  if not string_handling.valid_id(room_id):
    ch.write("Room ID's may consist of numbers, letters, or underscores.\r\n")
    return

  # otherwise zone was found and this is safe
  rm = zone.room_by_id(room_id)
  
  # we can copy the id into the redit_save now because it's the same even if we have to create the room
  redit_save.uid = structs.unique_identifier(zone_id, room_id)

  # TODO: replace this with a function: redit_save.from_room(rm)
  # if a room was found we'll load it's info into redit_save now
  if rm != None:
    redit_save.room_name = rm.name
    redit_save.room_desc = rm.desc.make_copy()

    # make a copy of all the exits as strings of either internal or external references
    for dir in exit.direction:
      redit_save.room_exits[dir] = rm.get_destination(dir) # some of these will be None!

  mud.echo_around(ch, None, f"{ch.name} starts using OLC (redit).\r\n")
  ch.d.olc = structs.olc_data(olc_mode.OLC_MODE_REDIT, redit.redit_state.REDIT_MAIN_MENU, False, redit_save)
  ch.d.state = descriptor.descriptor_state.OLC
  redit.redit_display_main_menu(ch.d)

def do_zedit(ch, scmd, argument, server, mud, db):
  Usage = "Usage: zedit [zone_id]\r\n"
  args = argument.split()
  num_args = len(args)

  zedit_save = structs.zedit_save_data()

  # if we make it past this check, correct syntax may be assumed
  if num_args > 2 or (num_args == 2 and args[0] != 'new'):
    ch.write(Usage)
    return
  
  # if no arguments are given, then use the zone ch is standing in
  if num_args == 0:
    zone_id = ch.room.zone_id
  # if one argument is given, the argument should be the zone_id
  elif num_args == 1:
    zone_id = args[0]
  # if two arguments are given, then args[0] and args[1] are 'new' and the new zone_id
  elif num_args == 2:
    zone_id = args[1]
    # check to see if we're trying to use a zone_id that is already in use
    if mud.zone_by_id(zone_id) != None:
      ch.write(f"That zone already exists.  Type: zedit {zone_id} to edit it instead!\r\n")
      return

  if not structs.string_handling.valid_id(zone_id):
    ch.write("That's not a valid zone id!\r\n")
    return

  # if zone == None here, that means we are making a new zone
  zone = mud.zone_by_id(zone_id)

  # future concern1: what if someone else creates a zone right now with the same id?
  # answer: if they save first, we'll save over them
  # future concern2: prevent folder collisions?

  if zone == None:
    # make OLC data for new zone
    zedit_save.zone_id = args[0]
    zedit_save.zone_name = "new zone"
    zedit_save.zone_folder = "new zone"
    zedit_save.zone_author = ch.Name
  else:
    # make OLC data for existing zone
    zedit_save.zone_id = zone.id
    zedit_save.zone_name = zone.name
    zedit_save.zone_folder = zone.folder
    zedit_save.zone_author = zone.author

  mud.echo_around(ch, None, f"{ch.name} starts using OLC (zedit).\r\n")
  ch.d.olc = structs.olc_data(olc_mode.OLC_MODE_ZEDIT, zedit.zedit_state.ZEDIT_MAIN_MENU, False, zedit_save)
  ch.d.state = descriptor.descriptor_state.OLC
  zedit.zedit_display_main_menu(ch.d)

def do_zlist(ch, scmd, argument, server, mud, db):

  ch.write(f"ID{(1 + config.MAX_ZONE_ID_LENGTH)*' '}Zone Name{(config.MAX_ZONE_NAME_LENGTH - 8)*' '}Author\r\n")

  ch.write(f"{(2 + config.MAX_ZONE_ID_LENGTH)*'-'} {config.MAX_ZONE_NAME_LENGTH*'-'} {config.MAX_PLAYER_NAME_LENGTH*'-'}\r\n")

  for zn in mud._zones.values():
    ch.write(f"[{GREEN}{zn.id:>{config.MAX_ZONE_ID_LENGTH}}{NORMAL}] {CYAN}{zn.name:<{config.MAX_ZONE_NAME_LENGTH}}{NORMAL} {YELLOW}{zn.author.capitalize():<{config.MAX_PLAYER_NAME_LENGTH}}{NORMAL}\r\n")

  ch.write(f"\r\nThere are a total of {len(mud._zones)} zones loaded into memory.\r\n")
