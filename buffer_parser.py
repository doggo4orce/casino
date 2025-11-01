from color import *

import enum
import string_handling

class parser_state(enum.IntEnum):
  DEFAULT         = 0 # about to start a new line, expecting <p> or ascii
  READING         = 1 # working on a line, outside of a paragraph
  PARAGRAPH       = 2 # streaming to an incomplete paragraph
  CLOSE_PARAGRAPH = 3 # just closed paragraph, will start newline before parsing more text

class buffer_parser:
  """TODO: write doc string for this"""
  def __init__(self):
    self.state = parser_state.DEFAULT
    self.parsed = ""
    self.paragraph = ""

  def parse_string(self, text):
    idx = 0
    while True:
      if idx == len(text):
        break
      num_bytes = self.parse_char(text[idx], text[idx+1:])
      idx += num_bytes
    return self.parsed

  def parse_char(self, b, next):
    if self.state == parser_state.DEFAULT:
      if b == '<':
        if next[:2] == "p>" and next.find('</p>') != -1:
          self.parsed += "<p>"
          self.state = parser_state.PARAGRAPH
          return 3
        else:
          self.parsed += b
          return 1
      elif b == '\r':
        if next[0] == '\n':
          self.parsed += '\r\n'
          return 2
        else:
          # should never happen, but if it does, skip this character
          return 1
      elif b == '\n':
        # shouldn't get here either, but if it does, add \r
        self.parsed += '\r\n'
        return 1
      else:
        self.state = parser_state.READING
        self.parsed += b
        return 1 
    elif self.state == parser_state.READING:
      if b == '<':
        if next[:2] == "p>" and next.find('</p>') != -1:
          self.state = parser_state.PARAGRAPH
          self.parsed += "\r\n<p>"
          return 3
        else:
          self.parsed += b
          return 1
      elif b == '\r':
        if next[0] == '\n':
          self.state = parser_state.DEFAULT
          self.parsed += '\r\n'
          return 2
        else:
          # should never happen, but if it does, skip this character
          return 1
      elif b == '\n':
        # shouldn't get here either, but if it does add \r
        self.state = parser_state.DEFAULT
        self.parsed += '\r\n'
        return 1
      else:
        self.parsed += b
        return 1
    elif self.state == parser_state.PARAGRAPH:
      if b == '<':
        if next[:3] == '/p>':
          self.state = parser_state.CLOSE_PARAGRAPH
          self.parsed += string_handling.clean_up_paragraph(self.paragraph) + '</p>'
          self.paragraph = ""
          return 4
        else:
          self.paragraph += b
          return 1
      elif b == '\r':
        if next[0] == '\n':
          self.paragraph += "\r\n"
          return 2
        else:
          # should never happen, but if it does, skip this character
          return 1
      elif b == '\n':
        # shouldn't get here either, but if we do add \r
        self.paragraph += '\r\n'
        return 1
      else:
        self.paragraph += b
        return 1
    elif self.state == parser_state.CLOSE_PARAGRAPH:
      if b == '\r':
        if next[0] == '\n':
          self.parsed += "\r\n"
          self.state = parser_state.DEFAULT
          return 2
        else:
          # should never happen, but if it does, skip this character
          return 1
      elif b == '\n':
        # shouldn't get here either, but if we do add \r
        self.parsed += '\r\n'
        self.state = parser_state.DEFAULT
        return 1
      else:
        self.parsed += '\r\n'
        self.parsed += b
        self.state = parser_state.READING
        return 1

  def debug(self):
    ret_val = f"State: {CYAN}{self.state.name}{NORMAL}\r\n"
    ret_val += f"Parsed: {CYAN}{repr(self.parsed)}{NORMAL}\r\n"
    ret_val += f"Paragraph: {CYAN}{self.paragraph}{NORMAL}"
    return ret_val