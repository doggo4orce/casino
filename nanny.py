# python modules
import logging
import telnet

# local modules
import cmd_trig_data
import commands
import config
import editor
import exit_data
import descriptor_data
import mudlog
import npc_data
import olc
import olc_data
import pc_data
import room_data
import spec_proc_data
import unique_id_data

cmd_dict = dict()

def init_commands():
  cmd_dict["north"]     = ( commands.do_move,        exit_data.direction.NORTH  )
  cmd_dict["east"]      = ( commands.do_move,        exit_data.direction.EAST   )
  cmd_dict["south"]     = ( commands.do_move,        exit_data.direction.SOUTH  )
  cmd_dict["west"]      = ( commands.do_move,        exit_data.direction.WEST   )
  cmd_dict["up"]        = ( commands.do_move,        exit_data.direction.UP     )
  cmd_dict["down"]      = ( commands.do_move,        exit_data.direction.DOWN   )

  cmd_dict["colors"]    = ( commands.do_colors,      0 )
  cmd_dict["copyover"]  = ( commands.do_copyover,    0 )
  cmd_dict["client"]    = ( commands.do_client,      0 )
  # cmd_dict["db"]        = ( commands.do_db,          0 )
  cmd_dict["drop"]      = ( commands.do_drop,        0 )
  cmd_dict["goto"]      = ( commands.do_goto,        0 )
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
  cmd_dict["score"]     = ( commands.do_score,       0 )
  cmd_dict["shutdown"]  = ( commands.do_shutdown,    0 )
  cmd_dict["title"]     = ( commands.do_title,       0 )
  cmd_dict["quit"]      = ( commands.do_quit,        0 )
  cmd_dict["who"]       = ( commands.do_who,         0 )

  # OLC commands (separated purely for organization)
  cmd_dict["mlist"]     = ( olc.do_mlist,            0 )
  cmd_dict["olist"]     = ( olc.do_olist,            0 )
  cmd_dict["redit"]     = ( olc.do_redit,            0 )
  cmd_dict["rlist"]     = ( olc.do_rlist,            0 )
  cmd_dict["zedit"]     = ( olc.do_zedit,            0 )
  cmd_dict["zlist"]     = ( olc.do_zlist,            0 )

def look_up_command(command):
  for cmd_key in cmd_dict:
    if cmd_key.startswith(command):
      return cmd_key
  return None

def interpret_msg(d, command, argument, server, mud, db):
  valid_command = False
  initial_room = d.character.room

  # they might just be hitting enter to see an updated prompt
  if command == "":
    d.has_prompt = False
    return

  # fire all prefix procs
  for mob in mud.room_by_uid(d.character.room).people:
    if isinstance(mob, npc_data.npc_data):
      if cmd_trig_data.prefix_cmd_trig_messages.BLOCK_INTERPRETER == mob.call_prefix_cmd_trigs(mud, d.character, command, argument, db):
        return

  for obj in mud.room_by_uid(d.character.room).contents:
    if cmd_trig_data.prefix_cmd_trig_messages.BLOCK_INTERPRETER == obj.call_prefix_cmd_trigs(mud, d.character, command, argument, db):
      return

  cmd_key = look_up_command(command)

  if cmd_key != None:
    cmd_value = cmd_dict[cmd_key]
    cmd_value[0](d.character, cmd_value[1], argument, server, mud, db)
    d.has_prompt = False
    valid_command = True

  # fire all suffix procs
  for mob in mud.room_by_uid(initial_room).people:
    if isinstance(mob, npc_data.npc_data):
      mob.call_suffix_cmd_trigs(mud, d.character, command, argument, db)

  if not valid_command:
    d.write("Huh!?!\r\n")
    d.has_prompt = False

# what should they see when they finish writing? menu? etc.
def writing_follow_up(d):
  if d.state == descriptor_data.descriptor_state.OLC:
    olc.olc_writing_follow_up(d)
  # other possibilities:
  #   reporting_bug, mailing letter, scribing scroll, etc.

def handle_next_input(d, server, mud, db):
  msg = d.input_stream.pop_input()

  if d.character:
    mudlog.debug(f"nanny.handle_next_input called on player {d.character.name} with input {msg}")
  else:
    mudlog.debug(f"nanny.handle_next_input called by descriptor from {d.client.term_host} with input {msg}")

  if msg is None:
    return

  d.has_prompt = False
  stripped_msg = msg.strip()
  command, argument = (stripped_msg.split(" ", 1) + ["", ""])[:2]
  if d.writing:
    done_writing = editor.editor_handle_input(d, msg)
    if done_writing:
      writing_follow_up(d)
  elif d.state == descriptor_data.descriptor_state.CHATTING:
    interpret_msg(d, command, argument, server, mud, db)
  elif d.state == descriptor_data.descriptor_state.OLC:
    olc.handle_input(d, stripped_msg, server, mud, db)
  elif d.state == descriptor_data.descriptor_state.GET_NAME:
    if command == "":
      d.disconnected = True
      return
    if len(command) < 2 or argument != "":
      d.write("Invalid name, please try another.\r\nName: ")
      return
    command = command.lower()
    d.login_info.name = command
    if db.name_used(command):
      mudlog.info(f"{command.capitalize()} is logging in.")
      d.state = descriptor_data.descriptor_state.GET_PASSWORD
      d.send(bytes(telnet.will_echo))
      d.write("Password: ")
    else:
      d.state = descriptor_data.descriptor_state.CONFIRM_NAME
      d.write(f"Did I get that right, {d.login_info.name} (Y/N)? ")
  elif d.state == descriptor_data.descriptor_state.CONFIRM_NAME:
    if command == "":
      d.disconnected = True
    elif command[0] in ['y', 'Y']:
      d.state = descriptor_data.descriptor_state.GET_NEW_PASS
      d.send(bytes(telnet.will_echo))
      d.write(f"Give me a password for {d.login_info.name}: ")
    elif command[0] in ['n', 'N']:
      d.state = descriptor_data.descriptor_state.GET_NAME
      d.write("Okay, what IS it, then? ")
    else:
      d.write("Please type Yes or No: ")
  elif d.state == descriptor_data.descriptor_state.GET_NEW_PASS:
    # use msg instead of command so as to allow for spaces in passwords
    if len(msg) not in range(config.MIN_PASSWORD_LENGTH, config.MAX_PASSWORD_LENGTH - 1) or not msg.isprintable():
      d.write("Illegal password.\r\nPassword: ")
    else:
      d.login_info.password = msg
      d.state = descriptor_data.descriptor_state.CONFIRM_PASS
      d.write("\r\nPlease retype password: ")
  elif d.state == descriptor_data.descriptor_state.CONFIRM_PASS:
    if msg == d.login_info.password:
      new_player = pc_data.pc_data()
      new_player.name = d.login_info.name
      new_player.password = d.login_info.password
      new_player.descriptor = d
      new_player.room = unique_id_data.unique_id_data.from_string(config.STARTING_ROOM)
      new_player.player_id = db.next_unused_pid()
      db.save_player(new_player)

      d.character = new_player
      d.state = descriptor_data.descriptor_state.CHATTING
      mud.add_character_to_room(d.character, mud.room_by_uid(d.character.room))
      mudlog.info(f"{d.login_info.name} [{d.client.term_host}] new player.")
      d.send(bytes(telnet.wont_echo) + bytes([ord('\r'),ord('\n')]))
      d.write("Welcome!  Have a great time!\r\n")
      mudlog.info(f"{d.login_info.name} has entered the game.")
    else:
      d.state = descriptor_data.descriptor_state.GET_NEW_PASS
      d.write("\r\nPasswords don't match... start over.\r\nPassword: ")
  elif d.state == descriptor_data.descriptor_state.GET_PASSWORD:
    # and here too for the same reason as above
    if not db.check_password(d.login_info.name, msg):
      d.write("\r\nWrong password.\r\nPassword: ")
    else:
      # turn localecho back on
      d.send(bytes(telnet.wont_echo) + bytes([ord('\r'),ord('\n')]))

      # check if they are logged in already
      ch = mud.pc_by_id(db.player_id_by_name(d.login_info.name))

      # nothing found, log in normally
      if ch == None:
        new_player = pc_data.pc_data()

        # player now knows their own name
        new_player.name = d.login_info.name

        player_id = db.player_id_by_name(d.login_info.name)

        if player_id is None:
          mudlog.error(f"Error: Trying to load player {d.login_info.name} which is not contained in the database.")
          d.disconnected = True
          return

        # set up some default data in case load fails
        new_player.room = unique_id_data.unique_id_data.from_string(config.STARTING_ROOM)
        new_player.title = config.DEFAULT_TITLE

        # load the player from the database
        db.load_player(new_player, player_id)

        d.character = new_player
        d.character.descriptor = d
        d.write("Welcome!  Have a great time!\r\n")
        d.state = descriptor_data.descriptor_state.CHATTING
        mudlog.info(f"{d.login_info.name} has entered the game.")

        # if their room has been deleted, put them in the void
        if mud.room_by_uid(d.character.room) == None:
          d.character.room = structs.unique_identifier.from_string(config.VOID_ROOM)

        mud.add_character_to_room(d.character, mud.room_by_uid(d.character.room))
        mud.echo_around(d.character, None, f"{d.login_info.name} has entered the game.\r\n")

      elif ch.descriptor:
        d.write("You are already logged in.\r\nThrow yourself off (Y/N)? ")
        d.state = descriptor_data.descriptor_state.GET_CONFIRM_REPLACE
      else:
        mud.reconnect(d, ch)
        mudlog.info(f"{ch} recovering lost connection.")
        mud.echo_around(ch, None, f"{ch} has reconnected.\r\n")
        ch.write("You have reconnected.\r\n")
      d.state = descriptor_data.descriptor_state.CHATTING

  elif d.state == descriptor_data.descriptor_state.GET_CONFIRM_REPLACE:
    if command != "" and command[0] in ['Y', 'y']:
      ch = mud.pc_by_id(db.player_id_by_name(d.login_info.name))
      if not ch:
        d.write("The situation has changed.  Please log in again from scratch.\r\n")
        d.disconnected = True
      else:
        ch.d.write("Your connection is being usurped!\r\n")
        mud.reconnect(d, ch)
        mudlog.info(f"{ch} usurping existing connection.")
        mud.echo_around(ch, None, f"{ch} suddenly keels over in pain, surrounded by a white aura...\r\n")
        mud.echo_around(ch, None, f"{ch}'s body has been taken over by a new spirit!\r\n")
        d.write("You take over your own body -- already in use!\r\n")
        d.state = descriptor_data.descriptor_state.CHATTING
