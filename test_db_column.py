import db_column

import unittest

class TestDbColumn(unittest.TestCase):
  def test_column_class(self):
    c = db_column.db_column("drink", str)
    self.assertEqual(c.name, "drink")
    self.assertEqual(c.type, str)
    self.assertEqual(c.sqlite3_type, "text")

    print(c)

    c = db_column.db_column("hp", int)
    self.assertEqual(c.name, "hp")
    self.assertEqual(c.type, int)
    self.assertEqual(c.sqlite3_type, "int")

    print(c)

if __name__ == "__main__":
  unittest.main()