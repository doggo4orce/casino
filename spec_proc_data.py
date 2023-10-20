import inspect
import logging
import string_handling

# TODO (idea?): add 'behaviour' field to npc/npc_protos to manage the lists of spec_procs
class spec_proc_data:
  expected_args = []

  """name        = representation as a string
     func        = behaviour function, uses return value as message to nanny
     args        = list of args that func is expecting
     num_args    = number of args that func is expecting
     arg_problem = checks whether self.func accepts the correct parameters"""

  def __init__(self, name, func=None):
    self.name = name
    self.func = func

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
  def arg_problem(self):
    return self.arg_error() != None

  @name.setter
  def name(self, new_name):
    self._name = new_name
  @func.setter
  def func(self, new_func):
    self._func = new_func
    if self.func == None:
      logging.warning("spec_proc({self.name})")
      logging.warning("  has no function")
      return
    arg_error = self.arg_error_brief()
    if arg_error != None:
      logging.warning(f"spec_proc({self.name})")
      logging.warning(f"  arg error with function {self.func.__name__}")
      logging.warning(f"  {arg_error}")

  """arg_error()        <-- describe problems with function parameters in the form of a paragraph
     consistent()       <-- check whether self.args is consistent with self.expected_args
     check(*args)       <-- check whether args are appropriate for self.func
     call(*args)        <-- pass args to self.func"""
     
  def arg_error(self):
    ret_val = f"spec_proc({self.name})\r\n"
    # if no function, just say so
    if self.func == None:
      return "has no function"
    # otherwise, build error message
    ret_val += "  expected_args: "
    if len(self.expected_args) == 0:
      ret_val += "None\r\n"
    else:
      ret_val += f"{self.expected_args}\r\n"
    ret_val += f"  function_args: "
    if len(self.args) == 0:
      ret_val += "None\r\n"
    else:
      ret_val += f"{', '.join(self.args)}\r\n"
    # wrong number of arguments
    if len(self.expected_args) != len(self.args):
      return ret_val
    for idx, arg in enumerate(self.expected_args):
      if self.args[idx] != arg:
        return ret_val
    # no problem if we made it this far
    return None

  def consistent(self):
    return self.arg_error_brief() == None

  def check(self, *args):
    return self.arg_error_brief(*args) != None

  def call(self, *args):
    if self.func == None:
      logging.error(f"Error: spec_proc({self.name})")
      logging.error(f"  tried to call with no function")
      return

    try:
      return self.func(*args)
    except TypeError:
      logging.error(f"Error: spec_proc({self.name})")
      logging.error(f"  tried to call {self.func.__name__}")
      logging.error(f"  expecting args: {', '.join(self.args)}")
      logging.error(f"  was passed: {', '.join([str(arg) for arg in args])}")