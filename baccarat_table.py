import commands
import logging
import nanny
import object
import spec_procs
import table

class baccarat_table(table.table):
  NUM_BACCARAT_SEATS = 3

  def __init__(self, proto=None):
    super().__init__(self.NUM_BACCARAT_SEATS, proto)
    self._dealer = None

  @classmethod
  def from_table(cls, old_table):
    ret_val = cls()
    
    ret_val.entity = old_table.entity
    ret_val.ldesc = old_table.ldesc
    ret_val.prefix_command_triggers = old_table.prefix_command_triggers
    ret_val.suffix_command_triggers = old_table.suffix_command_triggers
    ret_val.heart_beat_procs = old_table.heart_beat_procs

    if old_table.num_seats != 3:
      logging.warning(f"Changing {old_table}, which has {old_table.num_seats} to a baccarat table.")
      logging.warning("Adjusting capacity to 3.")
      ret_val.num_seats = 3

      for idx, guest in enumerate(old_table.guests):
        if idx >= 3:
          logging.warning(f"Removing guest: {guest}.")
        else:
          ret_val.add_player(guest)

    return ret_val

  @property
  def dealer(self):
    return self._dealer

  @property
  def hand(self):
    if self.dealer == None:
      return None
    return self.dealer.hand

  @dealer.setter
  def dealer(self, new_dealer):
    self._dealer = new_dealer

  def delay(self, time):
    if self.dealer == None:
      logging.warning(f"Table {self} attempting to delay non-existant dealer by {time} heartbeats.")
    else:
      self.dealer.bac_paused += time

  def render(self):
    ret_val = f"{' '*17}Player:{' '*32}Banker:\r\n"

    if self.hand == None:
      ret_val += "\r\n" * 6
    else:
      ret_val += f"{self.hand.display2()}\r\n"

    ret_val += """     +------+-----+-------+  +------+-----+-------+  +------+-----+-------+
     |Panda8| Tie |Dragon7|  |Panda8| Tie |Dragon7|  |Panda8| Tie |Dragon7|
     +------+-----+-------+  +------+-----+-------+  +------+-----+-------+
     |      Banker        |  |      Banker        |  |      Banker        |
     +--------------------+  +--------------------+  +--------------------+
     |      Player        |  |      Player        |  |      Player        |
     +--------------------+  +--------------------+  +--------------------+
     |                    |  |                    |  |                    |
     |                    |  |                    |  |                    |
     |                    |  |                    |  |                    |
     |                    |  |                    |  |                    |
     |                    |  |                    |  |                    |
     |                    |  |                    |  |                    |
     +--------------------+  +--------------------+  +--------------------+"""

    return ret_val

def baccarat_table_syntax_parser(mud, me, ch, command, argument, db):
  args = argument.split()
  num_args = len(args)

  full_command = nanny.look_up_command(command)
  
  if not isinstance(me, baccarat_table):
    logging.warning(f"Attempting to call inappropriate spec_proc 'baccarat_table_syntax_parser' on obj {me}.")
    return

  # these are the commands we listen to for non-guests
  if command == "sit":
    if ch.name in me.guests:
      ch.write("You are already playing!")
    else:
      ch.write("You sit down at the table, and join the game.")
      me.add_guest(ch.name)
      me.delay(30)
    return spec_procs.prefix_command_trigger_messages.BLOCK_INTERPRETER
  # TODO: add obj_flags so this can be handled by an !TAKE flag or something
  elif full_command == "get":
    rm = mud.room_by_code(ch.room)
    obj = rm.inventory.obj_by_alias(args[0])
    if obj == me:
      commands.do_say(me.dealer, None, "You can't take this table!", False, mud, db)
      return spec_procs.prefix_command_trigger_messages.BLOCK_INTERPRETER
    else:
      spec_procs.prefix_command_trigger_messages.RUN_INTERPRETER
  if ch.name not in me.guests:
    return spec_procs.prefix_command_trigger_messages.RUN_INTERPRETER

  # the following commands only work for guests
  if command == "leave":
    if ch.name not in me.guests:
      ch.write("You can't get up and leave -- you aren't even playing!")
    else:
      ch.write("You stand up, excusing yourself from the table.")
      me.remove_guest(ch.name)
    return spec_procs.prefix_command_trigger_messages.BLOCK_INTERPRETER
  elif full_command == "look":
    ch.write(me.render())
    return spec_procs.prefix_command_trigger_messages.BLOCK_INTERPRETER
  elif full_command in ["north", "south", "east", "west", "up", "down"]:
    ch.write("You must leave the table before going anywhere.\r\n")
    ch.write("Type baccarat leave to do so.\r\n")
    return spec_procs.prefix_command_trigger_messages.BLOCK_INTERPRETER

  