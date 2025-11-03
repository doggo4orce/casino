import spec_proc_data
import unittest

class TestSpecProc(unittest.TestCase):
  
  def test_spec_proc(self):
    spec_proc_data.spec_proc_data.expected_args = ["spec", "proc"]

    def sp_bad(arg1, arg2):
      return 1

    def sp_good(spec, proc):
      return 2

    spec_bad = spec_proc_data.spec_proc_data("spec proc bad", sp_bad)
    spec_good = spec_proc_data.spec_proc_data("spec proc good", sp_good)

    self.assertEqual(spec_bad.name, "spec proc bad")
    self.assertEqual(spec_good.name, "spec proc good")

    self.assertEqual(spec_bad.func, sp_bad)
    self.assertEqual(spec_good.func, sp_good)

    self.assertFalse(spec_bad.check("x", "y"))
    self.assertTrue(spec_bad.check("arg1", "arg2"))

    self.assertFalse(spec_good.check("x", "y"))
    self.assertTrue(spec_good.check("spec", "proc"))

    self.assertFalse(spec_bad.consistent)
    self.assertTrue(spec_good.consistent)

if __name__ == "__main__":
  unittest.main()