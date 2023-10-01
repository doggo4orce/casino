import unittest
import database2

class TestORM(unittest.TestCase):

  def test_create_table(self):
    db = database2.database(":memory:")
    db.create_table("employee", ("name", str), ("salary", int))
    db.create_table("machine", ("name", str), ("model", int), ("brand", str))

    db.create_table("badname!") # invalid name
    db.create_table("goodname") # valid name but no columns 

    # employee table should have been created with 2 columns
    self.assertTrue(db.table_exists("employee"))
    self.assertEqual(len(db.list_columns("employee")), 2)

    # machine table should have been created with 3 columns
    self.assertTrue(db.table_exists("machine"))
    self.assertEqual(len(db.list_columns("machine")), 3)

    # these tables should not be created
    self.assertFalse(db.table_exists("badname!"))
    self.assertFalse(db.table_exists("goodname"))

  def test_insert(self):
    db = database2.database(":memory:")

    db.create_table("score", ("first_name", str), ("last_name", str), ("score", int))

    insert("score", first_name="kyle", last_name="bang", score=94000)
    