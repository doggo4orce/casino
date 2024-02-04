import spec_proc_data
import unittest

class TestSpecProc(unittest.TestCase):
  def test_spec_proc(self):

    def f(arg1,arg2):
      pass

    spec1 = spec_proc_data.spec_proc_data("baker complains", f)
    spec2 = spec_proc_data.spec_proc_data("dealer waves")

    self.assertEqual(spec1.name, "baker complains")
    self.assertEqual(spec2.name, "dealer waves")

    self.assertIs(spec1.func, f)
    self.assertEqual(spec2.func, None)

    self.assertEqual(spec1.num_args, 2)
    self.assertEqual(spec1.args, ['arg1', 'arg2'])

    self.assertIn("arg1", spec1.args)
    self.assertIn("arg2", spec1.args)

    self.assertFalse(spec1.check(1,2,3))
    self.assertFalse(spec2.check(1,2))

    # should cause error log since f expects two args
    spec1.call(1,2,3)

    # should cause error log since spec2 has no function
    spec2.call(1,2)

    self.assertFalse(spec1.consistent)
    self.assertFalse(spec2.consistent)

if __name__ == "__main__":
  unittest.main()