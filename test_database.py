import database
import db_result

import unittest

class TestDb(unittest.TestCase):
  def test_db(self):
    db = database.database()
    db.connect(":memory:")

    # should have zero tables at first
    self.assertEqual(len(db.list_tables()), 0)

    # once we create our first, we should have exactly one
    db.create_table("players", ("name", str), ("age", int))    
    self.assertEqual(len(db.list_tables()), 1)

    # make sure the table exists
    self.assertTrue(db.table_exists("players"))

    # this should cause an error
    db.create_table("players", ("field_one", str), ("field_two", int))

    # manually use SQL syntax to add a row
    db.insert("players", name='roobiki', age=40)

    # manually use SQL syntax to view the table
    db.execute("SELECT * FROM players")
    r = db_result.db_result.from_dict(dict(db.fetch_one()))
    print(r)

    

if __name__ == "__main__":
  unittest.main()