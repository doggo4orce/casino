# python modules
import unittest

# local modules
# import buffer_data
import buffer_parser

class TestBufferParser(unittest.TestCase):
  def test_parse_string(self):
    parser = buffer_parser.buffer_parser()

    lines_messy = [
      "<p>.",           # first char is the first word
      "...",            # continue the paragraph
      "",               # empty line within paragraph ignored
      "<p>.. ... </p>", # <p> is part of the paragraph
      "</p> <p>",       # </p> should be treated as ascii but <p> starts a new paragraph
      "<p> ... ",       # leading \r\n should be trimmed and <p> is first word
      ".. </p>"         # terminating with </p>
    ]

    lines_clean = [
      "<p>. ... <p>.. ... </p>",
      "</p> ",
      "<p><p> ... .. </p>"
    ]

    messy = '\r\n'.join(lines_messy)
    clean = '\r\n'.join(lines_clean)

    parser.parse_string(messy)
    self.assertEqual(parser.parsed, clean)

  def test_parse_char(self):
    parser = buffer_parser.buffer_parser()

    self.assertEqual(parser.state, buffer_parser.parser_state.DEFAULT)

    parser.parse_char('6', '<p>.\r\n...\r\n\r\n<p>.. ... </p>\r\n</p> <p>\r\n<p> ... \r\n.. </p>')

    self.assertEqual(parser.state, buffer_parser.parser_state.READING)
    self.assertEqual(parser.parsed, "6")

    parser.parse_char('<', 'p>.\r\n...\r\n\r\n<p>.. ... </p>\r\n</p> <p>\r\n<p> ... \r\n.. </p>')

    self.assertEqual(parser.state, buffer_parser.parser_state.PARAGRAPH)
    self.assertEqual(parser.parsed, "6\r\n<p>")

    parser.parse_char('.', '\r\n...\r\n\r\n<p>.. ... </p>\r\n</p> <p>\r\n<p> ... \r\n.. </p>')

    self.assertEqual(parser.state, buffer_parser.parser_state.PARAGRAPH)
    self.assertEqual(parser.parsed, "6\r\n<p>")
    self.assertEqual(parser.paragraph, ".")

    parser.parse_char('\r', '\n...\r\n\r\n<p>.. ... </p>\r\n</p> <p>\r\n<p> ... \r\n.. </p>')

    self.assertEqual(parser.state, buffer_parser.parser_state.PARAGRAPH)
    self.assertEqual(parser.parsed, "6\r\n<p>")
    self.assertEqual(parser.paragraph, ".\r\n")

    parser.parse_char('.', '..\r\n\r\n<p>.. ... </p>\r\n</p> <p>\r\n<p> ... \r\n.. </p>')

    self.assertEqual(parser.state, buffer_parser.parser_state.PARAGRAPH)
    self.assertEqual(parser.parsed, "6\r\n<p>")
    self.assertEqual(parser.paragraph, ".\r\n.")

    parser.parse_char('.', '.\r\n\r\n<p>.. ... </p>\r\n</p> <p>\r\n<p> ... \r\n.. </p>')

    self.assertEqual(parser.state, buffer_parser.parser_state.PARAGRAPH)
    self.assertEqual(parser.parsed, "6\r\n<p>")
    self.assertEqual(parser.paragraph, ".\r\n..")

    parser.parse_char('.', '\r\n\r\n<p>.. ... </p>\r\n</p> <p>\r\n<p> ... \r\n.. </p>')

    self.assertEqual(parser.state, buffer_parser.parser_state.PARAGRAPH)
    self.assertEqual(parser.parsed, "6\r\n<p>")
    self.assertEqual(parser.paragraph, ".\r\n...")

    parser.parse_char('\r', '\n\r\n<p>.. ... </p>\r\n</p> <p>\r\n<p> ... \r\n.. </p>')

    self.assertEqual(parser.state, buffer_parser.parser_state.PARAGRAPH)
    self.assertEqual(parser.parsed, "6\r\n<p>")
    self.assertEqual(parser.paragraph, ".\r\n...\r\n")

    parser.parse_char('\r', '\n<p>.. ... </p>\r\n</p> <p>\r\n<p> ... \r\n.. </p>')

    self.assertEqual(parser.state, buffer_parser.parser_state.PARAGRAPH)
    self.assertEqual(parser.parsed, "6\r\n<p>")
    self.assertEqual(parser.paragraph, ".\r\n...\r\n\r\n")

    parser.parse_char('<', 'p>.. ... </p>\r\n</p> <p>\r\n<p> ... \r\n.. </p>')

    self.assertEqual(parser.state, buffer_parser.parser_state.PARAGRAPH)
    self.assertEqual(parser.parsed, "6\r\n<p>")
    self.assertEqual(parser.paragraph, ".\r\n...\r\n\r\n<")

if __name__ == "__main__":
  suite = unittest.TestSuite()
  suite.addTest(TestBufferParser('test_parse_string'))
  unittest.TextTestRunner().run(suite)
