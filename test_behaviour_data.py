import behaviour_data
import cmd_trigger_data
import heartbeat_proc_data
import spec_proc_data
import unittest
from unittest import mock

class TestBehaviourData(unittest.TestCase):
  def test_constructor(self):
    test_behave = behaviour_data.behaviour_data()

  def test_assign(self):

    def f(arg1, arg2):
      return

    mock_spec1 = mock.Mock(spec=heartbeat_proc_data.heartbeat_proc_data)
    mock_spec1.name.return_value = "mock heartbeat proc"
    mock_spec1.func.return_value = f
    mock_spec1.args.return_value = heartbeat_proc_data.heartbeat_proc_data.expected_args

    test_behave = behaviour_data.behaviour_data()

    test_behave.assign_spec_proc(mock_spec1)

    self.assertTrue(isinstance(mock_spec1, heartbeat_proc_data.heartbeat_proc_data))

if __name__ == "__main__":
  unittest.main()