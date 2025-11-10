# python modules
import sqlite3
import unittest

# local modules
import db_handler
import db_table

class test_db_table(unittest.TestCase):
  def test_create_drop(self):
    handler = db_handler.db_handler()
    handler.connect(":memory:")

    table = db_table.db_table(handler, "p_table")

    self.assertFalse(table.exists())

    table.create(
      ("first_name", str, True),
      ("last_name", str, True),
      ("height", int, False)
    )

    self.assertTrue(table.exists())

  def test_composite_key(self):
    handler = db_handler.db_handler()
    handler.connect(":memory:")

    table1 = db_table.db_table(handler, "p_table")
    table2 = db_table.db_table(handler, "q_table")

    table1.create(
      ("first_name", str, True),
      ("last_name", str, True),
      ("height", int, False)
    )

    table2.create(
      ("first_name", str, True),
      ("last_name", str, False),
      ("height", int, False)
    )

    self.assertTrue(table1.has_composite_key)
    self.assertFalse(table2.has_composite_key)

  def test_columns(self):
    # table is initialized
    handler = db_handler.db_handler()
    handler.connect(":memory:")
    table = db_table.db_table(handler, "p_table")

    # table is created
    table.create(
      ("first_name", str, True),
      ("last_name", str, False),
      ("height", int, False)
    )

    # check the columns
    self.assertTrue(table.has_column("first_name", str))
    self.assertTrue(table.has_column("last_name", str))
    self.assertTrue(table.has_column("height", int))

    # drop one of the columns
    table.drop_column("height")

    # check that it worked
    self.assertFalse(table.has_column("height"))

    # cannot drop a column which acts as primary key
    with self.assertRaises(sqlite3.OperationalError):
      table.drop("first_name")

if __name__ == "__main__":
  unittest.main()