# python modules
import unittest

# local modules
import event_data
import game_data

class TestGameData(unittest.TestCase):
  def test_add_event():
    mud = game_data.game_data()
    
    event = event_data.event_data()