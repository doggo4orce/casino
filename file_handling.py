import logging
import string_handling

"""This file is intended to include functions which are not attached to any
   specific class, but are designed for working directly with files in lib/"""

class FileHandlingError(Exception):
  pass

class TagError(FileHandlingError):
  """Exception raised by lib files, when tags are not formatted correctly."""
  def __init__(self, filename, number):
  	self.message = f"TagError: line {number} of '{filename}'"

def parse_generic(new_rno, rf):
  line_number = 0
  while True:
    line_number += 1
    line = rf.readline()
    # catches the end of the file
    if line == "":
      break
    # allows us to ignore comments and blank/empty lines
    if line == "\n" or line[0] == '#':
      continue
    # expecting a tag for sure
    tag, value = string_handling.split_tag_value(line)
    # if we don't get a tag this file is not formatted properly
    if tag[-1] != ":":
      print(line)
      raise TagError(f"{rf.name}", line_number)
    # remove the colon and convert to lowercase
    tag = tag[0:len(tag) - 1].lower()
    # ready to interpret the actual tag.  pass rf along as well in case
    # the specific file format indicates they need to read further
    new_rno.parse_tag(tag, value, rf)