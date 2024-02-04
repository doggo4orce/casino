import spec_proc_data

class heartbeat_proc_data(spec_proc_data.spec_proc_data):
  """Heartbeat Procs are called once per heartbeat
     mud = the mud object
     me = the character or object to which the proc is attached
     db = the main database"""
  expected_args = ['mud', 'me', 'db']

  def __init__(self, name, func):
    super().__init__(name, func)
