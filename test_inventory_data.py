import inventory_data
import object_data

import unittest

class TestInventory(unittest.TestCase):
  def test_inventory(self):
    inv = inventory_data.inventory_data()

    obj1 = object_data.object_data()
    obj1.reset_aliases("small", "sword")

    obj2 = object_data.object_data()
    obj2.reset_aliases("hot", "lantern")

    inv.add_object(obj1)
    inv.add_object(obj2)

    self.assertEqual(len(inv), 2)

    self.assertEqual(obj1, inv.obj_by_alias("small"))
    self.assertEqual(obj1, inv.obj_by_alias("sword"))
    self.assertEqual(obj2, inv.obj_by_alias("hot"))
    self.assertEqual(obj2, inv.obj_by_alias("lantern"))

    inv.remove_object(obj1)

    self.assertIsNone(inv.obj_by_alias("small"))
    self.assertIsNone(inv.obj_by_alias("sword"))

    self.assertEqual(obj2, inv.obj_by_alias("hot"))

    print("should cause error message")
    inv.remove_object(obj1)

if __name__ == "__main__":
  unittest.main()