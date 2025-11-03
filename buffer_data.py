import buffer_parser
from color import *
import config
import copy
import dataclasses
import enum
import logging
import re
import string_handling

OPEN_PARAGRAPH  = "<p>"
CLOSE_PARAGRAPH = "</p>"

class buffer_data:
  """[ITERABLE] Used to keep organize editor input for writing rooms, messages, etc.
     contents = the raw contents of buffer, one line at a time"""
  def __init__(self, str=None):
    self._contents = list()

    if str != None:
      lines = str.split('\r\n')
      
      self.add_lines(lines)

  def __getitem__(self, key):
    return self._contents[key]

  def __setitem__(self, key, value):
    self._contents[key] = value

  """Attributes:
     num_lines = returns line count
     is_empty = check if line count is zero"""

  @property
  def num_lines(self):
    return len(self._contents)

  @property
  def is_empty(self):
    return self.num_lines == 0

  """add_line(line)        <- adds line to buffer
     add_lines(lines)      <- adds lines to buffer
     insert_line(idx, str) <- adds a line in position idx and re-orders if necessary
     delete_line(idx)      <- deletes the line and re-orders
     clear()               <- empty self._contents
     copy_from(buf)        <- resets the contents to be identical from those of buf
     make_copy()           <- returns a new buffer with identical contents
     clean_up()            <- puts paragraphs on separate single lines
     display(width)        <- returns buffer as string formatted to width.
     str(numbers)          <- converts to string, called by __str__ with numbers=False
     preview(max_len)      <- shows up to the first max_len chars of first non-empty line"""

  def add_line(self, line):
    self._contents.append(line)

  def add_lines(self, lines):
    for line in lines:
      self.add_line(line)

  def insert_line(self, idx, line):
    if idx < 0 or idx > self.num_lines:
      return

    # this is equivalent to just adding a line
    if idx == self.num_lines:
      self.add_line(line)
      return

    leading = self._contents[:idx]
    leading.append(line)
    trailing = self._contents[idx:]

    self._contents = leading + trailing

  def delete_line(self, idx):
    if idx < 0 or idx > self.num_lines - 1:
      return

    self._contents = self._contents[:idx] + self._contents[idx+1:]

  def clear(self):
    self._contents = list()

  def copy_from(self, buffer):
    self._contents = copy.copy(buffer._contents)

  def make_copy(self):
    return copy.deepcopy(self)

  def split(self, l, c):
    temp = self[l]
    self.delete_line(l)
    self.insert_line(l, temp[c:])
    self.insert_line(l, temp[:c])

  def clean_up(self):
    parser = buffer_parser.buffer_parser()
    clean_buffer = parser.parse_string(self.str(numbers=False))
    return buffer_data(clean_buffer)

  # # note, use the split function written above
  # def pre_clean_up(self):
  #   buffer_string = self.str(numbers=False)
  #   clean = ""

  #   # look for any lines interupted by <p>
  #   pattern = re.compile(rf'([^\r\n]*{OPEN_PARAGRAPH}')

  #   while True:
  #     match = re.search(pattern, buffer_string)

  #     if match is None:
  #       clean += buffer_string
  #       break

  #     j = match.span()[0] # beginning of match
  #     k = match.span()[1] # immediately follows OPEN_PARAGRAPH

  #     # content before paragraph tag
  #     partial_line = match.group(1)

  #     clean += "{}{}{}".format(
  #       buffer_string[:j],
  #       "\r\n",
  #       OPEN_PARAGRAPH
  #     )

  # # TODO: add better documentation for this function
  # def clean_up(self):
  #   buffer_string = self.str(numbers=False)
  #   clean = ""

  #   # look for text enclosed with paragraph tags
  #   pattern = re.compile(rf'{OPEN_PARAGRAPH}([\s\S]*?){CLOSE_PARAGRAPH}')

  #   while True:
  #     match = re.search(pattern, buffer_string)

  #     if match is None:
  #       clean += buffer_string
  #       break

  #     j = match.span()[0] # beginning of match
  #     k = match.span()[1] # immediately follows CLOSE_PARAGRAPH

  #     # content between paragraph tags
  #     paragraph = match.group(1)

  #     clean += "{}{}{}{}".format(
  #       buffer_string[:j],
  #       OPEN_PARAGRAPH,
  #       string_handling.clean_up_paragraph(paragraph),
  #       CLOSE_PARAGRAPH,
  #     )

  #     # trim what was already processed
  #     buffer_string = buffer_string[k:]

  #   return buffer_data(clean)    

  def display(self, width, indent=True, numbers=False, color=True):
    temp_buf = self.make_copy()
    final_buf = buffer_data()
    ret_val = ""
    temp_buf = temp_buf.clean_up()

    for line in temp_buf:
      # print(f"Before paragraph check:\r\n[{line}]\r\n")
      if line[:len(OPEN_PARAGRAPH)] == OPEN_PARAGRAPH and line[(-1)*len(CLOSE_PARAGRAPH):] == CLOSE_PARAGRAPH:
        # print(f"Line: \r\n{line}\r\n passed paragraph check")
        line = line[len(OPEN_PARAGRAPH):(-1)*len(CLOSE_PARAGRAPH)]
        # print(f"After trimming:\r\n{line}\r\n")
        line = string_handling.paragraph(line, width, indent)
        # print(f"After formatting:\r\n{line}\r\n")

      final_buf.add_line(line)

    ret_val = final_buf.str(numbers)

    if color:
      ret_val = string_handling.proc_color(ret_val)

    return ret_val

  # TODO:  adjust this to use '\r\n'.join(self._contents)'
  def str(self, numbers=False):
    ret_val = ""
    for idx, line in enumerate(self._contents):
      if numbers:
        ret_val += f"L{idx+1}: "
      ret_val += line + "\r\n"
    # as long as we had at least one line, we have one too many \r\n
    if len(self._contents) > 0:
      ret_val = ret_val[:-2]
    return ret_val

  def preview(self, max_len):
    j = 0
    txt = ""

    if self.is_empty:
      return ""
    
    for line in self._contents:
      txt = string_handling.strip_tags(line)[:max_len]
      if txt != "":
        return txt
      
    return ""

  def __str__(self):
    return self.str(numbers=False)

  def __contains__(self, obj):
    return obj in self._contents

  def __iter__(self):
    return buffer_iterator(self)

  def __getitem__(self, key):
    return self._contents[key]

class buffer_iterator:
  def __init__(self, buffer):
    self._buffer = buffer
    self._index = 0

  def __next__(self):
    if self._index < len(self._buffer._contents):
      result = self._buffer._contents[self._index]
      self._index += 1
      return result
    raise StopIteration