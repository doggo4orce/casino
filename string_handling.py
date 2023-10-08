from color import *
import logging
import re

def ana(noun):
  if noun[0].lower() in ['a', 'e', 'i', 'o', 'u']:
    return "an"
  else:
    return "a"

def only_alpha_and_under_score(str):
  for c in str:
    if not c.isalpha() and c != '_':
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
  valid = True

  for j in range(0, len(str)):
    if not str[j].isalnum() and str[j] not in {'_'}:
      valid = False

  return valid

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
  
def paragraph(text, width, indent=False):
  words = text.split(' ')
  line_length = 0
  par = ""

  if indent:
    line_length += 2
    par += "  "

  for idx, word in enumerate(words):
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

    # it doesn't fit, so start a new line
    else:
      line_length = len(strip_tags(word)) + 1
      par += '\r\n' + word + ' '

  return par.rstrip()

# used to read files in lib/
def split_tag_value(line):
  var_list = line.split()
  return var_list[0], " ".join(var_list[1:])

def parse_reference(code):
  # if its just a local reference, put the zone_id to None
  if code.isalnum():
    zone_id = None
    id = code
  # if it's a global reference, we'd better find [] brackets
  else:
    n = code.find('[')
    # if not, then it's a broken local reference
    if n == -1:
      zone_id = None
      id = None
    # syntax is correct for global reference
    else:
      zone_id = code[:n]
      id = code[n+1:-1]
  return zone_id, id

# returns a cleaned up version of "Hello , how are     you guys ?"
def proofread(paragraph):

  formatted = ""

  lines = paragraph.split(' ')

  begin_sentence = True

  for word in lines:

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

def alpha_numeric_space(input):
  for j in range(0, len(input)):
    if input[j] != ' ' and not input[j].isalnum():
      return False
  return True

if __name__ == '__main__':
  str = "Hello <c333> world! <c0>    OK Bye\r\n" + "Hi <c12> again <c0> ok finally bye bye.      <c3>"
  str = tidy_color_tags(str)
  print(str)

