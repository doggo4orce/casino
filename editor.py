from color import *
import config
import dataclasses
import enum
import logging
import re
import string_handling

OPEN_PARAGRAPH  = "<p>"
CLOSE_PARAGRAPH = "</p>"

class buffer:
  """Used to keep organize editor input for writing rooms, messages, etc.
     contents = the raw contents of buffer, one line at a time"""
  def __init__(self, str=None):
    self._contents = list()

    if str != None:
      lines = str.split('\n')
      
      for line in lines:
        self._contents.append(line.strip('\r'))

  """add_line()            <- adds a line to the buffer
     insert_line(idx, str) <- adds a line in position idx and re-orders if necessary
     delete_line(idx)      <- deletes the line and re-orders
     clear()               <- empty self._contents
     make_copy()           <- returns a new buffer with identical contents
     copy_from(buf)        <- resets the contents to be identical from those of buf
     display(width)        <- returns buffer as string formatted to width.
     clean_up()            <- returns lines with paragraphs tidied up, optionally fix typos
     str()                 <- converts to string
     preview(max_len)      <- shows up to the first max_len chars of first line"""

  def __getitem__(self, key):
    return self._contents[key]

  def __setitem__(self, key, value):
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

  def make_copy(self):
    ret_val = buffer()
    for line in self._contents:
      ret_val.add_line(line)
    return ret_val

  def copy_from(self, buffer):
    self.clear()
    for line in buffer._contents:
      self.add_line(line)

  def display(self, width, format=True, indent=True, numbers=False, color=True):
    ret_val = ""
    buf = self.make_copy()

    if format:
      buf = buf.clean_up()

    for idx, line in enumerate(buf._contents):
      if line[:len(OPEN_PARAGRAPH)] == OPEN_PARAGRAPH and line[(-1)*len(CLOSE_PARAGRAPH):] == CLOSE_PARAGRAPH:
        line = line[len(OPEN_PARAGRAPH):]
        line = line[:(-1)*len(CLOSE_PARAGRAPH)]
        line = string_handling.paragraph(line, width, indent)

      if color:
        line = string_handling.proc_color_codes(line)

      if numbers:
        line = f"L{idx + 1}: " + line
      
      ret_val += line

      if idx != len(buf._contents) - 1:
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

EDITOR_HELP_STR = """Editor Commands
---------------------------------------------------
  /c                      - clear current buffer    
  /h                      - bring up this menu      
  /l                      - show unformatted buffer 
  /n                      - /l but with line numbers
  /f                      - merge multi-line paragraphs
  /p#                     - proofread line (paragraph only)
  /i#                     - insert before line #
  /d#                     - delete line #
  /x# '<text>'            - split line # at text
  /r '<text1>' '<text2>'  - replace text1 with text2
  /ra '<text1>' '<text2>' - all occurances
"""

# returns True if the player is done writing
def editor_handle_input(d, input):
  if d.char:
    width = d.char.screen_width
  else:
    width = config.DEFAULT_SCREEN_WIDTH

  if input == "":
    d.write_buffer.add_line(input)
  elif input == "/a":
    d.write("Aborting edit.\r\n")
    d.stop_writing(save=False)
    return True
  elif input == "/c":
    d.write("Buffer cleared.\r\n")
    d.write_buffer = buffer()
  elif input[:2] == "/d":
    editor_delete_line(d, input[2:])
  elif input == "/f":
    d.write("Merging separated paragraphs.\r\n")
    d.write_buffer = d.write_buffer.clean_up()
  elif input == "/h":
    d.write(EDITOR_HELP_STR)
  elif input[:2] == "/i":
    editor_insert_line(d, input[2:])
  elif input == "/l":
    d.write(d.write_buffer.str(numbers=False))
  elif input == "/n":
    d.write(d.write_buffer.str(numbers=True))
  elif input[:2] == "/p":
    editor_proofread_line(d, input[2:])
  elif input[:3] == "/ra":
    editor_find_replace_text(d, input[3:], replace_all=True)
  elif input[:2] == "/r":
    editor_find_replace_text(d, input[2:], replace_all=False)
  elif input == "/s":
    d.write("Saving buffer.\r\n")
    d.stop_writing(save=True)
    return True
  elif input[:2] == "/x":
    editor_split_line(d, input[2:])
  elif input[0] == "/" and len(input) > 1:
    d.write(f"Unrecognized command: {input[1]}\r\n")
  else:
    d.write_buffer.add_line(input)

  return False

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

  d.write(f"Splitting line #{line_num} at '{target}'.")
  d.write_buffer.delete_line(line_num - 1)
  d.write_buffer.insert_line(line_num - 1, second_half)
  d.write_buffer.insert_line(line_num - 1, first_half)

def editor_proofread_line(d, proofread):
  pattern = re.compile(r'(\d+)')
  match = re.search(pattern, proofread)
  if match == None:
    d.write("Proofread which line?")
    return
  line_num = int(match.group(1))

  if line_num < 1 or line_num > d.write_buffer.num_lines + 1:
    d.write(f"There is no line #{line_num}.\r\n")
    return

  d.write(f"Proofreading line #{line_num}.\r\n")
  line = d.write_buffer[line_num - 1]

  if line[:len(OPEN_PARAGRAPH)] == OPEN_PARAGRAPH and line[(-1)*len(CLOSE_PARAGRAPH):] == CLOSE_PARAGRAPH:
    line = line[len(OPEN_PARAGRAPH):]
    line = line[:(-1)*len(CLOSE_PARAGRAPH)]

  line = string_handling.tidy_color_tags(line)
  line = string_handling.proofread(line)

  d.write_buffer[line_num - 1] = OPEN_PARAGRAPH + line + CLOSE_PARAGRAPH

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
  new_buffer = buffer()
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
    for line in d.write_buffer:
      new_buffer.add_line(line.replace(old_text, new_text))
  else:
    for line in d.write_buffer:
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

if __name__ == '__main__':
  buf = buffer("<p>This would a <c3>great<c0> place to catch up on news from the non-existent message board that should be here!  To the north is the entrance to a different zone.</p>")

  print(buf.display(width=60, format=True, indent=True, color=True))