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

class buffer:
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

  def clean_up(self):
    original = self.str(numbers=False)
    clean = ""
    first_search = True

    # group 0: the whole match
    # group 1: \r\n if match starts with \r\n, otherwise null
    # group 2: everything between paragraph tags
    # group 3: \r\n if match ends with \r\n, otherwise null

    pattern = re.compile(
      r'((?:\r\n)?){}((?:.*?(?:\r\n)?)*?){}((?:\r\n)?)'.format(
        OPEN_PARAGRAPH,
        CLOSE_PARAGRAPH)
    )

    while True:
      match = re.search(pattern, original)

      if match == None:
        clean += original
        break

      j = match.span()[0] # beginning of match
      k = match.span()[1] # beginning of suffix

      if first_search and j == 0:
        pre_line_break = ""
      else:
        pre_line_break = "\r\n"

      post_line_break = match.group(3)

      paragraph = match.group(2).replace('\r\n', ' ')

      clean += f"{original[:j]}{pre_line_break}{OPEN_PARAGRAPH}{paragraph}{CLOSE_PARAGRAPH}{post_line_break}"
      original = original[k:]

      first_search = False

    return buffer(clean)    

  def clean_up2(self):
    ret_val = buffer() # store the return value
    line_buf = ""      # store progress while building line
    par_buf = ""       # store progress while building paragraph

    for idx, line in self._contents:
      if not p_open:
        pattern = re.compile(OPEN_PARAGRAPH)
        match = re.search(pattern, line)

        if match == None:
          ret_val.add_line(line)
          continue

        j = match.span()[0] # beginning of match
        k = match.span()[1] # beginning of suffix

        # line[:j] <-- what we will add to ret_val if </p> isn't also in this line
        # line[k:] <-- what we will set p_buf to if it doesn't contain </p>

    return None

  def clean_up3(self):
    ret_val = buffer()
    p_buffer = ""
    p_open = False

    # go through one line at a time
    for line in self._contents:

      # ignore empty lines within a paragraph
      if p_open and line == "":
        continue

      while (True):
        # if we're in the middle of a paragraph, find out if it closes on this line
        if p_open:
          target = CLOSE_PARAGRAPH
        # if it doesn't, then find out if a paragraph opens on this line
        else:
          target = OPEN_PARAGRAPH

        # see if we find out target
        pattern = re.compile(target)
        match = re.search(pattern, line)

        # if not, then just carry on with whatever we're doing
        if match == None:
          # whether we are in the middle of a paragraph
          if p_open:
            p_buffer += line + " "
          # or recording verbatim text
          else:
            ret_val.add_line(line)
          break

        # TODO: peek ahead to make sure a CLOSE_PARAGRAPH is coming
        # otherwise, the OPEN_PARAGRAPH we just found should not be
        # touched. Feb 9, 7:47

        # but if we did find a match, start splicing
        else:
          x = match.span()[0]
          y = match.span()[1]

          # if our paragraph is open, then we found the closing tag
          if p_open:
            # so close the paragraph
            p_open = False

            # add the pre-tag string into the paragraph buffer
            p_buffer += line[:x]

            # now record the paragraph as a single line
            ret_val.add_line(f"{OPEN_PARAGRAPH}{p_buffer}{CLOSE_PARAGRAPH}")

            # and reset the buffer for the next one
            p_buffer = ""

          # otherwise we found an opening paragraph tag
          else:
            # so open the paragraph
            p_open = True

            # unless its the beginning of the line
            if x != 0:
              # add the pre-tag string as a verbatim line
              ret_val.add_line(line[:x])

          # get the post-tag string ready to be handled on the next iteration
          line = line[x + len(target):]

        if line == "":
          break

    return ret_val

  def display(self, width, format=True, indent=True, numbers=False, color=True):
    temp_buf = self.make_copy()
    final_buf = buffer()
    ret_val = ""

    if format:
      temp_buf = temp_buf.clean_up()

    for line in temp_buf:
      if format and (line[:len(OPEN_PARAGRAPH)] == OPEN_PARAGRAPH and line[(-1)*len(CLOSE_PARAGRAPH):] == CLOSE_PARAGRAPH):
        line = line[len(OPEN_PARAGRAPH):]
        line = line[:(-1)*len(CLOSE_PARAGRAPH)]
        line = string_handling.paragraph(line, width, indent)

      final_buf.add_line(line)

    ret_val = final_buf.str(numbers)

    if color:
      ret_val = string_handling.proc_color(line)

    return ret_val

  # def display2(self, width, format=True, indent=True, numbers=False, color=True):
  #   ret_val = ""
  #   buf = self.make_copy()

  #   if format:
  #     buf = buf.clean_up()

  #   for idx, line in enumerate(buf._contents):

  #     if format and (line[:len(OPEN_PARAGRAPH)] == OPEN_PARAGRAPH and line[(-1)*len(CLOSE_PARAGRAPH):] == CLOSE_PARAGRAPH):
  #       line = line[len(OPEN_PARAGRAPH):]
  #       line = line[:(-1)*len(CLOSE_PARAGRAPH)]
  #       line = string_handling.paragraph(line, width, indent)

  #     if color:
  #       line = string_handling.proc_color(line)

  #     if numbers:
  #       line = f"L{idx + 1}: " + line
      
  #     ret_val += line

  #     if idx != len(buf._contents) - 1:
  #       ret_val += "\r\n"

  #   return ret_val

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