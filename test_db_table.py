import db_handler
import db_table
import unittest

class test_db_table(unittest.TestCase):
  def test_table_creation(self):
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

    print("\r\n".join([str(column) for column in table1.list_columns()]))
    print("\r\n".join([str(column) for column in table2.list_columns()]))

    self.assertTrue(table1.has_composite_key)
    self.assertFalse(table2.has_composite_key)

if __name__ == "__main__":
  unittest.main()