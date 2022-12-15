import logging

def ana(noun):
  if noun[0].lower() in ['a', 'e', 'i', 'o', 'u']:
    return "an"
  else:
    return "a"

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
def valid_id(vref):
  valid = True

  for j in range(0, len(vref)):
    if not vref[j].isalnum() and vref[j] not in {'_'}:
      valid = False

  return valid

def essay(text, width, indent=False):
  k = text.find("<p>")
  ret_val = ""

  if k == -1:
    return paragraph(text, width, indent) + "\r\n"

  while k != -1:
    k2 = text[k+4:].find('</p>')
    if k2 == -1:
      logging.warning("<p> tag appeared without </p>")
      ret_val += paragraph(text, width, indent) + "\r\n"
      return ret_val
    else:
      ret_val += paragraph(text[k+4:][k2:], width, indent) + "\r\n"
      text = text[k+4:][k2+4:]
    
  return ret_val

def paragraph(text, width, indent=False):
  words = text.split(' ')
  line_length = 0
  par = ""

  if indent:
    line_length += 2
    par += "  "

  for idx, word in enumerate(words):
    # it fits perfectly
    if line_length + len(word) == width:
      par += word

      # are we done?
      if idx == len(words) - 1:
        return par

      # if not, start over on the next line
      line_length = 0
      par += '\r\n'

    # it fits with room to spare
    elif line_length + len(word) < width:
      # add the word, and a space afterwards
      line_length += len(word) + 1
      par += word + ' '

    # it doesn't fit, so start a new line
    else:
      line_length = len(word) + 1
      par += '\r\n' + word + ' '

  return par

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

def yesno(flag):
  if flag == True:
    return 'yes'
  return 'no'

def alpha_numeric_space(input):
  for j in range(0, len(input)):
    if input[j] != ' ' and not input[j].isalnum():
      return False
  return True


