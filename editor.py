import config
import dataclasses
import enum
import logging
import re
import string_handling

class buffer:
  """a list of lines, used to keep organize raw and formatted input
     with the editor, but probably has other applications as well
     contents = the raw contents of buffer, one line at a time"""
  def __init__(self, str=None):
    self._contents = list()

  """num_lines()    <- returns number of lines in the buffer
     is_empty()     <- returns True is there aren't any lines in the buffer
     add_line()     <- adds a line to the buffer
     make_copy()    <- returns a new buffer with identical contents
     copy_from(buf) <- resets the contents to be identical from those of buf"""

  @property
  def num_lines(self):
    return len(self._contents)

  @property
  def is_empty(self):
    return self.num_lines == 0

  def add_line(self, line):
    self._contents.append(line)

  def make_copy(self):
    ret_val = buffer()
    for line in self._contents:
      ret_val.add_line(line)
    return ret_val

  def copy_from(self, source):
    self._contents = list()
    for line in source._contents:
      self.add_line(line)

  def __str__(self):
    ret_val = ""
    for line in self._contents:
      ret_val += line + "\r\n"
    return ret_val

  def __contains__(self, obj):
    return obj in self._contents

  def __iter__(self):
    return buffer_iterator(self)

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

class display_buffer:
  def __init__(self, str=None):
    self._raw = buffer()
    self._formatted = None

    if str != None:
      self._raw.add_line(str)

  @property
  def num_lines(self):
    return self._raw.num_lines + self._formatted.num_lines

  @property
  def is_formatted(self):
    return self._raw.is_empty

  def add_line(self, str):
    self._raw.add_line(str)

  def clear(sel):
    self._raw = display_buffer("")
    self._formatted = None

  def make_copy(self):
    ret_val = display_buffer()

    ret_val._raw = self._raw.make_copy()
    ret_val._formatted = None

    return ret_val

  def copy_from(self, source):
    self._raw.copy_from(source._raw)

  def proc_p_tags(self, width):
    self._formatted = buffer()
    p_buffer = ""
    p_open = False

    # go through one line at a time
    for line in self._raw:

      while (True):
        # if we're in the middle of a paragraph, find out if it closes on this line
        if p_open:
          target = r'</p>'
        # if it doesn't, then find out of a paragraph opens on this line
        else:
          target = r'<p>'

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
            self._formatted.add_line(line)
          break

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

            # then record the paragraph as a single line
            self._formatted.add_line(string_handling.paragraph(p_buffer, width, indent=True))

            # and reset the buffer for the next one
            p_buffer = ""

          # otherwise we found an opening paragraph tag
          else:
            # so open the paragraph
            p_open = True

            # unless its the beginning of the line
            if x != 0:
              # add the pre-tag string as a verbatim line
              self._formatted.add_line(line[:x])

          # get the post-tag string ready to be handled on the next iteration
          line = line[x + len(target):]

        if line == "":
          break

  def str(self, numbers=False):
    ret_val = ""

    for idx, line in enumerate(self._formatted):
      if numbers:
        ret_val += f"L{idx}: "
      ret_val += line + "\r\n"

    return ret_val

  def raw_str(self, numbers=False):
    ret_val = ""

    for idx, line in enumerate(self._raw):
      if numbers:
        ret_val += f"{idx}: "
      ret_val += line + "\r\n"

    return ret_val

if __name__ == '__main__':

  new_buf = display_buffer()

  new_buf.add_line("<p>Hi Dylan, I'm just writing to show you the awesome")
  new_buf.add_line("asd asdf asdf asdf asdf asdf asdf asdf asdf asdf asadf ok this")
  new_buf.add_line("sentence is erally long.")
  new_buf.add_line("you get the idea. now.  Check out")
  new_buf.add_line("my blue sword below.")
  new_buf.add_line("Oh right I forgot to close this paragraph as well. </p>-\\_(\")_/-<p>Now start a new")
  new_buf.add_line("paragraph but don't stop it until the next line at some point, so we can really find")
  new_buf.add_line("out whether our formatting is robust.</p>Ok it stopped on two lines later.")
  new_buf.add_line("(*) ==== +________________/  (*) ==== +________________/")
  new_buf.add_line("<p>The quick brown fox jumped over the lazy dog who was too busy chewing on his squeaky toys to notice.</p>")

  new_buf.proc_p_tags(width=50)

  print(new_buf.str(True))


