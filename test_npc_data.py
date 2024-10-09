import character_data
import npc_data
import unique_id_data

import unittest

class TestNpcData(unittest.TestCase):
  def test_npc_data(self):
    npc = npc_data.npc_data()

  def test_from_char(self):
    ch = character_data.character_data()
    ch.name = "bob"
    ch.desc = "<p>This is Bob.</p>"
    ch.ldesc = "Bob is standing around."
    ch.room = unique_id_data.unique_id_data("stockville", "casino")
    ch.reset_aliases("bob", "nice")

    npc = npc_data.npc_data.from_character(ch)

    print(ch.debug() + "\r\n")
    print(npc.debug())
if __name__ == "__main__":
  unittest.main()