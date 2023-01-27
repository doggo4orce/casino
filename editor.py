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

  """num_lines()           <- returns number of lines in the buffer
     is_empty()            <- returns True is there aren't any lines in the buffer
     add_line()            <- adds a line to the buffer
     insert_line(idx, str) <- adds a line in position idx and re-orders if necessary
     delete_line(idx)      <- deletes the line and re-orders
     clear()               <- empty self._contents
     make_copy()           <- returns a new buffer with identical contents
     copy_from(buf)        <- resets the contents to be identical from those of buf
     display(width)        <- returns buffer as string formatted to width.
                              optional flags: format, indent, numbers
     clean_up()            <- merge paragraphs spread across multiple lines
     str(numbers)          <- converts to string, with optional line numbers"""

  def __getline__(self, key):
    return self._contents[key]

  def __setline__(self, key, value):
    self._contents[key] = value

  @property
  def num_lines(self):
    return len(self._contents)

  @property
  def is_empty(self):
    return self.num_lines == 0

  def add_line(self, line):
    self._contents.append(line)

  def insert_line(self, idx, line):
    if idx < 0 or idx > self.num_lines:
      return

    # we can insert before the line after our last line
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

  def make_copy(self):
    ret_val = buffer()
    for line in self._contents:
      ret_val.add_line(line)
    return ret_val

  def copy_from(self, buffer):
    self.clear()
    for line in buffer._contents:
      self.add_line(line)

  def display(self, width, format=True, indent=True, numbers=False):
    ret_val = ""

    if format:
      lines = self.clean_up()
    else:
      lines = self

    for idx, line in enumerate(lines):
      if line[:3] == '<p>' and line[-4:] == '</p>':
        line = line[3:]
        line = line[:-4]
        ret_val += string_handling.paragraph(line, width, indent)
      else:
        ret_val += line

      if numbers:
        ret_val = f"L{idx + 1}: " + ret_val
      ret_val += "\r\n"

    return ret_val

  def clean_up(self):
    ret_val = buffer()
    p_buffer = ""
    p_open = False

    # go through one line at a time
    for line in self._contents:

      while (True):
        # if we're in the middle of a paragraph, find out if it closes on this line
        if p_open:
          target = r'</p>'
        # if it doesn't, then find out if a paragraph opens on this line
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
            ret_val.add_line(line)
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
            ret_val.add_line(f"<p>{p_buffer}</p>")

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

  def str(self, numbers=False):
    ret_val = ""
    for idx, line in enumerate(self._contents):
      if numbers:
        ret_val += f"L{idx+1}: "
      ret_val += line + "\r\n"
    return ret_val

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

class display_buffer:
  def __init__(self, str=None):
    self._raw = buffer()

    if str != None:
      self._raw.add_line(str)

  def __getitem__(self, key):
    return self._raw[key]
  def __setitem__(self, key, value):
    self._raw[key] = value

  @property
  def raw(self):
    return self._raw
  @property
  def num_lines(self):
    return self.raw.num_lines

  def add_line(self, str):
    self._raw.add_line(str)

  def insert_line(self, idx, str):
    self._raw.insert_line(idx, str)

  def delete_line(self, idx):
    self._raw.delete_line(idx)

  def clear(self):
    self._raw.clear()

  def make_copy(self):
    ret_val = display_buffer()

    ret_val._raw = self.raw.make_copy()

    return ret_val

  def copy_from(self, source):
    self._raw.copy_from(source._raw)

  def clean_up(self):
    self._raw = self._raw.clean_up()

  def display(self, width, format=True, indent=True, numbers=False):
    return self.raw.display(width, format, indent, numbers)

  def str(self, numbers=False):
    return self.raw.str(numbers)

def editor_split_line(d, split):
  pattern = re.compile(r'(\d+) \'(.*)\'')
  match = re.search(pattern, split)

  if match == None:
    d.write("Split which line number?\r\n")
    return


  line_num = int(match.group(1))
  target = match.group(2)
  if line_num < 1 or line_num > d.write_buffer.num_lines:
    d.write(f"There is no line #{line_num}.\r\n")
    return

  if target == '':
    d.write(f"Split line #{line_num} at which text?\r\n")
    return
  
  k = d.write_buffer[line_num - 1].find(target)
  first_half = d.write_buffer[line_num - 1][:k]
  second_half = d.write_buffer[line_num - 1][k:]

  d.write_buffer.delete_line(line_num - 1)
  d.write_buffer.insert_line(line_num - 1, second_half)
  d.write_buffer.insert_line(line_num - 1, first_half)

def editor_insert_line(d, insert):
  pattern = re.compile(r'(\d+) (.*)')
  match = re.search(pattern, insert)
  if match == None:
    d.write("Insert before which line number?\r\n")
    return
  line_num = int(match.group(1))
  line = match.group(2)

  if line_num < 1 or line_num > d.write_buffer.num_lines + 1:
    d.write(f"There is no line #{line_num}.\r\n")
    return

  if line_num == d.write_buffer.num_lines + 1:
    d.write_buffer.add_line(line)
    return

  d.write_buffer.insert_line(line_num - 1, line)
  d.write(f"Inserting '{line}' before line #{line_num}.\r\n")

def editor_delete_line(d, delete):
  pattern = re.compile(r'(\d+)')
  match = re.search(pattern, delete)
  if match == None:
    d.write("Delete which line number?\r\n")
    return
  line_num = int(match.group(1))
  if line_num < 1 or line_num > d.write_buffer.num_lines:
    d.write(f"There is no line #{line_num}.\r\n")
    return
  d.write_buffer.delete_line(line_num - 1)
  d.write(f"Deleting line {line_num}.\r\n")

def editor_find_replace_text(d, replace, replace_all=False):
  found_target = False
  replace_complete = False
  num_replaced = 0
  new_buffer = display_buffer()
  pattern = re.compile(r'\'(.+)\' \'(.+)\'')
  match = re.search(pattern, replace)

  if match == None:
    d.write("Perform a find/replace using the syntax:\r\n/r 'old text' 'new text'")
    return

  full_input = match.group(0)
  old_text = match.group(1)
  new_text = match.group(2)

  if replace_all:
    d.write(f"Replacing all occurances of '{old_text}' with '{new_text}'.")
    for line in d.write_buffer._raw:
      new_buffer.add_line(line.replace(old_text, new_text))
  else:
    for line in d.write_buffer._raw:
      # once replace_complete flag is set, simply copy the rest without changing anything
      if replace_complete or old_text not in line:
        new_buffer.add_line(line)
      else:
        new_buffer.add_line(line.replace(old_text, new_text, 1))
        replace_complete = True

    # once we're done, report once if we were successful with a single replacement
    if replace_complete:
      d.write(f"Replacing one occurance of '{old_text}' with '{new_text}'.")

  d.write_buffer = new_buffer

# all implemented except /r
EDITOR_HELP_STR = """Editor Commands
---------------------------------------------------
  /c                      - clear current buffer    
  /h                      - bring up this menu      
  /l                      - show unformatted buffer 
  /n                      - /l but with line numbers
  /f                      - format paragraphs  
  /i#                     - insert before line #
  /d#                     - delete line #
  /x# '<text>'            - split line # at text
  /r '<text1>' '<text2>'  - replace text1 with text2
  /ra '<text1>' '<text2>' - all occurances
"""

# returns True if the player is done writing
def editor_handle_input(d, input):
  if d.char:
    width = d.char.prefs.screen_width
  else:
    width = config.DEFAULT_SCREEN_WIDTH

  # put this check first so that all other checks may assume index[0] exists
  if input == "":
    d.write_buffer.add_line(input)
  elif input == "/c":
    d.write("Buffer cleared.\r\n")
    d.write_buffer = display_buffer()
  elif input[:3] == "/ra":
    editor_find_replace_text(d, input[3:], replace_all=True)
  elif input[:2] == "/r":
    editor_find_replace_text(d, input[2:], replace_all=False)
  elif input[:2] == "/i":
    editor_insert_line(d, input[2:])
  elif input[:2] == "/d":
    editor_delete_line(d, input[2:])
  elif input[:2] == "/x":
    editor_split_line(d, input[2:])
  elif input == "/l":
    d.write(d.write_buffer.raw_str())
  elif input == "/f":
    d.write_buffer.clean_up()
  elif input == "/n":
    d.write(d.write_buffer.str(numbers=True))
  elif input == "/h":
    d.write(EDITOR_HELP_STR)
  elif input == "/a":
    d.write("Aborting edit.\r\n")
    d.stop_writing(save=False)
    return True
  elif input == "/s":
    d.write("Saving buffer.\r\n")
    d.stop_writing(save=True)
    return True
  elif input[0] == "/" and len(input) > 1:
    d.write(f"Unrecognized command: {input[1]}\r\n")
  else:
    d.write_buffer.add_line(input)

  return False

if __name__ == '__main__':

  new_buf = display_buffer()

  new_buf.add_line("<p>Hi Bob, I'm just writing to show you the awesome")
  new_buf.add_line("asd asdf asdf asdf asdf asdf asdf asdf asdf asdf asadf ok this")
  new_buf.add_line("sentence is erally long.")
  new_buf.add_line("you get the idea. now.  Check out")
  new_buf.add_line("my blue sword below.")
  new_buf.add_line("Oh right I forgot to close this paragraph as well. </p>-\\_(\")_/-<p>Now start a new")
  new_buf.add_line("paragraph but don't stop it until the next line at some point, so we can really find")
  new_buf.add_line("out whether our formatting is robust.</p>Ok it stopped on two lines later.")
  new_buf.add_line("Keep this line verbatim:")
  new_buf.add_line("(*) ==== +________________/  (*) ==== +________________/")
  new_buf.add_line("<p>The quick brown fox jumped over the lazy dog who was too busy chewing on his squeaky toys to notice.</p>")

  print(new_buf.display(50, True))


