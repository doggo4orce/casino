import orm
import unittest

class TestORM(unittest.TestCase):

  def test_result_class(self):
    r = orm.result()
    self.assertTrue(r.is_blank)

    # constructor stores 2 fields correctly
    r = orm.result(name="kyle", age=39)
    self.assertIn("name", r)
    self.assertIn("age", r)
    self.assertIn("name", r.fields)
    self.assertIn("age", r.fields)
    self.assertEqual(r["name"], "kyle")
    self.assertEqual(r["age"], 39)
    self.assertEqual(r.num_fields, 2)

    # 2 manually added/changed fields work
    r["music"] = "rap"
    r.add_field("drink", "soda")
    self.assertIn("drink", r)
    self.assertIn("music", r)
    self.assertIn("drink", r.fields)
    self.assertIn("music", r.fields)
    self.assertEqual(r["drink"], "soda")
    self.assertEqual(r["music"], "rap")
    self.assertEqual(r.num_fields, 4)

    # 2 updated fields work
    r["drink"] = "monster"
    r.update_field("name", "dylan")
    self.assertEqual(r["name"], "dylan")
    self.assertEqual(r["age"], 39)
    self.assertEqual(r["drink"], "monster")
    self.assertEqual(r.num_fields, 4)

    # deleted fields are completely removed
    r.delete_field("age")
    self.assertNotIn("age", r)
    self.assertNotIn("age", r.fields)
    self.assertEqual(r.num_fields, 3)
    with self.assertRaises(KeyError):
      r["age"]

    # delete a field that doesn't exist
    with self.assertRaises(KeyError):
      r.delete_field("aeg")

    # iteration over r is equivalent to iterating over r.fields
    idx = 0
    with self.assertRaises(StopIteration):
      i = iter(r)
      while(True):
        field = next(i)
        self.assertEqual(field, r.fields[idx])
        idx += 1
    self.assertEqual(idx, r.num_fields)
    


  def test_column_class(self):
    c = orm.column("drink", str)
    self.assertEqual(c.name, "drink")
    self.assertEqual(c.type, str)
    self.assertEqual(c.sqlite3_type, "text")

    c = orm.column("food", "str")
    self.assertEqual(c.name, "food")
    self.assertEqual(c.type, str)
    self.assertEqual(c.sqlite3_type, "text")

    c = orm.column("name", "text")
    self.assertEqual(c.name, "name")
    self.assertEqual(c.type, str)
    self.assertEqual(c.sqlite3_type, "text")

    c = orm.column("age", int)
    self.assertEqual(c.name, "age")
    self.assertEqual(c.type, int)
    self.assertEqual(c.sqlite3_type, "int")

    c = orm.column("phone", "int")
    self.assertEqual(c.name, "phone")
    self.assertEqual(c.type, int)
    self.assertEqual(c.sqlite3_type, "int")

    c = orm.column("bad_column", "wef")
    self.assertEqual(c.name, "bad_column")
    self.assertEqual(c.type, None)
    self.assertEqual(c.sqlite3_type, None)

  def create_table(self):
    manager = orm.orm(":memory:")
    
    manager.create_table("employee", 
      ("name", str),
      ("salary", int)
    )

    manager.create_table("machine", ("name", str), ("model", int), ("brand", str))

    manager.create_table("badname!") # invalid name
    manager.create_table("goodname") # valid name but no columns 

    # employee table should have been created with 2 columns
    self.assertTrue(manager.table_exists("employee"))
    self.assertEqual(len(manager.list_columns("employee")), 2)

    # machine table should have been created with 3 columns
    self.assertTrue(manager.table_exists("machine"))
    self.assertEqual(len(manager.list_columns("machine")), 3)

    # these tables should not be created
    self.assertFalse(manager.table_exists("badname!"))
    self.assertFalse(manager.table_exists("goodname"))

  def insert(self):
    manager = orm.orm(":memory:")
    manager.create_table("score", ("first_name", str), ("last_name", str), ("score", int))
    #insert("score", first_name="kyle", last_name="bang", score=94000)
    