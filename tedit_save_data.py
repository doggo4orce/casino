from color import *

class tedit_save_data:
  def __init__(self):
  	self.original_name = None
  	self.name = None
  	self.columns = list()

  def debug(self):
  	ret_val = f"Name: {CYAN}{self.name}{NORMAL}\r\n"
  	ret_val += "Columns:"
  	for col in self.columns:
  	  ret_val += f"\r\n  {CYAN}{str(col)}{NORMAL}"
  	return ret_val