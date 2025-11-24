import commands
import dataclasses
import mudlog
import object_data
import pc_data
import spec_proc_data
import table_data

@dataclasses.dataclass
class baccarat_bet_data:
  pass

@dataclasses.dataclass
class guest_data:
  char:        pc_data.pc_data
  caught_up:   bool

class baccarat_table_data(table_data.table_data):
  NUM_BACCARAT_SEATS = 3

  def __init__(self, proto=None):
    super().__init__(self.NUM_BACCARAT_SEATS, proto)
    self._dealer = None

  @classmethod
  def from_table(cls, old_table):
    ret_val = cls()

    ret_val.copy_from(old_table)

    if old_table.num_seats != 3:
      mudlog.warning(f"Changing {old_table}, which has {old_table.num_seats} to a baccarat table.")
      mudlog.warning("Adjusting capacity to 3.")
      ret_val.num_seats = 3

      for idx, guest in enumerate(old_table.guests()):
        if idx >= 3:
          mudlog.warning(f"Removing guest: {guest}.")
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

  def debug(self):
    ret_val = super().debug()
    ret_val += f"Dealer: {self.dealer}\r\n"
    return ret_val

def baccarat_table_syntax_parser(mud, me, ch, command, argument, db):
  args = argument.split()
  num_args = len(args)

  full_command = nanny.look_up_command(command)
  
  if not isinstance(me, baccarat_table):
    logging.warning(f"Attem[[[[[[pting to call inappropriate spec_proc 'baccarat_table_syntax_parser' on obj {me}.")
    return

  # these are the commands we listen to for non-guests
  if command == "sit":
    if ch.name in me.guests:
      ch.write("You are already playing!\r\n")
    elif me.full:
      ch.write("You can't join -- the table is full!\r\n")
    else:
      ch.write("You sit down at the table, and join the game.\r\n")
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
      return spec_procs.prefix_command_trigger_messages.RUN_INTERPRETER

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
    return spec_procs.prefix_command_trigger_messages.BLOCK_INTERPRETER

  