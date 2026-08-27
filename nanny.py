import config
import pc_data

def nanny(d, mud, server, db, first_arg, input):
  match d.state:
    case descriptor_data.descriptor_state.GET_NAME:
      nanny_parse_get_name(d, mud, db, first_arg)
    case descriptor_data.descriptor_state.CONFIRM_NAME:
      nanny_parse_confirm_name(d, first_arg)
    case descriptor_data.descriptor_state.GET_NEW_PASS:
      nanny_parse_get_new_pass(d, input)
    case descriptor_data.descriptor_state.CONFIRM_PASS:
      nanny_parse_confirm_pass(d, mud, db, input)
    match descriptor_data.descriptor_state.GET_CONFIRM_REPLACE:
      nanny_parse_confirm_replace(d, mud, first_arg)
      
def nanny_parse_get_name(d, mud, db, first_arg)
  # drop anyone who gives a carriage return instead of a name
  if first_arg == "":
    d.disconnected = True
    return

    # don't allow names with less than 2 characters, or spaces in name
    if len(first_arg) < 2 or argument != "":
      d.write("Invalid name, please try another.\r\nName: ")
      return

    # we don't care about capitalization
    first_arg = first_arg.lower()

    # keep track of their login name
    d.login_info.name = first_arg

    # the database is unavailable, don't load anything just let them in
    if mud.mini_mode:

      # create a player with the login name
      new_player = pc_data.pc_data()
      new_player.name = d.login_info.name

      # hook them up to a descriptor
      new_player.descriptor = d
      d.character = new_player

      # put them in the emergency room
      emergency_room = unique_id_data.unique_id_data.from_string(config.STARTING_ROOM)
      load_room = mud.room_by_uid(emergency_room)
      mud.add_character_to_room(d.character, mud.room_by_uid(load_room))

      # let the user know we are an emergency mode
      d.write("\r\nThe database was not loaded correctly.\r\n")

      # send them in to normal gameplay
      d.state = descriptor_data.descriptor_state.CHATTING
      mudlog.info(f"{d.login_info.name} [{d.client.term_host}] has logged in.")
      return

    # check if new player
    if not db.named_used(first_arg):
      d.write(f"Did I get that right, {d.login_info.name} (Y/N)? ")
      d.state = descriptor_data.descriptor_state.CONFIRM_NAME
      return

    # turn off local echo and check their password
    d.send(bytes(telnet.will_echo))
    d.state = descriptor_data.descriptor_state.GET_PASSWORD
    d.write("Password: ")
    mudlog.info(f"{first_arg.capitalize()} is logging in.")

def nanny_parse_confirm_name(d, first_arg):
  if first_arg[0] in ['y', 'Y']:
    d.state = descriptor_data.descriptor_state.GET_NEW_PASS
    d.send(bytes(telnet.will_echo))
    d.write(f"Give me a password for {d.login_info.name}: ")
  elif input[0] in ['n', 'N']:
    d.state = descriptor_data.descriptor_state.GET_NAME
    d.write("Okay, what IS it, then? ")
  else:
    d.write("Please type Yes or No: ")

def nanny_parse_get_new_pass(d, input):
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

def nanny_parse_confirm_pass(d, mud, db, input):

  if msg != d.d.login_info.password:
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

def nanny_parse_confirm_replace(d):
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
      