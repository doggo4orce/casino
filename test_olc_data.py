import olc_data
import redit
import redit_save_data
import unittest

class TestOLCData(unittest.TestCase):
  def test_olc_data(self):
    olc = olc_data.olc_data()
    rsd = redit_save_data.redit_save_data()

    olc.mode = olc_data.olc_mode.OLC_MODE_ZEDIT
    olc.state = redit.redit_state.REDIT_MAIN_MENU
    olc.changes = True
    olc.save_data = rsd

    self.assertEqual(olc.mode, olc_data.olc_mode.OLC_MODE_ZEDIT)
    self.assertEqual(olc.state, redit.redit_state.REDIT_MAIN_MENU)
    self.assertTrue(olc.changes)
    self.assertEqual(olc.save_data, rsd)

if __name__ == "__main__":
  unittest.main()