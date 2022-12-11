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

def handle_input(d, input, server, mud):
  if d.olc.mode == olc_mode.OLC_MODE_ZEDIT:
  	zedit.zedit_parse(d, input, server, mud)
  elif d.olc.mode == olc_mode.OLC_MODE_REDIT:
    redit.redit_parse(d, input, server, mud)

def do_mlist(ch, scmd, argument, server, mud):
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

def do_olist(ch, scmd, argument, server, mud):
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

def do_rlist(ch, scmd, argument, server, mud):
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

  num_rooms = len(zone._world.items())

  if num_rooms == 0:
    ch.write("This zone has no rooms!\r\n")
    return

  ch.write(f"ID{(1 + config.MAX_ROOM_ID_LENGTH)*' '}Room Name{(config.MAX_ROOM_NAME_LENGTH - 8)*' '}Exit\r\n")
  ch.write(f"{(2 + config.MAX_ROOM_ID_LENGTH)*'-'} {config.MAX_ROOM_NAME_LENGTH*'-'} {(2 + config.MAX_ZONE_ID_LENGTH)*'-'}\r\n")

  for id, room in zone._world.items():
    ch.write(f"[{GREEN}{id:>{config.MAX_ROOM_ID_LENGTH}}{NORMAL}] {CYAN}{room.name:<30}{NORMAL}\r\n")

def do_redit(ch, scmd, argument, server, mud):
  USAGE = "Usage: redit [[zone_id ]room_id]"
  room = None

  zone_id = ch.room.zone_id
  room_id = ch.room.id

  args = argument.split()
  num_args = len(args)

  redit_save = structs.redit_save_data()

  # too many arguments, send usage and quit
  if num_args not in {0,1,2}:
    ch.write(USAGE)
    return

  # no room or zone id specified, edit the current room
  if num_args == 0:
    room = mud.room_by_code(ch.room)

    if room == None:
      ch.write("For some reason, we couldn't find the room you're currently in.\r\n")
      return

    redit_save.zone_id = zone_id
    redit_save.room_id = room_id

  # in this case they specified the room_id, but left zone_id blank
  elif num_args == 1:
    room_id = args[0]
    room = mud.room_by_code(structs.unique_identifier(zone_id, room_id))

    # if the room could not be found, send general error for now
    if room == None:
      # todo: figure out what went wrong, zone or room?
      ch.write(f"Error: could not find room {room_id} in zone {zone_id}.")
      return

    # attach it to current zone
    redit_save.zone_id = zone_id
    
  # room and zone id specified
  elif num_args == 2:
    zone_id, room_id = args[0], args[1]

    if mud.zone_by_id(zone_id) == None:
      ch.write("That zone doesn't exist.  You'll have to create it first!\r\n")
      return

    redit_save.zone_id = zone_id
    redit_save.room_id = room_id
    
    room = mud.room_by_code(structs.unique_identifier(zone_id, room_id))
 
  # by this point we either already returned, or redit_save has been initialized and
  # room == None if we're making a new room, otherwise it is the room we're editing.
  if room != None:
    redit_save.room_name = room.name
    redit_save.room_desc = room.desc

    redit_save.zone_id = zone_id
    redit_save.room_id = room_id
    redit_save.room_name = room.name
    redit_save.room_desc = room.desc

    # make a copy of all the exits as strings of either internal or external references
    for dir in exit.direction:
      redit_save.room_exits[dir] = room.get_destination(dir) # some of these will be None!

  mud.echo_around(ch, None, f"{ch.name} starts using OLC (redit).\r\n")
  ch.d.olc = structs.olc_data(olc_mode.OLC_MODE_REDIT, redit.redit_state.REDIT_MAIN_MENU, False, redit_save)
  ch.d.state = descriptor.descriptor_state.OLC
  redit.redit_display_main_menu(ch.d)

def do_zedit(ch, scmd, argument, server, mud):
  Usage1 = "Usage: zedit <zone_id> to edit an existing zone, or\r\n"
  Usage2 = "Usage: zedit new <zone_id> to create a new zone."
  args = argument.split()
  num_args = len(args)

  zedit_save = structs.zedit_save_data()

  if num_args == 0:
    zone_id = ch.room.zone_id
    zone = mud.zone_by_id(zone_id)
    zedit_save.zone_id = zone.id
    zedit_save.zone_name = zone.name
    zedit_save.zone_folder = zone.folder
    zedit_save.zone_author = zone.author
  elif num_args == 1:
    zone_id = args[0]
    zone = mud.zone_by_id(zone_id)

    # the only difference is if the zone isn't found, it keeps more default values
    if zone != None:
      zedit_save.zone_id = zone_id
      zedit_save.zone_name = zone.name
      zedit_save.zone_author = zone.author
      zedit_save.zone_folder = zone.folder
    
  elif num_args == 2:
    # zedit new new_zone?
    if args[0] != 'new':
      ch.write(Usage1)
      ch.write(Usage2)
      return
    # otherwise its zedit new <zone_id>
    zone_id = args[1]

    zone = mud.zone_by_id(zone_id)

    if zone != None:
      ch.write("That zone already exists, edit it instead!\r\n")
      return

    zedit_save.zone_id = args[1]
    
  else:
    ch.write(Usage1)
    ch.write(Usage2)
    return

  mud.echo_around(ch, None, f"{ch.name} starts using OLC (zedit).\r\n")
  ch.d.olc = structs.olc_data()
  ch.d.olc = structs.olc_data(olc_mode.OLC_MODE_ZEDIT, zedit.zedit_state.ZEDIT_MAIN_MENU, False, zedit_save)
  ch.d.state = descriptor.descriptor_state.OLC
  zedit.zedit_display_main_menu(ch.d)

def do_zlist(ch, scmd, argument, server, mud):

  ch.write(f"ID{(1 + config.MAX_ZONE_ID_LENGTH)*' '}Zone Name{(config.MAX_ZONE_NAME_LENGTH - 8)*' '}Author\r\n")

  ch.write(f"{(2 + config.MAX_ZONE_ID_LENGTH)*'-'} {config.MAX_ZONE_NAME_LENGTH*'-'} {config.MAX_PLAYER_NAME_LENGTH*'-'}\r\n")

  for zn in mud._zones.values():
    ch.write(f"[{GREEN}{zn.id:>{config.MAX_ZONE_ID_LENGTH}}{NORMAL}] {CYAN}{zn.name:<{config.MAX_ZONE_NAME_LENGTH}}{NORMAL} {YELLOW}{zn.author.capitalize():<{config.MAX_PLAYER_NAME_LENGTH}}{NORMAL}\r\n")

  ch.write(f"\r\nThere are a total of {len(mud._zones)} zones loaded into memory.\r\n")
