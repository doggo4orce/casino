from color import *
import command_data
import commands
import config
import descriptor_data
import mudlog
import olc
import pc_data
import unique_id_data

class command_interpreter:
  """Creates a command interpreter object to parse input from players
     and handle the game's response.
     commands = a list of commands which have been loaded"""
  def __init__(self, game):
    self.commands = list()

  """enable(command, function, subcmd)                    <- add new command to list
     disable(command)                                     <- remove command from list
     hand_input(d, server, mud, db)                       <- universal input handler
     interpret_msg(d, command, argument, server, mud, db) <- normal in-game command interpreter
     load_commands()                                      <- load all commands into the game
     writing_follow_up(d)                                 <- save edit buffer appropriately"""

  def enable(self, command, function, subcmd):
    self.commands.append(command_data.command_data(command, function, subcmd))

  def disable(self, command):
    for cmd_object in self.commands:
      if cmd_object.command == commmand:
        self.commands.pop(cmd_object)

  # Server object passed because the mud doesn't know about it, and some administrative
  # commands might like to inspect the server (e.g. to look up states of all descriptors)
  def handle_input(d, server, mud, db):
    msg = d.input_stream.pop_input()

    if msg is None:
      return

    if d.character:
      mudlog.debug(f"handle_next_input called on player {d.character.name} with input '{msg}'")
    else:
      mudlog.debug(f"handle_next_input called by descriptor from {d.client.term_host} with input '{msg}'")

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

      try:
        name_used = db.name_used(command)
      except:
        d.write("Failed to lookup name in database -- assuming new character.\r\n")
        name_used = False

      if name_used:
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
        d.character = new_player
        new_player.room = unique_id_data.unique_id_data.from_string(config.STARTING_ROOM)
  
        try:
          new_player.player_id = db.next_unused_pid()
        except:
          d.write("Failed to lookup next unused player_id -- assigning 0.\r\n")
          new_player.player_id = 0
        else:
          db.save_player(new_player)
  
        d.state = descriptor_data.descriptor_state.CHATTING
        load_room = mud.room_by_uid(d.character.room)
  
        if load_room is None:
          mud.add_character_to_room(d.character, mud.room_by_uid(unique_id_data.unique_id_data.from_string(config.VOID_ROOM)))
        else:
          mud.add_character_to_room(d.character, mud.room_by_uid(load_room))

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
            d.character.room = unique_id_data.unique_id.from_string(config.VOID_ROOM)

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

  def load_commands():
    self.enable("north", commands.do_move, exit_data.direction.NORTH)
    self.enable("east", commands.do_move, exit_data.direction.EAST)
    self.enable("south", commands.do_move, exit_data.direction.SOUTH)
    self.enable("west", commands.do_move, exit_data.direction.WEST)
    self.enable("up", commands.do_move, exit_data.direction.UP)
    self.enable("down", commands.do_move, exit_data.direction.DOWN)

    self.enable("colors", commands.do_colors, None)
    self.enable("copyover", commands.do_copyover, None)
    self.enable("db", commands.do_db, None)
    self.enable("drop", commands.do_drop, None)
    self.enable("get", commands.do_get, None)
    self.enable("give", commands.do_give, None)
    self.enable("gossip", commands.do_gossip, None)
    self.enable("goto", commands.do_goto, None)
    self.enable("help", commands.do_help, None)
    self.enable("inventory", commands.do_inventory, None)
    self.enable("look", commands.do_look, None)
    self.enable("pindex", commands.do_pindex, None)
    self.enable("prefs", commands.do_prefs, None)
    self.enable("quit", commands.do_quit, None)
    self.enable("save", commands.do_save, None)
    self.enable("say", commands.do_say, None)
    self.enable("score", commands.do_score, None)
    self.enable("shutdown", commands.do_shutdown, None)
    self.enable("title", commands.do_title, None)
    self.enable("who", commands.do_who, None)

    self.enable("mlist", olc.do_mlist, None)
    self.enable("olist", olc.do_olist, None)
    self.enable("rlist", old.do_rlist, None)
    self.enable("zlist", old.do_zlist, None)
    self.enable("redit", old.do_redit, None)
    self.enable("zedit", old.do_zedit, None)