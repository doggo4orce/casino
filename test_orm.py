import orm
import unittest

class TestORM(unittest.TestCase):

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

if __name__ == "__main__":
  unittest.main()
    