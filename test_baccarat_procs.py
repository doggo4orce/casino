import baccarat_dealer_data
import baccarat_procs
import pc_data
import unittest

class TestBaccaratProcs(unittest.TestCase):
  def test_baccarat_procs(self):
    dealer = baccarat_dealer_data.baccarat_dealer_data()
    player = pc_data.pc_data()

    baccarat_procs.baccarat_dealer_history()
if __name__ == "__main__":
  unittest.main()