import command_interpreter
import descriptor_data
import pc_data
import unique_id_data
import unittest

import test_utilities

class TestCommandInterpreter(unittest.TestCase):
  def test_handle_input(self):
    # build a tiny test world
    mud, zone, room = test_utilities.create_single_room_test_world()

    # set up command interpreter
    nanny = command_interpreter.command_interpreter(mud)
    nanny.load_commands()

    # put the character in the room
    d = descriptor_data.descriptor_data(None, "localhost")
    pc = pc_data.pc_data()
    d.character = pc
    pc.descriptor = d
    d.state = descriptor_data.descriptor_state.CHATTING
    d.character.room = unique_id_data.unique_id_data(room.id, room.zone_id)
    mud.add_character_to_room(d.character, room)

    d.input_stream.input_q.append("look")
    nanny.handle_next_input(d, mud, None, None)

    d.input_stream.input_q.append("redit")
    nanny.handle_next_input(d, mud, None, None)

    d.input_stream.input_q.append("q")
    nanny.handle_next_input(d, mud, None, None)
    print(d.out_buf)

   
if __name__ == "__main__":
  unittest.main()