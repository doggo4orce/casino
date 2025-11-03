import database
import pc_data

import unittest

class TestPcData(unittest.TestCase):
  def test_pc_data(self):
    pc = pc_data.pc_data()

    pc.name = "Roobiki"
    pc.reset_aliases("roobiki")
    pc.ldesc = "Roobiki is standing here."
    pc.desc = "He looks handsome as usual."
    pc.password = "p@ssw0rd"
    pc.player_id = 1
    pc.title = "the great guy"

    pc.set_pref("brief_mode", True)
    pc.set_pref("active_idle", True)

    pc.set_pref("screen_width", 50)
    pc.set_pref("screen_length", 30)

    # anything goes for text prefs
    pc.set_pref("color_mode", "anything goes for now")

    print(pc.debug())

if __name__ == "__main__":
  unittest.main()