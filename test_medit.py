# Python Modules
import unittest

# Local Modules
import command_interpreter_data
import database
import descriptor_data
import medit
import nanny
import npc_proto_data
import olc
import pc_data
import test_utilities

def process_input(d, input, mud, db, verbose, CI):
  if verbose:
    print(d.out_buf, input)
    d.out_buf = ""

  d.input_stream.input_q.append(input)

  CI.handle_next_input(d, mud, None, db)

class TestMEDIT(unittest.TestCase):
  def test_create_npc(self):
    db = database.database(":memory:")
    db.connect()
    db.create_tables()

    # create command interpreter
    CI = command_interpreter_data.command_interpreter_data()
    
    # only need one command
    CI.enable("medit", olc.do_medit, None)

    # create player/descriptor combo
    player = pc_data.pc_data()
    d = descriptor_data.descriptor_data(None, "localhost")

    # connect them
    player.descriptor = d
    d.character = player
    d.state = descriptor_data.descriptor_state.CHATTING

    # create a single room so they can perform tedit command
    mud, zone, room = test_utilities.create_single_room_test_world()

    # add an npc_proto to edit
    npcp = npc_proto_data.npc_proto_data()
    npcp.zone_id = zone.id
    npcp.id = "new_npc"
    zone.add_npc(npcp)

    # must be in room to use tedit command
    mud.add_character_to_room(player, room)

    verbose = True

    input_q = [
      "medit new_npc", # create new npc
      "1",             # select edit name
      "roobiki",       # change name to roobiki
      "2",             # select edit description
      "/c",            # clear buffer
      "desc",          # set description to "desc"
      "/s",            # save changes
      "3",             # select edit ldesc
      "here",          # set ldesc to "here"
      "4",             # select edit aliases
      "npc alias",     # enter npc and alias as aliases
      "q",             # save changes
      "y"              # confirm save
    ]

    for input in input_q:
      process_input(d, input, mud, db, verbose, CI)

    self.assertEqual(npcp.name, "roobiki")
    self.assertEqual(npcp.desc, "desc")
    self.assertEqual(npcp.ldesc, "here")

    self.assertTrue(npcp.has_alias("npc"))
    self.assertTrue(npcp.has_alias("alias"))
    self.assertEqual(npcp.num_aliases, 2)

if __name__ == "__main__":
  unittest.main()