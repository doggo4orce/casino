import behaviour_data
import cmd_trig_data
import hbeat_proc_data
import spec_proc_data
import unittest

class TestBehaviourData(unittest.TestCase):
  def test_assign(self):
    hbeat_proc_data.hbeat_proc_data.expected_args = ['a','b','c']

    # applies to both prefix/suffix_cmd_trigs
    cmd_trig_data.cmd_trig_data.expected_args = ['a','b']

    def spec_proc_f(a,b):
      return a
    def prefix_cmd_trig_g(a,b):
      return b
    def suffix_cmd_trig_h(a,b):
      return a + b
    def hbeat_proc_q(a,b,c):
      return c

    spec_proc = spec_proc_data.spec_proc_data("general spec", spec_proc_f)
    prefix_cmd_trig = cmd_trig_data.prefix_cmd_trig_data("prefix cmd trig", prefix_cmd_trig_g)
    suffix_cmd_trig = cmd_trig_data.suffix_cmd_trig_data("suffix cmd trig", suffix_cmd_trig_h)
    hbeat_proc = hbeat_proc_data.hbeat_proc_data("heartbeat proc", hbeat_proc_q)

    bd = behaviour_data.behaviour_data()

    bd.assign_proc(spec_proc)
    bd.assign_proc(prefix_cmd_trig)
    bd.assign_proc(suffix_cmd_trig)
    bd.assign_proc(hbeat_proc)

    self.assertIn(prefix_cmd_trig, bd.prefix_cmd_trigs)
    self.assertIn(suffix_cmd_trig, bd.suffix_cmd_trigs)
    self.assertIn(hbeat_proc, bd.hbeat_procs)

    bd.remove_all_procs()

    self.assertNotIn(prefix_cmd_trig, bd.prefix_cmd_trigs)
    self.assertNotIn(suffix_cmd_trig, bd.suffix_cmd_trigs)
    self.assertNotIn(hbeat_proc, bd.hbeat_procs)
    

if __name__ == "__main__":
  unittest.main()