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
import test_utilities


class TestNanny(unittest.TestCase):
  def test_nanny_individual_parse_functions_good_input(self):
    client, host = socket.socketpair()
    d = descriptor_data.descriptor_data(host, "client.dyn.dns.org")

    mud = game_data.game_data()

    db = database.database(":memory:")
    db.connect()
    db.create_tables()
    db._state = database.database_state.VERIFIED


    d.state = descriptor_data.descriptor_state.GET_NAME

    nanny.nanny_parse_get_name(d, mud, db, "kyle", "")

    self.assertEqual(d.state, descriptor_data.descriptor_state.CONFIRM_NAME)

    nanny.nanny_parse_confirm_name(d, "y")

    self.assertEqual(d.state, descriptor_data.descriptor_state.GET_NEW_PASS)

    nanny.nanny_parse_get_new_pass(d, "asdf") # go check function parameters, rename possibly
    
    self.assertEqual(d.state, descriptor_data.descriptor_state.CONFIRM_PASS)

if __name__ == "__main__":
  unittest.main()