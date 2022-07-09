import commands
import config
import descriptor
import logging
import pbase
import pc
import room
import telnet

cmd_dict = dict()

def init_commands():
  cmd_dict["north"]     = ( commands.do_move,        room.direction.NORTH  )
  cmd_dict["east"]      = ( commands.do_move,        room.direction.EAST   )
  cmd_dict["south"]     = ( commands.do_move,        room.direction.SOUTH  )
  cmd_dict["west"]      = ( commands.do_move,        room.direction.WEST   )
  cmd_dict["up"]        = ( commands.do_move,        room.direction.UP     )
  cmd_dict["down"]      = ( commands.do_move,        room.direction.DOWN   )

  cmd_dict["copyover"]  = ( commands.do_copyover,    0 )
  cmd_dict["client"]    = ( commands.do_client,      0 )
  cmd_dict["drop"]      = ( commands.do_drop,        0 )
  cmd_dict["help"]      = ( commands.do_help,        0 )
  cmd_dict["inventory"] = ( commands.do_inventory,   0 )
  cmd_dict["get"]       = ( commands.do_get,         0 )
  cmd_dict["give"]      = ( commands.do_give,        0 )
  cmd_dict["gossip"]    = ( commands.do_gossip,      0 )
  cmd_dict["look"]      = ( commands.do_look,        0 )
  # cmd_dict["pindex"]    = ( commands.do_pindex,      0 )
  cmd_dict["prefs"]     = ( commands.do_prefs,       0 )
  cmd_dict["save"]      = ( commands.do_save,        0 )
  cmd_dict["say"]       = ( commands.do_say,         0 )
  cmd_dict["score"]     = ( commands.do_client,      0 )
  cmd_dict["shutdown"]  = ( commands.do_shutdown,    0 )
  cmd_dict["title"]     = ( commands.do_title,       0 )
  cmd_dict["quit"]      = ( commands.do_quit,        0 )
  cmd_dict["who"]       = ( commands.do_who,         0 )

def interpret_msg(d, command, argument, server, mud):
  if command == "":
    d.has_prompt = False
    return

  block_interpreter = False

  for mob in mud.wld[d.char.room].people:
    if isinstance(mob, pc.npc):
      block_interpreter = mob.call_command_triggers(mud, d.char, command, argument)

  if block_interpreter:
    return

  for c in cmd_dict:
    if c.startswith(command):
      cmd_dict[c][0](d.char, cmd_dict[c][1], argument, server, mud)
      d.has_prompt = False
      return

  d.write("Huh!?!\r\n")
  d.has_prompt = False

def handle_next_input(d, server, mud):
  input = d.next_input()
  if not input:
    return
  d.has_prompt = False
  msg = input.data
  stripped_msg = msg.strip()
  command, argument = (stripped_msg.split(" ", 1) + ["", ""])[:2]
  if d.state == descriptor.descriptor_state.CHATTING:
    interpret_msg(d, command, argument, server, mud)
  elif d.state == descriptor.descriptor_state.GET_NAME:
    if command == "":
      d.disconnected = True
      return
    if len(command) < 2 or argument != "":
      d.write("Invalid name, please try another.\r\nName: ")
      return
    command = command.lower()
    d.login_info = d.login_info._replace(name = command.capitalize())
    id = pbase.id_by_name(command)
    if id != None:
      d.state = descriptor.descriptor_state.GET_PASSWORD
      d.send(bytes(telnet.will_echo))
      d.write("Password: ")
    else:
      d.state = descriptor.descriptor_state.CONFIRM_NAME
      d.write(f"Did I get that right, {d.login_info.name} (Y/N)? ")
  elif d.state == descriptor.descriptor_state.CONFIRM_NAME:
    if command == "":
      d.disconnected = True
    elif command[0] in ['y', 'Y']:
      d.state = descriptor.descriptor_state.GET_NEW_PASS
      d.send(bytes(telnet.will_echo))
      d.write(f"Give me a password for {d.login_info.name}: ")
    elif command[0] in ['n', 'N']:
      d.state = descriptor.descriptor_state.GET_NAME
      d.write("Okay, what IS it, then? ")
    else:
      d.write("Please type Yes or No: ")
  elif d.state == descriptor.descriptor_state.GET_NEW_PASS:
    # use msg instead of command so as to allow for spaces in passwords
    if len(msg) not in range(config.MIN_PASSWORD_LENGTH, config.MAX_PASSWORD_LENGTH - 1) or not msg.isprintable():
      d.write("Illegal password.\r\nPassword: ")
    else:
      d.login_info = d.login_info._replace(password = msg)
      d.state = descriptor.descriptor_state.CONFIRM_PASS
      d.write("\r\nPlease retype password: ")
  elif d.state == descriptor.descriptor_state.CONFIRM_PASS:
    if msg == d.login_info.password:
      pbase.add_player_to_index(d.login_info.name)
      pbase.update_index_file()
      new_char = pc.pc()
      new_char.name = d.login_info.name
      new_char.pwd = d.login_info.password
      new_char.d = d
      new_char.room = config.STARTING_ROOM
      new_char.id = pbase.id_by_name(new_char.name)
      new_char.save_char()
      d.char = new_char
      d.state = descriptor.descriptor_state.CHATTING
      mud.add_char(d.char)
      logging.info(f"{d.login_info.name} [{d.client_info.host_name}] new player.")
      d.send(bytes(telnet.wont_echo) + bytes([ord('\r'),ord('\n')]))
      d.write("Welcome!  Have a great time!\r\n")
      logging.info(f"{d.login_info.name} has entered the game.")
    else:
      d.state = descriptor.descriptor_state.GET_NEW_PASS
      d.write("\r\nPasswords don't match... start over.\r\nPassword: ")
  elif d.state == descriptor.descriptor_state.GET_PASSWORD:
    # and here too for the same reason as above
    if not pbase.verify_password(d.login_info.name, msg):
      d.write("\r\nWrong password.\r\nPassword: ")
    else:
      # turn localecho back on
      d.send(bytes(telnet.wont_echo) + bytes([ord('\r'),ord('\n')]))
      # check if they are logged in already
      ch = mud.pc_by_id(pbase.id_by_name(d.login_info.name))
      # nothing found, log in normally
      if not ch:
        d.char = pbase.load_char_by_name(d.login_info.name)
        d.char.d = d
        d.write("Welcome!  Have a great time!\r\n")
        d.state = descriptor.descriptor_state.CHATTING
        logging.info(f"{d.login_info.name} has entered the game.")
        mud.add_char(d.char)
        mud.echo_around(d.char, None, f"{d.login_info.name} has entered the game.\r\n")
      else:
        if ch.d:
          d.write("You are already logged in.\r\nThrow yourself off (Y/N)? ")
          d.state = descriptor.descriptor_state.GET_CONFIRM_REPLACE
        else:
          mud.reconnect(d, ch)
          logging.info(f"{ch} recovering lost connection.")
          mud.echo_around(ch, None, f"{ch} has reconnected.\r\n")
          ch.write("You have reconnected.\r\n")
          d.state = descriptor.descriptor_state.CHATTING
        return
  elif d.state == descriptor.descriptor_state.GET_CONFIRM_REPLACE:
    if command != "" and command[0] in ['Y', 'y']:
      ch = mud.pc_by_id(pbase.id_by_name(d.login_info.name))
      if not ch:
        d.write("The situation has changed.  Please log in again from scratch.\r\n")
        d.disconnected = True
      else:
        ch.d.write("Your connection is being usurped!\r\n")
        mud.reconnect(d, ch)
        logging.info(f"{ch} usurping existing connection.")
        mud.echo_around(ch, None, f"{ch} suddenly keels over in pain, surrounded by a white aura...\r\n")
        mud.echo_around(ch, None, f"{ch}'s body has been taken over by a new spirit!\r\n")
        d.write("You take over your own body -- already in use!\r\n")
        d.state = descriptor.descriptor_state.CHATTING
