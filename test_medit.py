# Python Modules
import unittest

# Local Modules
import database
import descriptor_data
import medit
import olc
import pc_data
import test_utilities

class TestZeditSave(unittest.TestCase):
  def test_create_npc(self):
    db = database.database(":memory:")
    db.connect()

    # create player/descriptor combo
    player = pc_data.pc_data()
    d = descriptor_data.descriptor_data(None, "localhost")

    # connect them
    player.descriptor = d
    d.character = player
    d.state = descriptor_data.descriptor_state.CHATTING

    # create a single room so they can perform tedit command
    mud, zone, room = test_utilities.create_single_room_test_world()

    # must be in room to use tedit command
    mud.add_character_to_room(player, room)

    # make a new table and change its name    
    olc.do_medit(player, None, "new_npc", None, mud, db, None)

    print(d.out_buf)

if __name__ == "__main__":
  unittest.main()