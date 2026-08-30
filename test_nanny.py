# python modules
import socket
import unittest

# local modules
import database
import descriptor_data
import game_data
import mudlog
import nanny
import pc_data
import room_data
import server
import test_utilities
import zone_data


class TestNanny(unittest.TestCase):
  def test_nanny_individual_parse_functions_good_input(self):
    client, host = socket.socketpair()
    d = descriptor_data.descriptor_data(host, "client.dyn.dns.org")

    void_room = room_data.room_data()
    void_room.attributes.zone_id = 'stockville'
    void_room.attributes.id = 'void'

    void_zone = zone_data.zone_data()
    void_zone.id = 'stockville'
    void_zone.add_room(void_room)

    mud = game_data.game_data()
    mud.add_zone(void_zone)

    db = database.database(":memory:")
    db.connect()
    db.create_tables()
    db._state = database.database_state.VERIFIED

    d.state = descriptor_data.descriptor_state.GET_NAME

    nanny.input_handler_parse_get_name(d, mud, db, "kyle", "")

    self.assertEqual(d.state, descriptor_data.descriptor_state.CONFIRM_NAME)

    nanny.input_handler_parse_confirm_name(d, "y")

    self.assertEqual(d.state, descriptor_data.descriptor_state.GET_NEW_PASS)

    nanny.input_handler_parse_get_new_pass(d, "asdf")

    self.assertEqual(d.state, descriptor_data.descriptor_state.CONFIRM_PASS)

    nanny.input_handler_parse_confirm_pass(d, mud, db, "asdf")

    self.assertEqual(d.state, descriptor_data.descriptor_state.CHATTING)

    client.close()
    d.close()

  def test_input_handler_generic_good_input(self):
    client, host = socket.socketpair()
    d = descriptor_data.descriptor_data(host, "client.dyn.dns.org")

    void_room = room_data.room_data()
    void_room.attributes.zone_id = 'stockville'
    void_room.attributes.id = 'void'

    void_zone = zone_data.zone_data()
    void_zone.id = 'stockville'
    void_zone.add_room(void_room)

    mud = game_data.game_data()
    mud.add_zone(void_zone)

    db = database.database(":memory:")
    db.connect()
    db.create_tables()
    db._state = database.database_state.VERIFIED

    d.state = descriptor_data.descriptor_state.GET_NAME

    nanny.input_handler_generic(d, mud, None, db, "kyle", "", "kyle")

    self.assertEqual(d.state, descriptor_data.descriptor_state.CONFIRM_NAME)

    nanny.input_handler_generic(d, mud, None, db, "y", "", "ye")

    self.assertEqual(d.state, descriptor_data.descriptor_state.GET_NEW_PASS)

    nanny.input_handler_generic(d, mud, None, db, "asdf", "", "asdf")

    self.assertEqual(d.state, descriptor_data.descriptor_state.CONFIRM_PASS)

    nanny.input_handler_generic(d, mud, None, db, "asdf", "", "asdf")

    self.assertEqual(d.state, descriptor_data.descriptor_state.CHATTING)

    client.close()
    d.close()

if __name__ == "__main__":
  unittest.main()