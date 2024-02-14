import behaviour_data
import cmd_trig_data
import hbeat_proc_data
import spec_proc_data
import unittest

class TestBehaviourData(unittest.TestCase):
  def test_assign(self):

    def spec_proc_f(a,b):
      return a

    spec_proc = spec_proc_data.spec_proc_data("general spec", spec_proc_f)

    def prefix_cmd_trig_g(a,b):
      return b

    cmd_trig_data.cmd_trig_data.expected_args = ['a','b']
    prefix_cmd_trig = cmd_trig_data.prefix_cmd_trig_data("prefix cmd trig", prefix_cmd_trig_g)

    def suffix_cmd_trig_h(a,b):
      return a + b

    suffix_cmd_trig = cmd_trig_data.suffix_cmd_trig_data("suffix cmd trig", suffix_cmd_trig_h)

    def hbeat_proc_q(a,b,c):
      return c

    hbeat_proc_data.hbeat_proc_data.expected_args = ['a','b','c']
    hbeat_proc = hbeat_proc_data.hbeat_proc_data("heartbeat proc", hbeat_proc_q)

    test_behave = behaviour_data.behaviour_data()

    test_behave.assign(spec_proc)
    test_behave.assign(prefix_cmd_trig)
    test_behave.assign(suffix_cmd_trig)
    test_behave.assign(hbeat_proc)

    print(test_behave)

if __name__ == "__main__":
  unittest.main()