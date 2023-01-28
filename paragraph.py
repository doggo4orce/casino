import re

str = "You are at the southern end of the temple hall in the Temple of Midgaard. The temple, constructed from giant marble blocks, is eternal in appearance. Ancient paintings picturing Gods, Giants, and peasants cover most of its walls.  Broad steps lead down through the grand temple gate, descending to the massive mound upon which the temple was built. The steps end at the temple square below. To the west, you see the Reading Room. The donation room is in a small alcove to your east."

lines = [
  "You are at the southern end of the temple hall",
  "in the Temple of Midgaard. The temple, constructed",
  "from giant marble blocks, is eternal in appearance. ",
  "Ancient paintings picturing Gods, Giants, and peasants",
  "cover most of its walls.  Broad steps lead down through the ",
  "grand temple gate, descending to the massive mound upon which",
  "the temple was built. The steps end at the temple square below.",
  "To the west, you see the Reading Room. The donation room is in a small alcove to your east."
]

sentence = ' '.join(lines)

# sentence = """Hey man  ,  how     are  you .  
#      You  stink.  I     
# really     think  you  
# are stupid even though
#  I can't 
# type 
# properly   myself .      """

def proof_read_paragraph(paragraph):

  formatted = ""

  list1 = sentence.split(' ')
  list2 = list()
  begin_sentence = True

  for word in list1:

    word = word.strip()

    if word == '':
      continue

    if word in {'.', '?'}:
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

    if word[-1:] in {'.', '?'}:
      formatted += ' '
      begin_sentence = True

  return formatted