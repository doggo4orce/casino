import spec_proc_data
import unittest

class TestSpecProc(unittest.TestCase):
  def test_spec_proc(self):

    def f(arg1,arg2):
      pass

    spec = spec_proc_data.spec_proc_data("baker complains", f)

    self.assertEqual(spec.name, "baker complains")
    self.assertIs(spec.func, f)

    self.assertEqual(spec.num_args, 2)
    self.assertIn("arg1", spec.args)
    self.assertIn("arg2", spec.args)

if __name__ == "__main__":
  unittest.main()