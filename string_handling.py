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
# so if valid_id('zn') and valid_id('rm') both return True, then 'rm@zn'
# is a sensible vref
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

def parse_reference(vref):
  # first find '@'
  codes = vref.split('@')

  # first check for local reference
  if len(codes) == 1 and valid_id(vref):
    return vref, None
  # otherwise there should be one '@'
  elif len(codes) != 2:
    return None, None

  # make sure codes are valid
  if not (valid_id(codes[0]) and valid_id(codes[1])):
    return None, None

  # codes[0] = local, codes[1] = global
  return codes[0], codes[1]

def parse_reference_old(code):
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

# returns a cleaned up version of "Hello , how are     you guys ?"
def proofread(paragraph):

  NUM_SPACES_AFTER_PUNCTUATION = 2

  formatted = ""

  lines = paragraph.split(' ')

  begin_sentence = True

  # clean up capitalization, commas, and periods
  for idx, word in enumerate(lines):
    word = word.strip()

    terminal_punct = {'.', '?', '!'}

    if word == '':
      continue

    if word in terminal_punct:
      formatted += word + ' '*NUM_SPACES_AFTER_PUNCTUATION
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

    if word[-1:] in terminal_punct:
      formatted += ' '
      begin_sentence = True

  # clean up trailing punctuation
  while True:
    pattern = re.compile(r' ([,.!?])')
    match = re.search(pattern, formatted)

    if match == None:
      break

    # formatted = formatted.replace(
    #   f"{match.group(1)} {match.group(2)}",
    #   f"{match.group(1)}{match.group(2)}"
    # )
    formatted = formatted.replace(match.group(0), match.group(1))

  return formatted.rstrip()

def yesno(flag):
  if flag == True:
    return 'yes'
  elif flag == False:
    return 'no'

def tidy_color_tags(line):
  tidy = False

  # first push all color tags forward to the next word
  while True:
    pattern = re.compile(r' ((?:<c\d+>)+) ')
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

    line = line.replace(match.group(0), f"{match.group(1)} ")

  # now delete any redundant color tags
  while True:
    pattern = re.compile(r'(?:<c\d+>)+( *<c\d+>)')
    match = re.search(pattern, line)

    if match == None:
      break

    line = line.replace(match.group(0), match.group(1))

  return line

def proc_color(line):
  for j in range(0,256):
    line = line.replace(f'<c{j}>', ansi_color_sequence(j))
  return line

