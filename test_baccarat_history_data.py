import baccarat_history_data
import unittest

class TestBaccaratShoeData(unittest.TestCase):
  def test_report_count(self):
    b_hist = baccarat_history_data.baccarat_history_data()

    b_hist.report_history(baccarat_history_data.history_entry.PANDA)
    b_hist.report_history(baccarat_history_data.history_entry.PANDA)
    b_hist.report_history(baccarat_history_data.history_entry.PANDA)
    b_hist.report_history(baccarat_history_data.history_entry.PLAYER_WIN)
    b_hist.report_history(baccarat_history_data.history_entry.DRAGON)
    b_hist.report_history(baccarat_history_data.history_entry.BANKER_WIN)
    b_hist.report_history(baccarat_history_data.history_entry.DRAGON)

    self.assertEqual(b_hist.count_reports(baccarat_history_data.history_entry.PANDA), 3)
    self.assertEqual(b_hist.count_reports(baccarat_history_data.history_entry.PLAYER_WIN), 1)
    self.assertEqual(b_hist.count_reports(baccarat_history_data.history_entry.BANKER_WIN), 1)
    self.assertEqual(b_hist.count_reports(baccarat_history_data.history_entry.DRAGON), 2)

    b_hist.report_extra(baccarat_history_data.extra_side_bet.THREE_CARD_9_8)
    b_hist.report_extra(baccarat_history_data.extra_side_bet.NATURAL_9_8)
    b_hist.report_extra(baccarat_history_data.extra_side_bet.NATURAL_9_8)
    b_hist.report_extra(baccarat_history_data.extra_side_bet.ANY_8_7)

    self.assertEqual(b_hist.count_extras(baccarat_history_data.extra_side_bet.THREE_CARD_9_8), 1)
    self.assertEqual(b_hist.count_extras(baccarat_history_data.extra_side_bet.NATURAL_9_8), 2)
    self.assertEqual(b_hist.count_extras(baccarat_history_data.extra_side_bet.ANY_8_7), 1)

if __name__ == '__main__':
  unittest.main()