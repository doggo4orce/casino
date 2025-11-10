import db_table
import unittest

class test_db_table(unittest.TestCase):
  def test_init(self):
    table1 = db_table.db_table("p_table",
     ("id", int, True),
     ("name", str, False)
    )

    table2 = db_table.db_table("p_table",
     ("name", str, False),
     ("weight", int, False),
     ("height", int, False)
    )

    self.assertTrue(table1.has_primary_key)
    self.assertFalse(table2.has_primary_key)
    self.assertFalse(table1.has_composite_key)

    print(table1.debug() + "\r\n")
    print(table2.debug())

  def test_creation_syntax(self):
    table = db_table.db_table("p_table",
     ("first_name", str, True),
     ("last_name", str, True),
     ("height", int, False)
    )

    self.assertTrue(table.has_composite_key)

    print(table.creation_syntax())
   
if __name__ == "__main__":
  unittest.main()