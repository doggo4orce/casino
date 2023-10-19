import inspect
import string_handling

# TODO (idea?): add 'behaviour' field to npc/npc_protos to manage the lists of spec_procs
class spec_proc_data:
  expected_args = []

  """name      = representation as a string
     func      = behaviour function, uses return value as message to nanny
     args      = list of args that func is expecting
     num_args  = number of args that func is expecting
     arg_error = checks whether self.func accepts the correct parameters"""

  def __init__(self, name, func):
    self.name = name
    self.func = fn

  @property
  def name(self):
    return self._name
  @property
  def func(self):
    return self._func
  @property
  def args(self):
    return inspect.getfullargspec(self.func).args
  @property
  def num_args(self):
    return len(self.args)
  @property
  def arg_error(self):
    return self.arg_error_brief() != None

  @name.setter
  def name(self, new_name):
    self._name = new_name
  @func.setter
  def func(self, new_func):
    self._func = new_func

  """arg_error_brief()  <-- first disagreement between self.args and self.expected_args
     arg_error_full()   <-- same as above but with more context
     correct_fn_args()  <-- check whether self.args is consistent with self.expected_args"""
     
  def arg_error_brief(self):
    if self.expected_args == None and self.args != None:
      return f"found arg '{self.args[0]}' when no args were expected"
    for idx, arg in enumerate(self.expected_args):
      if self.args[idx] != arg:
        return f"expecting '{arg}' for {string_handling.ordinal(idx+1)} arg but found '{actual_args[idx]}'"
    return None

  def arg_error_full(self):
    arg_error = self.first_fn_arg_error_brief()
    problems = list()
    if arg_error != None:
      problems.append(f"Error: spec_proc({self.name})")
      problems.append(f"  arg error with self.func={self.func.__name__}")
      problems.append(f"  {arg_error}")
    return problems

  def correct_fn_args(self):
    return self.first_fn_arg_error_brief() == None