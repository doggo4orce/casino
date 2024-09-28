import config
import pref_data

import unittest

class TestPrefData(unittest.TestCase):
  def test_pref_data_numeric(self):
    pdn = pref_data.pref_data_numeric()

    self.assertIn("screen_width", pdn.__dataclass_fields__)
    self.assertIn("screen_length", pdn.__dataclass_fields__)
    self.assertNotIn("foobar", pdn.__dataclass_fields__)

    self.assertEqual(pdn.get("screen_width"), config.DEFAULT_SCREEN_WIDTH)
    self.assertEqual(pdn.get("screen_length"), config.DEFAULT_SCREEN_LENGTH)

    pdn.set("screen_width", 30)
    self.assertEqual(pdn.get("screen_width"), 30)

  def test_pref_data_text(self):
    pdt = pref_data.pref_data_text()

    self.assertIn("color_mode", pdt.__dataclass_fields__)
    self.assertNotIn("foobar", pdt.__dataclass_fields__)

    self.assertEqual(pdt.get("color_mode"), config.DEFAULT_COLOR_MODE)

    pdt.set("color_mode", "16")
    self.assertEqual(pdt.get("color_mode"), "16")

    pdt.set("color_mode", "off")
    self.assertEqual(pdt.get("color_mode"), "off")

  def tests_pref_data_flags(self):
    pdf = pref_data.pref_data_flags()

    self.assertIn("active_idle", pdf.__dataclass_fields__)
    self.assertIn("brief_mode", pdf.__dataclass_fields__)
    self.assertIn("debug_mode", pdf.__dataclass_fields__)
    self.assertNotIn("foobar", pdf.__dataclass_fields__)

    self.assertEqual(pdf.get("active_idle"), config.DEFAULT_ACTIVE_IDLE)
    self.assertEqual(pdf.get("brief_mode"), config.DEFAULT_BRIEF_MODE)
    self.assertEqual(pdf.get("debug_mode"), config.DEFAULT_DEBUG_MODE)

    pdf.set("brief_mode", True)
    self.assertTrue(pdf.get("brief_mode"))
    pdf.flip("brief_mode")
    self.assertFalse(pdf.get("brief_mode"))
    pdf.flip("brief_mode")
    self.assertTrue(pdf.get("brief_mode"))

if __name__ == "__main__":
  unittest.main()