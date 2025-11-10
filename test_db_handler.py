import db_column
import db_handler
import db_result
import db_table

import unittest

class TestDbHandler(unittest.TestCase):
  def test_db(self):
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
    self.assertTrue(handler.table_exists("players"))
    self.assertTrue(handler.table_exists("wizards"))

    # but nothing else does
    self.assertEqual(handler.num_tables(), 2)
    self.assertFalse(handler.table_exists("wizerds"))

    # and has the right columns
    self.assertEqual(handler.list_column_names("players"), ["name", "age", "drink", "food", "job"])
    self.assertEqual(handler.num_columns("players"), 5)

    # this should cause an error
    p_table.create(
      ("field_one", str, False),
      ("field_two", int, False)
    )

    p_table.insert(
      name='roobiki',
      age=41, #ugh
      drink="beer",
      food='nachos',
      job='comedian'
    )

    p_table.insert(
      name='deglo',
      age=33,
      drink="coffee",
      food="nachos"
    )

    p_table.insert(
      name='bob',
      age=21,
      drink="coffee",
      food="nachos",
      job="janitor"
    )

    p_table.select(drink="coffee", food="nachos"
)
    # search table for entries satisfying multiple clauses
    handler.search_table("players", )

    rs = handler.fetch_all()

    # should have found two matches, deglo and bob
    self.assertEqual(rs.num_results, 2)

    # this will delete bob
    handler.delete_records("players", drink="coffee", food="nachos", age=21)

    # only roobiki and deglo remain
    self.assertEqual(handler.num_records("players"), 2)

    handler.close()

  def test_drop_table(self):
    handler = db_handler.db_handler()
    handler.connect(":memory:")

    handler.create_table("test_table1", ("f_one", int, False), ("f_two", str, False))
    handler.create_table("test_table2", ("g_one", int, False), ("g_two", str, False))

    self.assertTrue(handler.table_exists("test_table1"))
    self.assertTrue(handler.table_exists("test_table2"))

    handler.drop_table("test_table1")

    self.assertNotIn("test_table1", handler.list_tables())
    self.assertIn("test_table2", handler.list_tables())
    self.assertEqual(handler.num_tables(), 1)

  def test_add_drop_columns(self):
    handler = db_handler.db_handler()
    handler.connect(":memory:")

    handler.create_table("players",
      ("name", str, False),
      ("age", int, False),
      ("drink", str, False),
      ("food", str, False),
      ("job", str, False)
    )

    self.assertEqual(handler.num_columns("players"), 5)

    self.assertTrue(handler.has_column("players", "name", str))
    self.assertEqual(handler.column_type("players", "name"), str)
    self.assertTrue(handler.has_column("players", "age", int))
    self.assertEqual(handler.column_type("players", "age"), int)
    self.assertTrue(handler.has_column("players", "drink", str))
    self.assertEqual(handler.column_type("players", "drink"), str)
    self.assertTrue(handler.has_column("players", "food", str))
    self.assertEqual(handler.column_type("players", "food"), str)
    self.assertTrue(handler.has_column("players", "job", str))
    self.assertEqual(handler.column_type("players", "job"), str)

    handler.drop_column("players", "age")

    self.assertEqual(handler.num_columns("players"), 4)
    self.assertNotIn("age", handler.list_column_names("players"))
    self.assertIsNone(handler.column_type("players", "age"))

    handler.add_column("players", "nickname", str)

    self.assertEqual(handler.num_columns("players"), 5)
    self.assertIn("nickname", handler.list_column_names("players"))

    handler.close()

  def test_has_column_and_type(self):
    handler = db_handler.db_handler()
    handler.connect(":memory:")

    handler.create_table("players",
      ("name", str, False),
      ("age", int, False),
      ("drink", str, False),
      ("food", str, False),
      ("job", str, False)
    )

    self.assertTrue(handler.has_column("players", "name", str))
    self.assertFalse(handler.has_column("players", "name", int))
    self.assertFalse(handler.has_column("players", "song", str))

    self.assertEqual(handler.column_type("players", "name"), str)
    self.assertEqual(handler.column_type("players", "age"), int)
    self.assertIsNone(handler.column_type("players", "typo"))

    handler.close()

  def test_verify_columns(self):
    handler = db_handler.db_handler()
    handler.connect(":memory:")

    handler.create_table("players",
      ("name", str, False),
      ("age", int, False)
    )

    handler.verify_columns("players", ("drink", str, False), ("height", int, False))
    handler.verify_columns("mobs", ("hp", int, False), ("experience", int, False))
    self.assertTrue(handler.has_column("players", "drink", str))
    self.assertTrue(handler.has_column("players", "height", int))

    handler.close()

  def test_delete_records(self):
    handler = db_handler.db_handler()
    handler.connect(":memory:")

    handler.create_table("players",
      ("name", str, False),
      ("age", int, False),
      ("drink", str, False),
      ("food", str, False),
      ("job", str, False)
    )

    self.assertEqual(handler.num_records("players"), 0)

    handler.insert_record("players",
      name='roobiki',
      age=40, #ugh
      drink="beer",
      food='nachos',
      job='comedian'
    )

    handler.insert_record("players",
      name='deglo',
      age=33,
      drink="coffee",
      food="nachos"
    )

    handler.insert_record("players",
      name='bob',
      age=21,
      drink="coffee",
      food="nachos",
      job="janitor"
    )

    self.assertEqual(handler.num_records("players"), 3)

    handler.delete_records("players", drink="coffee")

    self.assertEqual(handler.num_records("players"), 1)

    handler.search_table("players", name="roobiki")
    self.assertTrue(handler.fetch_one() != None)

    handler.close()

  def test_get_record(self):
    handler = db_handler.db_handler()
    handler.connect(":memory:")

    handler.create_table("players",
      ("name", str, False),
      ("age", int, False),
      ("drink", str, False),
      ("food", str, False),
      ("job", str, False)
    )

    handler.insert_record("players",
      name='roobiki',
      age=40, #ugh
      drink="beer",
      food='nachos',
      job='comedian'
    )

    handler.insert_record("players",
      name='deglo',
      age=33,
      drink="coffee",
      food="nachos"
    )

    handler.insert_record("players",
      name='bob',
      age=21,
      drink="coffee",
      food="nachos",
      job="janitor"
    )

    bob = handler.get_record("players", name='bob')

    self.assertEqual(bob['name'], 'bob')
    self.assertEqual(bob['age'], 21)

  def test_apostrophe(self):
    handler = db_handler.db_handler()
    handler.connect(":memory:")

    handler.create_table("npcs",
      ("name", str, False),
      ("age", int, False),
      ("desc", str, False)
    )

    handler.insert_record("npcs",
      name="the baker",
      age=52,
      desc="He's got an apostrophe in his description."  
    )

    baker = handler.get_record("npcs", name="the baker")

    self.assertEqual(baker["name"], "the baker")
    self.assertEqual(baker["age"], 52)
    self.assertEqual(baker["desc"], "He's got an apostrophe in his description.")
    
if __name__ == "__main__":
  unittest.main()