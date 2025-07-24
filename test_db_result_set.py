import db_result
import db_result_set

import unittest

class TestDbResultSet(unittest.TestCase):
  def test_result_set(self):
    rs = db_result_set.db_result_set("name", "age")

    # can check the columns
    self.assertEqual(rs.columns, ["name", "age"])

    # add some results to the result set
    r1 = db_result.db_result(name="Kyle",age=40)
    r2 = db_result.db_result(name="Dylan",age=12)
    rs.add_result(r1)
    rs.add_result(r2)
    self.assertIn(r1, rs)
    self.assertIn(r2, rs)
    self.assertEqual(rs.num_results, 2)
    print(rs)

    # cannot add a result with the wrong fields
    r3 = db_result.db_result(nmae="bob",age=25)
    rs.add_result(r3)
    self.assertNotIn(r3, rs)
    self.assertEqual(rs.num_results, 2)

    # cannot add a result with the extra fields
    r4 = db_result.db_result(name="alice",age=30,height=5)
    rs.add_result(r4)
    self.assertNotIn(r4, rs)
    self.assertEqual(rs.num_results, 2)

    # delete a column
    rs.delete_column("age")
    print(rs)

    # add a column
    rs.add_column("age")
    rs.add_column("height")

    # now this should work
    rs.add_result(r4)

    print(rs[0])

if __name__ == "__main__":
  unittest.main()