import config
import descriptor_data
import game_data
import mudlog
import pc_data
import telnet
import unique_id_data

def input_handler_generic(d, mud, server, db, command, argument, input):

  # route to case-specific handler if character is in login process
  match d.state:
    case descriptor_data.descriptor_state.GET_NAME:
      input_handler_parse_get_name(d, mud, db, command, argument)
    case descriptor_data.descriptor_state.CONFIRM_NAME:
      input_handler_parse_confirm_name(d, command)
    case descriptor_data.descriptor_state.GET_PASSWORD:
      input_handler_parse_get_password(d, mud, db, input)
    case descriptor_data.descriptor_state.GET_NEW_PASS:
      input_handler_parse_get_new_pass(d, input)
    case descriptor_data.descriptor_state.CONFIRM_PASS:
      input_handler_parse_confirm_pass(d, mud, db, input)
    case descriptor_data.descriptor_state.GET_CONFIRM_REPLACE:
      input_handler_parse_confirm_replace(d, mud, command)

def input_handler_parse_get_name(d, mud, db, command, argument):
  # drop anyone who gives a carriage return instead of a name
  if command == "":
    d.disconnected = True
    return

  # don't allow names with less than 2 characters, or spaces in name
  if len(command) < 2 or argument != "":
    d.write("Invalid name, please try another.\r\nName: ")
    return

  # we don't care about capitalization
  command = command.lower()

  # keep track of their login name
  d.login_info.name = command

  # the database is unavailable, don't load anything just let them in
  if mud.mini_mode:

    # check if they are logged in already
    ch = mud.pc_by_name(d.login_info.name)

    # they are logged in with live connection
    if ch and ch.descriptor:
      d.write("You are already logged in.\r\nThrow yourself off (Y/N)? ")
      d.state = descriptor_data.descriptor_state.GET_CONFIRM_REPLACE
      return

    # they are logged in with a dead connection
    elif ch:
      mud.reconnect(d, ch)
      mudlog.info(f"{ch} recovering lost connection.")
      mud.echo_around(ch, None, f"{ch} has reconnected.\r\n")
      ch.write("You have reconnected.\r\n")
      d.state = descriptor_data.descriptor_state.CHATTING
      return

    # they aren't reconnecting, so log in normally
    new_player = pc_data.pc_data()
    new_player.name = d.login_info.name

    # hook them up to the descriptor
    new_player.descriptor = d
    d.character = new_player

    # put them in the emergency room
    emergency_room = unique_id_data.unique_id_data.from_string(config.VOID_ROOM)
    load_room = mud.room_by_uid(emergency_room)
    
    mud.add_character_to_room(d.character, mud.room_by_uid(load_room))

    # let the user know we are an emergency mode
    d.write("\r\nThe database was not loaded correctly.\r\n")

    # send them in to normal gameplay
    d.state = descriptor_data.descriptor_state.CHATTING
    mudlog.info(f"{d.login_info.name} [{d.client.term_host}] has logged in.")
    return

  # check if new player
  if not db.name_used(command):
    d.write(f"Did I get that right, {d.login_info.name} (Y/N)? ")
    d.state = descriptor_data.descriptor_state.CONFIRM_NAME
    return

  # turn off local echo and check their password
  d.send(bytes(telnet.will_echo))
  d.state = descriptor_data.descriptor_state.GET_PASSWORD
  d.write("Password: ")
  mudlog.info(f"{command.capitalize()} is logging in.")

def input_handler_parse_confirm_name(d, command):
  if command[0] in ['y', 'Y']:
    d.state = descriptor_data.descriptor_state.GET_NEW_PASS
    d.send(bytes(telnet.will_echo))
    d.write(f"Give me a password for {d.login_info.name}: ")
  elif command[0] in ['n', 'N']:
    d.state = descriptor_data.descriptor_state.GET_NAME
    d.write("Okay, what IS it, then? ")
  else:
    d.write("Please type Yes or No: ")

def input_handler_parse_get_password(d, mud, db, input):
  # if they enter nothing at all, kick them out
  if input == "":
    d.disconnected = True
    return

  # if they entered the wrong password, leave them in same state
  if not db.check_password(d.login_info.name, input):
    d.write("\r\nWrong password.\r\nPassword: ")
    return

  # otherwise, password was correct, turn localecho back on
  d.send(bytes(telnet.wont_echo) + bytes([ord('\r'),ord('\n')]))

  # check if they are logged in already
  ch = mud.pc_by_name(d.login_info.name)

  # they are logged in with live connection
  if ch and ch.descriptor:
    d.write("You are already logged in.\r\nThrow yourself off (Y/N)? ")
    d.state = descriptor_data.descriptor_state.GET_CONFIRM_REPLACE
    return

  # they are logged in with a dead connection
  elif ch:
    mud.reconnect(d, ch)
    mudlog.info(f"{ch} recovering lost connection.")
    mud.echo_around(ch, None, f"{ch} has reconnected.\r\n")
    ch.write("You have reconnected.\r\n")
    d.state = descriptor_data.descriptor_state.CHATTING
    return

  # they are not logged in already
  new_player = pc_data.pc_data()

  new_player.name = d.login_info.name

  player_id = db.player_id_by_name(d.login_info.name)

  if player_id is None:
    d.write("Something went wrong, sorry.\r\n")
    mudlog.error(f"Error: Trying to load player {d.login_info.name} which is not contained in the database.")
    d.disconnected = True
    return

  # set up some default data in case load partially fails
  new_player.room = unique_id_data.unique_id_data.from_string(config.STARTING_ROOM)
  new_player.title = config.DEFAULT_TITLE

  # load the player from the database
  db.load_player(new_player, player_id)

  # hook it up to the descriptor
  d.character = new_player
  d.character.descriptor = d

  # if their room has been deleted, put them in the void
  if mud.room_by_uid(d.character.room) == None:
    d.character.room = unique_id_data.unique_id.from_string(config.VOID_ROOM)

  # put them in the game
  mudlog.info(f"{d.login_info.name} has entered the game.")
  mud.add_character_to_room(d.character, mud.room_by_uid(d.character.room))
  mud.echo_around(d.character, None, f"{d.login_info.name} has entered the game.\r\n")

  # they're good to go
  d.write("Welcome!  Have a great time!\r\n")
  d.state = descriptor_data.descriptor_state.CHATTING

def input_handler_parse_get_new_pass(d, input):
  # refer to full user input, passwords may contain spaces
  if len(input) < config.MIN_PASSWORD_LENGTH:
  	d.write(f"Password must be at least {config.MIN_PASSWORD_LENGTH} characters.\r\nPassword: ")
  	return

  if len(input) > config.MAX_PASSWORD_LENGTH:
  	d.write(f"Password must be no longer than {config.MAX_PASSWORD_LENGTH} characters.\r\nPassword: ")
  	return

  if not input.isprintable():
    d.write("Illegal password.\r\nPassword: ")
    return
        
  d.login_info.password = input
  d.state = descriptor_data.descriptor_state.CONFIRM_PASS
  d.write("\r\nPlease retype password: ")

def input_handler_parse_confirm_pass(d, mud, db, input):

  if input != d.login_info.password:
    d.state = descriptor_data.descriptor_state.GET_NEW_PASS
    d.write("\r\nPasswords don't match... start over.\r\nPassword: ")
    return

  new_player = pc_data.pc_data()
  new_player.name = d.login_info.name
  new_player.password = d.login_info.password
  new_player.room = unique_id_data.unique_id_data.from_string(config.STARTING_ROOM)
  new_player.player_id = db.next_unused_pid()
  db.save_player(new_player)

  # hook them up to their descriptor
  new_player.descriptor = d
  d.character = new_player
        
  # put them in the game
  load_room = mud.room_by_uid(d.character.room)
  
  # if we can't find their starting room, put them in the void
  if load_room is None:
    load_room = mud.room_by_uid(unique_id_data.unique_id_data.from_string(config.VOID_ROOM))

  mud.add_character_to_room(d.character, load_room)

  mudlog.info(f"{d.login_info.name} [{d.client.term_host}] new player.")
  d.send(bytes(telnet.wont_echo) + bytes([ord('\r'),ord('\n')]))
  d.write("Welcome!  Have a great time!\r\n")
  d.state = descriptor_data.descriptor_state.CHATTING
  mudlog.info(f"{d.login_info.name} has entered the game.")

def input_handler_parse_confirm_replace(d):
  if first_arg != "" and first_arg[0] in ['Y', 'y']:
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
      