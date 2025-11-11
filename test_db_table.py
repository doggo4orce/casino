# python modules
import sqlite3
import unittest

# local modules
import db_handler
import db_table

class TestDBTable(unittest.TestCase):
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

  def test_num_records(self):
    handler = db_handler.db_handler()
    handler.connect(":memory:")

    # should have zero tables at first
    self.assertEqual(handler.num_tables(), 0)

    p_table = db_table.db_table(handler, "players")
    p_table.create(
      ("name", str, True),
      ("age", int, False),
      ("drink", str, False),
      ("food", str, False),
      ("job", str, False)
    )

    p_table.insert(name='roobiki', age=41, drink="beer", food='nachos', job='comedian')
    p_table.insert(name='deglo', age=33, drink="coffee", food="nachos")
    p_table.insert(name='bob', age=21, drink="coffee", food="nachos", job="janitor")

    # should have three records
    self.assertEqual(p_table.num_records(), 3)

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

    # make player table
    table = db_table.db_table(handler, "p_table")

    # table is created
    table.create(
      ("first_name", str, True),
      ("last_name", str, False),
      ("height", int, False)
    )

    # check the columns
    self.assertTrue(table.has_column("first_name", str, True))
    self.assertTrue(table.has_column("last_name", str, False))
    self.assertTrue(table.has_column("height", int, False))

    # drop one of the columns
    table.drop_column("height")

    # check that it worked
    self.assertFalse(table.has_column("height"))

    # cannot drop a column which acts as primary key
    with self.assertRaises(sqlite3.OperationalError):
      table.drop_column("first_name")

  def test_insert_delete_search(self):
    handler = db_handler.db_handler()
    handler.connect(":memory:")

    # should have zero tables at first
    self.assertEqual(handler.num_tables(), 0)

    p_table = db_table.db_table(handler, "players")
    p_table.create(
      ("name", str, True),
      ("age", int, False),
      ("drink", str, False),
      ("food", str, False),
      ("job", str, False)
    )

    wizard_table = db_table.db_table(handler, "wizards")
    wizard_table.create(
      ("name", str, False),
      ("position", str, False)
    )

    # make sure the tables exists
    self.assertTrue(p_table.exists())
    self.assertTrue(wizard_table.exists())

    # but nothing else does
    self.assertEqual(handler.num_tables(), 2)
    self.assertFalse(handler.table_exists("wizerds"))

    # and has the right columns
    self.assertEqual(handler.list_column_names("players"), ["name", "age", "drink", "food", "job"])
    self.assertEqual(handler.num_columns("players"), 5)

    with self.assertRaises(RuntimeError):
      # this should cause an error
      p_table.create(
        ("field_one", str, False),
        ("field_two", int, False)
      )

    p_table.insert(name='roobiki', age=41, drink="beer", food='nachos', job='comedian')
    p_table.insert(name='deglo', age=33, drink="coffee", food="nachos")
    p_table.insert(name='bob',age=21, drink="coffee", food="nachos", job="janitor")

    # should have three records
    self.assertEqual(p_table.num_records(), 3)

    # should match with deglo and bob
    rs = p_table.search(drink="coffee", food="nachos")

    # which means two matches
    self.assertEqual(rs.num_results, 2)

    # this will delete bob
    p_table.delete(drink="coffee", food="nachos", age=21)

    # only roobiki and deglo remain
    self.assertEqual(p_table.num_records(), 2)

    # close handler object for good measure
    handler.close()

  def test_primary_fields(self):
    handler = db_handler.db_handler()
    handler.connect(":memory:")

    # should have zero tables at first
    self.assertEqual(handler.num_tables(), 0)

    p_table = db_table.db_table(handler, "players")
    p_table.create(
      ("name", str, True),
      ("age", int, True),
      ("drink", str, False),
      ("food", str, False),
      ("job", str, False)
    )

    wizard_table = db_table.db_table(handler, "wizards")
    wizard_table.create(
      ("name", str, False),
      ("position", str, False)
    )

    self.assertEqual(p_table.primary_fields(), ["name", "age"])
    self.assertEqual(wizard_table.primary_fields(), list())

  def test_get_by_pk(self):
    handler = db_handler.db_handler()
    handler.connect(":memory:")

    # should have zero tables at first
    self.assertEqual(handler.num_tables(), 0)

    p_table = db_table.db_table(handler, "players")
    p_table.create(
      ("first_name", str, True),
      ("last_name", str, True),
      ("age", int, False),
      ("drink", str, False),
      ("food", str, False),
      ("job", str, False)
    )

    p_table.insert(first_name='roobiki', last_name="tendo", age=41, drink="beer", food='nachos', job='comedian')
    p_table.insert(first_name='beastly', last_name="fido", age=33, drink="coffee", food="nachos")
    p_table.insert(first_name='bob', last_name="dylan", age=21, drink="coffee", food="nachos", job="janitor")

    self.assertEqual(p_table.primary_fields(), ["first_name", "last_name"])

    record = p_table.get_by_pk(first_name='roobiki', last_name="tendo")

if __name__ == "__main__":
  unittest.main()
  # unittest.main(defaultTest="TestDBTable.test_num_records")