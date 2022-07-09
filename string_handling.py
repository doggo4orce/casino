def ana(noun):
  if noun[0].lower() in ['a', 'e', 'i', 'o', 'u']:
    return "an"
  else:
    return "a"

def oxford_comma(words):
  if len(words) == 0:
    return None
  elif len(words) == 1:
    return words[0]
  elif len(words) == 2:
    return f"{words[0]} and {words[1]}"
  else:
    return ', '.join(words[:-1]) + ', and ' + words[-1]

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

def yesno(flag):
  if flag == True:
    return 'yes'
  return 'no'