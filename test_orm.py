import orm
import unittest

class TestORM(unittest.TestCase):

  def test_record(self):
    r = orm.result()
    self.assertTrue(r.is_blank())

    r = orm.result(name="kyle", age=39)
    self.assertFalse(r.is_blank())
    self.assertTrue("name" in r.fields())
    self.assertTrue("age" in r.fields())
    self.assertEqual(r["name"], "kyle")
    self.assertEqual(r["age"], 39)
    self.assertEqual(r.num_fields(), 2)

    r.add_field("fav_drink", "bang")
    self.assertTrue("fav_drink" in r.fields())
    self.assertEqual(r["fav_drink"], "bang")
    self.assertEqual(r.num_fields(), 3)

    r.delete_field("age")
    self.assertFalse("age" in r.fields())
    self.assertEqual(r.num_fields(), 2)
    self.assertRaises(KeyError, r.__getitem__, "age",)

  def create_table(self):
    manager = orm.orm(":memory:")
    manager.create_table("employee", ("name", str), ("salary", int))
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
    