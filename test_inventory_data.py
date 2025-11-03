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

    self.assertEqual(inv[0], obj1)
    self.assertEqual(inv[1], obj2)

    self.assertEqual(len(inv), 2)

    self.assertEqual(obj1, inv.object_by_alias("small"))
    self.assertEqual(obj1, inv.object_by_alias("sword"))
    self.assertEqual(obj2, inv.object_by_alias("hot"))
    self.assertEqual(obj2, inv.object_by_alias("lantern"))

    inv.remove_object(obj1)

    self.assertIsNone(inv.object_by_alias("small"))
    self.assertIsNone(inv.object_by_alias("sword"))

    self.assertEqual(obj2, inv.object_by_alias("hot"))

    print("should cause error message")
    inv.remove_object(obj1)

  def test_transfer(self):
    inv = inventory_data.inventory_data()
    inv2 = inventory_data.inventory_data()

    obj1 = object_data.object_data()
    obj1.reset_aliases("small", "sword")

    obj2 = object_data.object_data()
    obj2.reset_aliases("hot", "lantern")

    obj3 = object_data.object_data()
    obj3.reset_aliases("steel", "mace")

    inv.add_object(obj1)
    inv.add_object(obj2)
    inv.add_object(obj3)

    inv.transfer_obj(obj2, inv2)

    self.assertNotIn(obj2, inv)
    self.assertIn(obj2, inv2)
    self.assertEqual(len(inv), 2)
    self.assertEqual(len(inv2), 1)

    inv.transfer_all(inv2)

    self.assertNotIn(obj1, inv)
    self.assertNotIn(obj3, inv)

    self.assertTrue(inv.empty())

    self.assertEqual(len(inv2), 3)

if __name__ == "__main__":
  unittest.main()