import dataclasses
import enum
import logging
import string_handling

class format_instructions(enum.IntEnum):
  BEGIN_PARAGRAPH = 1
  END_PARAGRAPH   = 2

def get_tag_by_instruction(instruction):
  if instruction == format_instructions.BEGIN_PARAGRAPH:
    return 'p'
  elif instruction == format_instructions.END_PARAGRAPH:
    return '/p'

def get_instruction_by_tag(tag):
  if tag == 'p':
    return format_instructions.BEGIN_PARAGRAPH
  elif tag == '/p':
    return format_instructions.END_PARAGRAPH

# returns the 2-ple (text, tag), where text is the 
# value of the first tag, and text is the remainder of the parameter str after
# the first tag has been peeled off
def peel_next_tag(str):
  k1 = str.find('<')

  if k1 == -1:
    return None, None

  k2 = str.find('>')

  if k2 == -1:
    logging.warning(f"Incomplete tag found: {str[k1:k1+15]}")
    return None, None

  next_tag = str[k1+1:k2]

  return k2+1, next_tag

# this funciton should just return a list of paragraphs separated into lines that havent been wrapped/indented yet
# then width/indent dont need to be passed as parameters
def process_tags(str, width, indent=False):
  index, next_tag = peel_next_tag(str)

  next_paragraph = ""

  if get_instruction_by_tag(next_tag) == format_instructions.BEGIN_PARAGRAPH:
    # find specific tag /p
    str = str[index:]
    close_tag = str.find(get_tag_by_instruction(format_instructions.END_PARAGRAPH))
    next_paragraph = string_handling.paragraph(str[:close_tag], width, indent)
    return process_tags(next_paragraph, width, indent) + "\r\n" + process_tags(str[close_tag+4:], width, indent)
  else:
    return str

if __name__ == '__main__':

  lines = [
    "<p>Hello world.  This is a new",
    "document.  How should it be organized",
    "into paragraphs?</p>", 
    "<p>This should be the start of",
    "a new paragraph, even though the first line was not that long.</p>",
    "ASDF     d       d       d        d      d"
  ]

  combined = ' '.join(lines)

  print(process_tags(combined, 40, True))