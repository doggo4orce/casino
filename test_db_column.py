import db_column

import unittest

class TestDbColumn(unittest.TestCase):
  def test_column_class(self):
    c = db_column.db_column("drink", str, False)
    self.assertEqual(c.name, "drink")
    self.assertEqual(c.type, str)
    self.assertEqual(c.sqlite3_type, "text")
    self.assertFalse(c.is_primary)

    print(c)

    c = db_column.db_column("hp", int)
    self.assertEqual(c.name, "hp")
    self.assertEqual(c.type, int)
    self.assertEqual(c.sqlite3_type, "int")
    self.assertFalse(c.is_primary)

    print(c)

    c = db_column.db_column("id", int, primary=True)
    self.assertEqual(c.name, "id")
    self.assertEqual(c.type, int)
    self.assertEqual(c.sqlite3_type, "int")
    self.assertTrue(c.is_primary)    

    print(c)

  def test_tuple(self):
    c = db_column.db_column("drink", str, False)

    t = c.tuple()
    self.assertEqual(t[0], "drink")
    self.assertEqual(t[1], str)
    self.assertFalse(t[2])

if __name__ == "__main__":
  unittest.main()