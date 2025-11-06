import buffer_data
from color import *
import config
import dataclasses
import enum
import logging
import re
import string_handling

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
  /ra '<text1>' '<text2>' - all occurances"""

# returns True if the player is done writing
def editor_handle_input(d, input):
  if d.character:
    width = d.character.page_width
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
    d.write_buffer = buffer_data.buffer_data()
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

# TODO I've since written a buffer_data.split() function which can
# probably be called directly in this code
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
  new_buffer = buffer_data.buffer_data()
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
  buf = buffer.buffer("<p>This would a <c3>great<c0> place to catch up on news from the non-existent message board that should be here!  To the north is the entrance to a different zone.</p>")

  print(buf.display(width=60, indent=True, color=True))