from color import *
import logging
import re

def ana(noun):
  if noun[0].lower() in ['a', 'e', 'i', 'o', 'u']:
    return "an"
  else:
    return "a"

def alpha_under_score(str):
  for c in str:
    if not c.isalpha() and c != '_':
      return False
  return True

def alpha_num_under_score(str):
  for c in str:
    if not c.isalnum() and c != '_':
      return False
  return True

def alpha_num_space(str):
  for c in str:
    if not c.isalnum() and c != ' ':
      return False
  return True

def ordinal(n):
  first_digit = n % 10
  if first_digit == 1:
    suffix="st"
  elif first_digit == 2:
    suffix="nd"
  elif first_digit == 3:
    suffix="rd"
  else:
    suffix="th"
  return f"{n}{suffix}"

def oxford_comma(words):
  if len(words) == 0:
    return None
  elif len(words) == 1:
    return words[0]
  elif len(words) == 2:
    return f"{words[0]} and {words[1]}"
  else:
    return ', '.join(words[:-1]) + ', and ' + words[-1]

# check if a vref str is a valid internal code, like a room within a zone
# so if valid_id('zn') and valid_id('rm') both return True, then 'zn[rm]'
# is a sensible full identifier
def valid_id(str):
  return alpha_num_under_score(str)

def strip_tags(str):
  pattern = re.compile(r'<c(\d{1,2})>')
  match = re.search(pattern, str)
  
  while match != None:
    x = match.span()[0]
    y = match.span()[1]
    str = str[:x] + str[y:]
    match = re.search(pattern, str)

  pattern = re.compile(r'</?p>')
  match = re.search(pattern, str)

  while match != None:
    x = match.span()[0]
    y = match.span()[1]
    str = str[:x] + str[y:]
    match = re.search(pattern, str)

  return str

# inputs a string of space-delimited words, and prints them as paragraph
# with specified width and optional indent
#
# Notes:
#   * Anything that is not an explicit space will be assumed to be part
# of a word, including line breaks and punctuation.
#   * If the first word is wider than the specified width, indent is ignored.
def paragraph(text, width, indent=False):
  words = text.split(' ')
  line_length = 0
  par = ""

  if indent:
    line_length += 2
    par += "  "

  for idx, word in enumerate(words):
    # if there are extra spaces in text, words will contain null strings
    if word == '':
      continue

    # it fits perfectly
    if line_length + len(strip_tags(word)) == width:
      par += word

      # are we done?
      if idx == len(words) - 1:
        return par

      # if not, start over on the next line
      line_length = 0
      par += '\r\n'

    # it fits with room to spare
    elif line_length + len(strip_tags(word)) < width:
      # add the word, and a space afterwards
      line_length += len(strip_tags(word)) + 1
      par += word + ' '

    # line is empty and it still doesn't fit
    elif line_length == 0 and len(strip_tags(word)) > width:
      # add the word anyway
      line_length += len(strip_tags(word)) + 1
      par += word + ' '

    # at initial indent and the first word doesn't fit
    elif par == '  ' and 2 + len(strip_tags(word)) > width:
      # delete the indent and write the word anyway
      line_length = len(strip_tags(word)) + 1
      par = word + ' '

    # it doesn't fit, so start a new line
    else:
      line_length = len(strip_tags(word)) + 1
      par = f"{par[:-1]}\r\n{word} "

  return par.rstrip()

# used to read files in lib/
# should be deprecated since we now use sql
# def split_tag_value(line):
#   var_list = line.split()
#   return var_list[0], " ".join(var_list[1:])

def parse_reference(code):
  # if its just a local reference, put the zone_id to None
  if valid_id(code):
    return None, code

  # otherwise, we'd better find [] brackets
  n = code.find('[')

  # if not, then it's a broken global reference
  if n == -1 or code[-1] != ']':
    return None, None

  # otherwise the format is good
  zone_id = code[:n]
  id = code[n+1:-1]

  # one last check
  if valid_id(zone_id) and valid_id(id):
    return zone_id, id

  return None, None

def proofread(paragraph):
  # find first . or ? or !
  # then grab all subsequent . ? !
  # bundle them together as a terminator to a sentence
  # format the preceding sentence and capitalize the beginning
  # repeat
  pass

# returns a cleaned up version of "Hello , how are     you guys ?"
def proofread2(paragraph):

  formatted = ""

  lines = paragraph.split(' ')

  begin_sentence = True

  for idx, word in enumerate(lines):

    word = word.strip()

    if word == '':
      continue

    if word in {'.', '?', '!'}:
      formatted += word + ' '
      begin_sentence = True
      continue
    elif word == ',':
      formatted += ','
      continue

    if begin_sentence:
      formatted += word.capitalize()
      begin_sentence = False
    else:
      formatted += ' ' + word

    if word[-1:] in {'.', '?', '!'}:
      formatted += ' '
      begin_sentence = True

  return formatted.rstrip()

def yesno(flag):
  if flag == True:
    return 'yes'
  return 'no'

def tidy_color_tags(line):
  tidy = False

  # first push all color tags forward to the next word
  while True:
    pattern = re.compile(r' (<c\d+>) ')
    match = re.search(pattern, line)

    if match == None:
      break

    line = line.replace(f"{match.group(0)}", f"  {match.group(1)}")

  # then pull the last one backwards if necessary
  while True:
    pattern = re.compile(r' (<c\d+>)$')
    match = re.search(pattern, line)

    if match == None:
      break

    line = line.replace(f"{match.group(0)}", f"{match.group(1)}")
  return line

def proc_color_codes(line):
  for j in range(0,256):
    line = line.replace(f'<c{j}>', ansi_color_sequence(j))
  return line



if __name__ == '__main__':
  str = "Hello <c333> world! <c0>    OK Bye\r\n" + "Hi <c12> again <c0> ok finally bye bye.      <c3>"
  str = tidy_color_tags(str)
  print(str)

