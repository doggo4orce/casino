import db_result

import unittest

class TestDbResult(unittest.TestCase):
  def test_result_class(self):
    # start with a blank result
    r = db_result.db_result()
    self.assertTrue(r.is_blank)

    # constructor stores 2 fields correctly
    r = db_result.db_result(name="kyle", age=40)
    self.assertEqual(r.num_fields, 2)

    # can check for containment in fields
    self.assertIn("name", r.fields)
    self.assertIn("age", r.fields)

    # or in the result itself
    self.assertIn("name", r)
    self.assertIn("age", r)
    self.assertNotIn("size", r)

    # entries can be accessed specifying fields as keys
    self.assertEqual(r["name"], "kyle")
    self.assertEqual(r["age"], 40)

    # may add fields manually after the fact
    r.add_field("drink", "soda")
    self.assertIn("drink", r)
    self.assertEqual(r["drink"], "soda")
    self.assertEqual(r.num_fields, 3)

    # and this may be done using keys as well
    r["music"] = "rap"
    self.assertIn("music", r)
    self.assertEqual(r["music"], "rap")
    self.assertEqual(r.num_fields, 4)

    # results have string representations same as dict()
    print(r.debug())

    # keys may be updated using a function call
    r.update_field("name", "dylan")
    self.assertEqual(r["name"], "dylan")

    # or using keys
    r["drink"] = "monster"
    self.assertEqual(r["drink"], "monster")

    # deleted fields are completely removed
    r.delete_field("age")
    self.assertNotIn("age", r)
    self.assertEqual(r.num_fields, 3)

    # KeyError raised if non-existant field is accessed or deleted
    with self.assertRaises(KeyError):
      r["age"]
    with self.assertRaises(KeyError):
      r.delete_field("age")

if __name__ == "__main__":
  unittest.main()