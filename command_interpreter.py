from color import *
import cmd_trig_data
import command_data
import commands
import config
import descriptor_data
import editor
import exit_data
import mudlog
import npc_data
import olc
import pc_data
import telnet
import unique_id_data

class command_interpreter:
  """Creates a command interpreter object to parse input from players
     and handle the game's response.
     cmd_dict = commands which have been loaded"""
  def __init__(self, game=None):
    self._cmd_dict = dict()

  """enable(command, function, subcmd)                    <- add new command object to list based on parameters
     disable(command)                                     <- remove command from list by name
     handle_next_input(d, mud, server, db)                <- handle next input from descriptor
     look_up_command(name)                                <- look up command based on name
     interpret_msg(d, command, argument, mud, server, db) <- normal in-game command interpreter
     load_commands()                                      <- load all commands into the game
     writing_follow_up(d)                                 <- save edit buffer appropriately"""

  def enable(self, command, function, subcmd):
    self._cmd_dict[command] = command_data.command_data(command, function, subcmd)

  def disable(self, command):
    for cmd_object in self.commands:
      if cmd_object.command == commmand:
        del self._cmd_dict[command]

  # Server object passed because the mud doesn't know about it, and some administrative
  # commands might like to inspect the server (e.g. to look up states of all descriptors)
  def handle_next_input(self, d, mud, server, db):
    # grab the next input from their input queue
    msg = d.input_stream.pop_input()

    # if they had no message, take no action
    if msg is None:
      return

    # debugging logs
    if d.character:
      mudlog.debug(f"handle_next_input called on player {d.character.name} with input '{msg}'")
    else:
      mudlog.debug(f"handle_next_input called by descriptor from {d.client.term_host} with input '{msg}'")

    # if we got this far, they at least hit enter, and need their prompt drawn again
    d.has_prompt = False

    # strip leading or trailing whitespaces
    stripped_msg = msg.strip()

    # argument contains everything after the first space
    command, argument = (stripped_msg.split(" ", 1) + ["", ""])[:2]

    # if user is writing, let the editor handle the input
    if d.writing:

      # editor handler lets us know if user finished writing or not
      done_writing = editor.editor_handle_input(d, msg)

      # if so, send appropriate follow-up, based on what they were doing before
      if done_writing:
        self.writing_follow_up(d)

      return

    # basic command parser for players in normal gameplay mode
    if d.state == descriptor_data.descriptor_state.CHATTING:
      self.interpret_msg(d, command, argument, mud, server, db)
      return

    # olc has its own input handler
    if d.state == descriptor_data.descriptor_state.OLC:
      olc.handle_input(d, stripped_msg, server, mud, db)
      return

    # if we made it here, pass the input to nanny
    nanny.nanny(d, mud, server, db, command, msg)
        
  def look_up_command(self, command):
    for key in self.cmd_dict.keys():
      if self.cmd_dict[key].command.startswith(command):
        return self.cmd_dict[key].command
    return None

  def interpret_msg(self, d, command, argument, mud, server, db):
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

    cmd_key = self.look_up_command(command)

    if cmd_key != None:
      cmd_obj = self.cmd_dict[cmd_key]
      cmd_obj.function(d.character, cmd_key, argument, server, mud, db, self)
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
  def writing_follow_up(self, d):
    if d.state == descriptor_data.descriptor_state.OLC:
      olc.olc_writing_follow_up(d)
    # other possibilities:
    #   reporting_bug, mailing letter, scribing scroll, etc.

  def load_commands(self):
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
    self.enable("rlist", olc.do_rlist, None)
    self.enable("zlist", olc.do_zlist, None)
    self.enable("redit", olc.do_redit, None)
    self.enable("zedit", olc.do_zedit, None)