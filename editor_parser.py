import enum

class parser_state(enum.IntEnum):
  DEFAULT = 0
  IN_PROGRESS = 1
  PARAGRAPH = 2                 
  CLOSE_PARAGRAPH = 3           # just closed paragraph, will start newline before parsing more text

class editor_parser:
  def __init__(self):
    self.state = parser_state.DEFAULT
    self.parsed = ""
    self.paragraph = ""

  def parse_char(self, b, next):
    if self.state == DEFAULT:
      if b == '<':
        if next[:2] == "p>"
          self.state = PARAGRAPH
          return 3
        else:
          self.tag += b
          return 1
      else b == '\r':
        if next[0] == '\n'
          self.parsed += '\r\n'
          return 2
        else:
          self.parsed += b
          return 1
    elif self.state == IN_PROGRESS:
      if b == '<':
        if next[:2] == "p>"
          self.state = PARAGRAPH
          return 3
        else:
          self.parsed += b
      else:
        self.parsed += b
    elif self.state == PARAGRAPH:
      if b == '<':
        self.state = POSSIBLE_CLOSE_PARAGRAPH
        self.tag += b
      else:
      	self.parsed += b
    elif self.state == CLOSE_PARAGRAPH:
      if b == '