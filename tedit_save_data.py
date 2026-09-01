from color import *

class tedit_save_data:
  """original_name <- the name of the table before any edits
     name          <- new name, if name has been changed
     old_name      <- old name if we are changing the name of a column
     column        <- temporary storage for editing column
     columns       <- list of columns in the table
     create_column <- check if column is edited or new"""
  def __init__(self):
    self.original_name = None
    self.name = None
    self.old_name = None
    self.column = None
    self.columns = list()
    self.renamed_columns = dict()
    self.create_column = False

  def debug(self):
    ret_val = f"Original Name: {CYAN}{self.original_name}{NORMAL}\r\n"
    ret_val += "Columns:"
    for col in self.columns:
      ret_val += f"\r\n  {CYAN}{str(col)}{NORMAL}"
    ret_val += f"\r\nName: {CYAN}{self.name}{NORMAL}\r\n"
    ret_val += f"Column: {CYAN}{str(self.column)}{NORMAL}\r\n"
    ret_val += f"Renamed Columns:"
    for (key,value) in self.renamed_columns:
      ret_val += f"\r\n  {key} -> {value}"
    ret_val += f"\r\nCreate Column: {CYAN}{self.create_column}{NORMAL}\r\n"
    return ret_val