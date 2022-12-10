import baccarat
import descriptor
import exit
import logging
import math
import socket

from color import *
import config
import event
import nanny
import olc
import os
import pbase
import pc
import room
import string_handling
import structs
import zedit
import zone

def do_colors(ch, scmd, argument, server, mud):
  out_str = ""
  
  out_str += "For Reference, this is normal text.\r\n\r\n"

  out_str += "-----------------------------------\r\n"
  out_str += "Colours".ljust(21) + "Bright Colours\r\n"
  out_str += "-----------------------------------\r\n\r\n"

  out_str += f"{BLACK}Black{NORMAL}".ljust(30) + f"{BRIGHT_BLACK}Bright Black{NORMAL}\r\n"
  out_str += f"{RED}Red{NORMAL}".ljust(30) + f"{BRIGHT_RED}Bright Red{NORMAL}\r\n"
  out_str += f"{GREEN}Green{NORMAL}".ljust(30) + f"{BRIGHT_GREEN}Bright Green{NORMAL}\r\n"
  out_str += f"{YELLOW}Yellow{NORMAL}".ljust(30) + f"{BRIGHT_YELLOW}Bright Yellow{NORMAL}\r\n"
  out_str += f"{BLUE}Blue{NORMAL}".ljust(30) + f"{BRIGHT_BLUE}Bright Blue{NORMAL}\r\n"
  out_str += f"{MAGENTA}Magenta{NORMAL}".ljust(30) + f"{BRIGHT_MAGENTA}Bright Magenta{NORMAL}\r\n"
  out_str += f"{CYAN}Cyan{NORMAL}".ljust(30) + f"{BRIGHT_CYAN}Bright Cyan{NORMAL}\r\n"
  out_str += f"{WHITE}Dark White{NORMAL}".ljust(30) + f"{BRIGHT_WHITE}Bright White{NORMAL}\r\n\r\n"

  out_str += "------------------------------------\r\n"
  out_str += "Background Colours".ljust(21) + "Special Effects\r\n"
  out_str += "------------------------------------\r\n\r\n"

  out_str += f"{BKGD_BLACK}Background Black{NORMAL}".ljust(30) + f"{UNDERLINE}Underline{NORMAL}\r\n"
  out_str += f"{BKGD_RED}Background Red{NORMAL}".ljust(30) + f"{FLASH}Flashing{NORMAL}\r\n"
  out_str += f"{BKGD_GREEN}Background Green{NORMAL}\r\n"
  out_str += f"{BKGD_YELLOW}Background Yellow{NORMAL}\r\n"
  out_str += f"{BKGD_BLUE}Background Blue{NORMAL}\r\n"
  out_str += f"{BKGD_MAGENTA}Background Magenta{NORMAL}\r\n"
  out_str += f"{BKGD_CYAN}Background Cyan{NORMAL}\r\n"
  out_str += f"{BKGD_WHITE}Background White{NORMAL}\r\n\r\n"

  ch.write(out_str)

def do_give(ch, scmd, argument, server, mud):
  args = argument.split()
  num_args = len(args)

  if num_args == 0:
    ch.write("Give what to whom?\r\n")
    return

  elif num_args != 2:
    ch.write("Usage: give <item> <recipient>\r\n")
    return

  # what to give
  obj = ch.inventory.obj_by_alias(args[0])

  if obj == None:
    ch.write(f"You don't seem to have {string_handling.ana(args[0])} {args[0]}.\r\n")
    return

  # who to give it to
  rm = mud.room_by_code(ch.room)
  tch = rm.char_by_alias(args[1])

  if tch == None:
    ch.write(f"There is nobody by the name {args[1]} here.\r\n")
    return

  # transfer the object
  ch.inventory.remove(obj)
  tch.inventory.insert(obj)

  # let everyone know
  ch.write(f"You give {obj} to {tch}.\r\n")
  tch.write(f"{ch} gives you {obj}.\r\n")
  mud.echo_around(ch, [tch], f"{ch} gives {obj} to {tch}.\r\n")

  if type(tch) == pc.npc:
    def check_it_out(c, mu):
      mu.echo_around(c, None, f"{c} takes a closer look at {obj}.\r\n")
    def decide_no(c, mu):
      do_say(c, None, "I don't want this junk!", None, mu)
    def drop_it(c, mu):
      do_drop(c, None, args[0], None, mu)

    mud.add_event(event.event(tch, check_it_out, None, 10))
    mud.add_event(event.event(tch, decide_no, None, 20))
    mud.add_event(event.event(tch, drop_it, None, 30))


def do_get(ch, scmd, argument, server, mud):
  args = argument.split()
  num_args = len(args)

  if num_args == 0:
    ch.write("Get what?\r\n")
    return

  elif num_args != 1:
    ch.write("Usage: get <item>\r\n")
    return

  rm = mud.room_by_code(ch.room)
  obj = rm.inventory.obj_by_alias(args[0])

  if obj == None:
    ch.write(f"There is no {args[0]} here.\r\n")
    return

  rm.inventory.remove(obj)
  ch.inventory.insert(obj)

  ch.write(f"You get {obj}.\r\n")
  mud.echo_around(ch, None, f"{ch} gets {obj}.\r\n")

def do_goto(ch, scmd, argument, server, mud):
  here_id = ch.room.id
  here_zone_id = ch.room.zone_id
  here = mud.room_by_code(ch.room)

  there_zone_id, there_room_id = string_handling.parse_reference(argument)
  there = mud.room_by_code(structs.unique_identifier(there_zone_id, there_room_id))

  if there == None:
    ch.write("I'm sorry, but that room cannot be found.\r\n")
    return

  # remove them from the old room
  here.remove_char(ch)
  here.echo(f"{ch.name} disappears in a puff of smoke.\r\n")

  # add them to the new room
  there.echo(f"{ch.name} appears with an ear-splitting bang.\r\n")
  there.add_char(ch)

  # show them the new room
  show_room_to_char(ch, there)


def do_drop(ch, scmd, argument, server, mud):
  args = argument.split()
  num_args = len(args)
  rm = mud.room_by_code(ch.room)

  if num_args == 0:
    ch.write("Drop what?\r\n")
    return

  elif num_args != 1:
    ch.write("Usage: drop <item alias>\r\n")
    return

  obj = ch.inventory.obj_by_alias(args[0])

  if obj == None:
    ch.write(f"You don't have a {args[0]}.\r\n")
    return

  obj.room = ch.room
  rm.inventory.insert(obj)
  ch.inventory.remove(obj)
  ch.write(f"You drop {obj}.\r\n")
  mud.echo_around(ch, None, f"{ch} drops {obj}.\r\n")

def do_inventory(ch, scmd, argument, server, mud):
  if len(ch.inventory) == 0:
    ch.write("You aren't carrying anything.\r\n")
    return

  out_str = "You are carrying:\r\n"
  for obj in ch.inventory:
    out_str += f"  {obj}\r\n"

  ch.write(out_str)

def do_help(ch, scmd, argument, server, mud):
  cmds = list(nanny.cmd_dict.keys())
  num_cmds = len(cmds)

  # choices for spacing out the commands
  leading_spaces = 2
  min_space = 1

  # find out the longest command name to determine column width
  fmt_len = max([ len(cmd) for cmd in cmds ]) + min_space

  # pad each word with spaces
  cmds = [cmd.ljust(fmt_len) for cmd in cmds]

  # number of columns (subtract leading spaces but add the extra trailing space that isn't needed)
  n = (ch.prefs.screen_width - leading_spaces + min_space)//fmt_len


  # r is number of complete columns (unless it is zero then n is)
  r = num_cmds % n

  # number of rows (round up)
  m = math.ceil(float(num_cmds)/float(n))

  out_str = "Available Commands:\r\n"
  # build the table
  if r == 0:
    # each row follows the same rule
    for j in range(0, m):
      out_str += leading_spaces * ' '
      # count up by m for each column
      for k in range(0, n - 1):
        out_str += cmds[j + m*k]
      out_str = out_str[:-min_space] + '\r\n'
  else:
    # all but the last row follow the same rule
    for j in range(0, m - 1):
      out_str += leading_spaces * ' '
      # count by m for the first r + 1 columns
      for k in range(0, r):
        out_str += cmds[j + m*k]
      # then by m - 1 for the rest
      for k in range(0, n - r):
        out_str += cmds[j + m*r + (m - 1)*k]
      out_str = out_str[:-min_space] + '\r\n'
    # now build the last row
    out_str += leading_spaces * ' '
    for k in range(0, r + 1):
      out_str += cmds[(m - 1) + m*k]
    out_str = out_str[:-min_space] + '\r\n'

  ch.write(out_str)

def do_client(ch, scmd, argument, server, mud):
  have_info = False

  ci = ch.d.client_info

  out_str = "Connection Information:\r\n"
  
  if ci.term_type != None:
    out_str += f"  term_type      [{ORANGE}{ci.term_type.lower()}{NORMAL}]\r\n"
  if ci.term_width != None:
    out_str += f"  term_width     [{ORANGE}{ci.term_width}{NORMAL}]\r\n"
  if ci.term_length != None:
    out_str += f"  term_length    [{ORANGE}{ci.term_length}{NORMAL}]\r\n"
  if ci.host_name != None:
    out_str += f"  host_name      [{ORANGE}{ci.host_name}{NORMAL}]\r\n"

  ch.write(out_str)

def do_prefs(ch, scmd, argument, server, mud):
  prefs_help = "Customizable Preferences:\r\n"
  prefs_help += f"  screen_width   [{ORANGE}{ch.prefs.screen_width}{NORMAL}]\r\n"
  prefs_help += f"  screen_length  [{ORANGE}{ch.prefs.screen_length}{NORMAL}]\r\n"
  prefs_help += f"  color_mode     [{ORANGE}{ch.prefs.color_mode}{NORMAL}]\r\n"
  prefs_help += "\r\n"
  prefs_help += f"To change one of these options, use: prefs set <option> <value>\r\n"
  prefs_help += "\r\n"
  prefs_help += "Toggleable preferences:\r\n"
  prefs_help += f"  active_idle    [{ORANGE}{ch.prefs.active_idle}{NORMAL}]\r\n"
  prefs_help += f"  brief_mode     [{ORANGE}{ch.prefs.brief_mode}{NORMAL}]\r\n"
  prefs_help += f"  debug_mode     [{ORANGE}{ch.prefs.debug_mode}{NORMAL}]\r\n"
  prefs_help += "\r\n"
  prefs_help += f"To change one of these options, use: prefs toggle <option>\r\n"

  args = argument.split()
  num_args = len(args)
  if num_args == 0:
    ch.write(prefs_help)
    return
  if args[0] == 'set':
    if num_args != 3:
      ch.write("Usage: prefs set <option> <value>\r\n")
      return
    option = args[1]
    value = args[2]
    if option in ['screen_width', 'screen_length']:
      if not value.isdecimal():
        ch.write(f"{option} must take an integer value.\r\n")
        return
      ch.prefs.set(option, int(value))
    elif option == 'color_mode':
      accepted = ['off', '16', '256']
      if value not in accepted:
        ch.write(f"Acceptable values for {option} are {string_handling.oxford_comma(accepted)}.\r\n")
        return
      ch.prefs.set(option, value)
    else:
      ch.write(f"Option '{option}' cannot be set.\r\n")
      return
    ch.write(f"Setting {option} to {value}.\r\n")
  elif args[0] == 'toggle':
    if num_args != 2:
      ch.write("Usage: prefs toggle <option>\r\n")
      return
    option = args[1]
    if option in ['active_idle', 'brief_mode', 'debug_mode']:
      ch.prefs.flip(option, 'on', 'off')
      ch.write(f"Setting {option} to {getattr(ch.prefs, option)}.\r\n")
    else:
      ch.write(f"Option '{option}' cannot be toggled.\r\n")
      return
  else:
    ch.write(prefs_help)
    return

def do_pindex(ch, scmd, argument, server, mud):
  out_str = ''.join(f"{p['id']} {p['name']}\r\n" for p in pbase.ptable)
  ch.write(out_str)

def do_gossip(ch, scmd, argument, server, mud): 
  # TODO: change this function to write to all characters in the game so that we can work towards
  # not interacting with descriptors directly
  server.write_all(f"{YELLOW}{ch} gossips, '{argument}'{NORMAL}\r\n", exceptions=[ch.d])
  ch.write(f"{YELLOW}You gossip, '{argument}'{NORMAL}\r\n")

def do_say(ch, scmd, argument, server, mud):
  rm = mud.room_by_code(ch.room)
  rm.echo(f"{ch} says, '{argument}'\r\n", exceptions=[ch])
  ch.write(f"You say, '{argument}'\r\n")

def do_save(ch, scmd, argument, server, mud):
  ch.write(f"Saving {ch}.\r\n")
  ch.save_char()

def do_title(ch, scmd, argument, server, mud):
  ch.title = argument

  if argument:
    ch.write(f"You are now {ch} {ch.title}.\r\n")
  else:
    ch.write("You now have no title.\r\n")

def do_score(ch, scmd, argument, server, mud):  
  out_str  = f"Name:      {ch}\r\n"
  out_str += f"Client:    {ch.d.client_info.term_type}\r\n"
  out_str += f"Screen:    {ch.d.client_info.term_length}x{ch.d.client_info.term_width}\r\n"

  if ch.prefs.debug_mode == 'on':
    out_str += f"Room:      {ch.room}\r\n"
    
  ch.write(out_str)

def do_who(ch, scmd, argument, server, mud):
  d_dict = server.descriptors
  num_online = 0
  out_str =  "Players\r\n"
  out_str += f"-------\r\n{YELLOW}"

  for d in d_dict.values():
    if d.state == descriptor.descriptor_state.CHATTING:
      out_str += f"{d.char} {d.char.title}\r\n"
      num_online += 1

  if len(d_dict) > 1:
    out_str += f"\r\n{NORMAL}{num_online} connections displayed.\r\n"
  else:
    out_str += f"\r\n{NORMAL}1 lonely connection displayed.\r\n"

  ch.write(out_str)

def do_shutdown(ch, scmd, argument, server, mud):
  USAGE = "Usage: 'shutdown die' or 'shutdown reboot'\r\n"

  first_arg, remaining_args = (argument.split(" ", 1) + ["", ""])[:2]

  if first_arg == 'die':
    os.system("touch .killscript")
    server.write_all("Shutting down for maintenance.  Come back another time.\r\n")
  elif first_arg == 'pause':
    os.system("touch .pausescript")
    server.write_all("Rebooting.  Wait minute or two before returning.\r\n")
  elif first_arg == 'pause':
    server.write_all("Rebooting.  Come back in a few seconds.\r\n")
  else:
    ch.write(USAGE)
    return
  
  logging.info(f"Shutdown {first_arg} by {ch}.")
  server.shutdown_cmd = True

def do_copyover(ch, scmd, argument, server, mud):
  out_msg_others = f"\r\n{RED}Time stops for a moment as {ch} folds space and time.{NORMAL}\r\n"
  out_msg_self = f"\r\n{RED}Time stops for a moment as you fold space and time.{NORMAL}\r\n"

  server.write_all(out_msg_others, exceptions = [ch.d])
  ch.write(out_msg_self)

  with open(config.COPYOVER_PATH, "w") as wf:
    for id, td in server.descriptors.items():
      if td.state != descriptor.descriptor_state.CHATTING:
        td.write("Rebooting, come back in a few seconds.\r\n")
        continue

      td.char.save_char()

      fd = td.socket.fileno()
      name = td.char.name.lower()
      typ = td.socket.type
      host = td.client_info.host_name
      ttype = td.client_info.term_type
      twidth = td.client_info.term_width
      tlength = td.client_info.term_length

      wf.write(f"{fd} {name} {typ} {host} {ttype} {twidth} {tlength}\n")

  server.copyover_cmd = True

def do_look(ch, scmd, argument, server, mud):
  args = argument.split()
  num_args = len(args)

  rm = mud.room_by_code(ch.room)
  
  # if no args, then just look at the room
  if num_args == 0:
    if ch.room == None:
      ch.write("You are nowhere!\r\n")
      return
    show_room_to_char(ch, rm)
  elif num_args == 1:
    tch = rm.char_by_alias(args[0])

    if tch != None:
      show_char_to_char(ch, tch)
    else:
      ch.write(f"You see no {args[0]} here.\r\n")

def show_room_to_char(ch, rm):
  out_buf = f'{CYAN}{string_handling.paragraph(rm.name, ch.prefs.screen_width, False)}{NORMAL}\r\n'

  if ch.prefs.brief_mode == 'off':
    out_buf += f'{string_handling.paragraph(rm.desc, ch.prefs.screen_width, True)}\r\n'
  
  out_buf += f'{CYAN}{rm.show_exits()}{NORMAL}\r\n'

  for tch in rm.people:
    if tch != ch:
      out_buf += f"{YELLOW}{string_handling.paragraph(tch.ldesc, ch.prefs.screen_width, False)}{NORMAL}"
      if type(tch) == pc.pc and tch.d != None and tch.d.state == descriptor.descriptor_state.OLC:
        out_buf += " (olc)"
      out_buf += "\r\n"

  for obj in rm.inventory:
    out_buf += f"{GREEN}{string_handling.paragraph(obj.ldesc, ch.prefs.screen_width, False)}{NORMAL}\r\n"

  ch.write(out_buf)

def show_char_to_char(ch, tch):
  out_buf = f"{string_handling.paragraph(tch.entity.desc, ch.prefs.screen_width, False)}\r\n"
  out_buf += "\r\n"
  out_buf += "You attempt to peek at his inventory:\r\n"

  for obj in tch.inventory:
    out_buf += f"  {obj}\r\n"
  if len(tch.inventory) == 0:
    out_buf += "  Nothing.\r\n"

  if ch.prefs.debug_mode == 'on':
    out_buf += "\r\nDebug Info:\r\n"
    out_buf += f"Type: {type(tch)}\r\n"
    out_buf += "Prefix Procs:\r\n"

    for spec in tch.prefix_command_triggers:
      out_buf += f"  {spec.name}\r\n"
    
    out_buf += "Suffix Procs:\r\n"

    for spec in tch.suffix_command_triggers:
      out_buf += f"  {spec.name}\r\n"

    out_buf += "Hearbeat Procs:\r\n"

    for spec in tch.heart_beat_procs:
      out_buf += f"  {spec.name}\r\n"

    if type(tch) == baccarat.baccarat_dealer:
      out_buf += f"State: {baccarat.baccarat_dealer_state(tch.bac_state).name}\r\n"
      out_buf += f"Paused: {string_handling.yesno(tch.paused)}"

  ch.write(out_buf)

def do_move(ch, scmd, argument, server, mud):
  starting_room = mud.room_by_code(ch.room)
  dest_ref = starting_room.get_destination(scmd)

  if not dest_ref:
    ch.write("Alas, you cannot go that way.\r\n")
    return

  if dest_ref.isalnum():
    # check first to see if dest_ref is just a room_id (internal exit)
    dest_id = structs.unique_identifier(ch.room.zone_id, dest_ref)
  #elif: TODO: check for external exit that should be external and change it
  else:
    # in this case, the exit leads to a room in another zone (external exit)
    dest_id = structs.unique_identifier.from_string(dest_ref)

  print(f"{dest_id.zone_id} {dest_id.id}")

  ending_room = mud.room_by_code(dest_id)

  left_msg = f"{ch} leaves {scmd.name.lower()}.\r\n"

  arrived_messages = {
    exit.direction.NORTH: 'the south',
    exit.direction.EAST:  'the east',
    exit.direction.SOUTH: 'the north',
    exit.direction.WEST:  'the east',
    exit.direction.UP:    'below',
    exit.direction.DOWN:  'above',
  }

  arrived_msg = f"{ch} has arrived from {arrived_messages[scmd]}.\r\n"

  if ending_room == None:
    # uncomment to send them to the void, but for now just stop movement
    # ending_room = mud.room_by_code(structs.unique_identifier.from_string(config.VOID_ROOM))
    ch.write("Construction blocks your path.\r\n")
    return

  # remove them from the old room
  starting_room.remove_char(ch)
  starting_room.echo(left_msg)

  # add them to the new room
  ending_room.echo(arrived_msg)
  ending_room.add_char(ch)

  # show them the new room
  show_room_to_char(ch, ending_room)

def do_quit(ch, scmd, argument, server, mud):
  d = ch.d
  room = mud.room_by_code(ch.room)
  ch.save_char()
  mud.extract_char(ch)

  for tch in room.people:
     if tch != ch:
       tch.write(f"{ch} has left the game.\r\n")

  ch.write("Goodbye!\r\n")
  d.has_prompt = True
  server.just_leaving.append(d.id)

