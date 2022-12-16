import dataclasses
import enum
import logging
import string_handling

class format_instructions(enum.IntEnum):
  NORMAL = 0
  RED    = 1

  BEGIN_PARAGRAPH = 100
  END_PARAGRAPH   = 101

def get_tag_by_instruction(instruction):
  if instruction == format_instructions.BEGIN_PARAGRAPH:
    return 'p'
  elif instruction == format_instructions.END_PARAGRAPH:
    return '/p'
  elif instruction == format_instructions.NORMAL:
    return '@n'
  elif instruction == format_instructions.RED:
    return '@r'

def get_instruction_by_tag(tag):
  if tag == 'p':
    return format_instructions.BEGIN_PARAGRAPH
  elif tag == '/p':
    return format_instructions.END_PARAGRAPH
  elif tag == '@n':
    return format_instructions.NORMAL
  elif tag == '@r':
    return format_instructions.RED

# returns the triple (text1, tag, text2), where text1 is the
# text that precedes the next tag, and text2 is everything after the first tag
def peel_next_tag(str):
  count = 0

  pre_tag_str = ""
  tag_str = ""

  # find next open bracket index
  while True:
    open_bracket = str.find('<')

    if open_bracket == -1:
      break

    if str[open_bracket+1] == '<':
      pre_tag_str += str[:open_bracket + 1]
      str = str[open_bracket+2:]
      continue

    close_bracket = str.find('>')
    next_open_bracket = str.find('<')

    if close_bracket == -1:
      logging.warning("Ignoring lonely '<' wit missing '>' -- did you mean '<<'?")
      break

    if next_open_bracket < close_bracket:
      logging.warning("Ignoring lonely '<' wit missing '>' -- did you mean '<<'?")
      pre_tag_str += str[:next_open_bracket]
      str = str[next_open_bracket+1:]
      continue

    pre_tag_str += str[:open_bracket]
    str = str[open_bracket+1:]
    break


    

    
  if close_bracket == -1:
    logging.warning(f"Incomplete tag following: {pre_tag_str} -- did you mean '<<'?")
    return pre_tag_str + str, None, None

  tag_str = str[:close_bracket]

  # trim off the tag that we just found
  str = str[close_bracket+1:]

  return pre_tag_str, tag_str, str

# this function should just return a list of paragraphs separated into lines that havent been wrapped/indented yet
# then width/indent dont need to be passed as parameters
def process_tags(text, width, indent=False):
  next_paragraph = ""
  ret_val = ""

  # these may not even be needed, but since they sometimes are, it makes
  # sense to define them near the top of the function
  begin_ptag = get_tag_by_instruction(format_instructions.BEGIN_PARAGRAPH)
  end_ptag = get_tag_by_instruction(format_instructions.END_PARAGRAPH)
  
  while True:
    pre_tag_str, tag_str, post_tag_str = peel_next_tag(text)

    print(f"{pre_tag_str} {tag_str} {post_tag_str}")
    if tag_str == "":
      break

    instruction = get_instruction_by_tag(tag_str)
    
    if instruction == format_instructions.BEGIN_PARAGRAPH:

      # figure out where the </p> happens
      end_ptag_index = post_tag_str.find(end_ptag)
      if end_ptag_index == -1:
        logging.warning(f"tag {begin_ptag} occurs without {end_ptag}")
        ret_val += pre_tag_str + process_tags(post_tag_str, width, indent)
        break

      next_paragraph = string_handling.paragraph(text[:end_ptag_index - 1], width, indent)
      ret_val += pre_tag_str + process_tags(next_paragraph, width, indent) + "\r\n"
    elif instruction == format_instructions.NORMAL:
      ret_val += NORMAL
    elif instruction == format_instructions.RED:
      ret_val += RED
    else:
      logging.warning(f"Unrecognized tag: {tag_str}")

     
    pre_tag_str, tag_str, post_tag_str = peel_next_tag(post_tag_str)
 
  # copy over the last section of text that has no tags
  ret_val += text

  return ret_val

if __name__ == '__main__':

  lines = [
    "This returns to verbatim text:  (*)====+________________/",
    "<p>This is onext_instruction next_instruction next_instruction next_instruction next_instruction very long super long the longest super long",
    "long longidddy long dididily next _instr uctio nnext inst uctio next_ struc ionn xt_in truc ionne xt_inst uctio nex _instr uction"
    "long longidddy long dididily next _instr uctio nnext inst uctio next_ struc ionn xt_in truc ionne xt_inst uctio nex _instr uction"
    "long longidddy long dididily next _instr uctio nnext inst uctio next_ struc ionn xt_in truc ionne xt_inst uctio nex _instr uction</p>"
    "<p>This should be the start of",
    "a new paragraph, even though the first line was not that long.</p>",
    "This returns to verbatim text:  (*)====+________________/\n",
    "This returns to verbatim text:  (*)====+________________/"

  ]

  combined = ' '.join(lines)

  print(process_tags(combined, 60, True))