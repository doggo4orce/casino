import character_data

import obj_proto_data
import table_data

import unittest

class TestTableData(unittest.TestCase):
  def test_table(self):
    obj_p = obj_proto_data.obj_proto_data()
    obj_p.name = "a wooden table"
    obj_p.reset_aliases("wooden", "table")
    obj_p.ldesc = "A wooden table has been placed here."
    obj_p.desc = "It's covered in beer bottles and poker cards."
    table = table_data.table_data(4, obj_p)

    bob = character_data.character_data()
    bob.name = "Bob"
    doug = character_data.character_data()
    doug.name = "Doug"
    roobiki = character_data.character_data()
    roobiki.name = "Roobiki"
    table.add_guest(bob)
    table.add_guest(doug)
    table.add_guest(roobiki)

    print(table.debug())

if __name__ == "__main__":
  unittest.main()