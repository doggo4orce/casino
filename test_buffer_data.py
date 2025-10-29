import buffer_data
import unittest

class TestBuffer(unittest.TestCase):

  def test_constructor(self):
    lines = [
      "This is the first line.",
      "This is the second line.",
      "This is the third line.",
      "This is the fourth line."
    ]

    paragraph = "\r\n".join(lines)

    test_buf = buffer_data.buffer_data(paragraph)

    for idx, line in enumerate(lines):
      self.assertEqual(lines[idx], test_buf[idx])

  def test_iterator_clear(self):
    lines = [
      "This is the first line.",
      "This is the second line.",
      "This is the third line.",
      "This is the fourth line."
    ]

    test_buf = buffer_data.buffer_data()

    test_buf.add_lines(lines)

    self.assertEqual(test_buf.num_lines, len(lines))

    # check that lines are stored in the correct order
    for idx, line in enumerate(lines):
      self.assertEqual(test_buf[idx], lines[idx])

    test_buf.clear()

    self.assertTrue(test_buf.is_empty)

  def test_add_delete(self):
    lines = [
      "This is the first line.",
      "This is the second line.",
      "This is the third line.",
      "This is the fourth line."
    ]

    test_buf = buffer_data.buffer_data();

    self.assertTrue(test_buf.is_empty)
    self.assertEqual(test_buf.num_lines, 0)

    # test adding the lines
    for idx, line in enumerate(lines):
      test_buf.add_line(line)
      self.assertEqual(test_buf.num_lines, idx + 1)

    self.assertFalse(test_buf.is_empty)

    # test deleting initial line
    test_buf.delete_line(0)

    for idx in range(0, len(lines) - 1):
      self.assertEqual(test_buf[idx], lines[idx+1])

    self.assertEqual(test_buf.num_lines, 3)

    # reset
    test_buf = buffer_data.buffer_data()

    for line in lines:
      test_buf.add_line(line)

    # test deleting middle line
    test_buf.delete_line(2)

    self.assertEqual(test_buf[0], lines[0])
    self.assertEqual(test_buf[1], lines[1])
    self.assertEqual(test_buf[2], lines[3])

    self.assertEqual(test_buf.num_lines, 3)

    # reset
    test_buf = buffer_data.buffer_data()

    for line in lines:
      test_buf.add_line(line)

    # test deleting final line
    test_buf.delete_line(len(lines) - 1)

    for idx in range(0, len(lines) - 1):
      self.assertEqual(test_buf[idx], lines[idx])

    self.assertEqual(test_buf.num_lines, 3)

  def test_add_multiple_lines(self):
    lines = [
      "This is the first line.",
      "This is the second line.",
      "This is the third line.",
      "This is the fourth line."
    ]

    test_buf = buffer_data.buffer_data()

    test_buf.add_lines(lines)

    for idx, line in enumerate(lines):
      self.assertEqual(line, test_buf[idx])

  def test_insert(self):
    lines = [
      "This is the first line.",
      "This is the second line.",
      "This is the third line.",
      "This is the fourth line."
    ]

    test_buf = buffer_data.buffer_data()

    for j in range(0,3):
      test_buf.add_line(lines[j])

    # add last line in position 1
    test_buf.insert_line(1, lines[3])

    self.assertEqual(test_buf[0],lines[0])
    self.assertEqual(test_buf[1],lines[3])
    self.assertEqual(test_buf[2],lines[1])
    self.assertEqual(test_buf[3],lines[2])

  def test_copy_from(self):
    lines = [
      "This is the first line.",
      "This is the second line.",
      "This is the third line.",
      "This is the fourth line."
    ]

    test_buf1 = buffer_data.buffer_data()
    test_buf2 = buffer_data.buffer_data()

    for j in range(0,3):
      test_buf1.add_line(lines[j])

    test_buf2.copy_from(test_buf1)

    for idx in range(0,3):
      self.assertEqual(test_buf1[idx], test_buf2[idx])

    test_buf1[0] = "This line has changed."

    # check that changing the original doesn't change the first
    self.assertNotEqual(test_buf1[0], test_buf2[0])

  def test_make_copy(self):
    lines = [
      "This is the first line.",
      "This is the second line.",
      "This is the third line.",
      "This is the fourth line."
    ]

    test_buf1 = buffer_data.buffer_data()
    test_buf2 = buffer_data.buffer_data()

    for line in lines:
      test_buf1.add_line(line)

    test_buf2 = test_buf1.make_copy()

    for idx in range(0,3):
      self.assertEqual(test_buf1[idx], test_buf2[idx])

    test_buf1[0] = "This line has changed."

    # check that changing the original doesn't change the first
    self.assertNotEqual(test_buf1[0], test_buf2[0])

  def test_clean_up1(self):
    lines_messy = [
      ":) +------+ (*)=(*) ASCII ART 1 + 2 = 3"
      "<p> Hello, ",
      "buddy I         miss you ! "
      "Oh I     forgot to  close the paragraph . </p>"
    ]

    lines_cleaned = [
      ":) +------+ (*)=(*) ASCII ART 1 + 2 = 3",
      "<p> Hello, buddy I         miss you ! Oh I     forgot to  close the paragraph . </p>"
    ]
  
    test_buf = buffer_data.buffer_data()
    test_buf.add_lines(lines_messy)
    test_buf = test_buf.clean_up()

    for idx, line in enumerate(test_buf.clean_up()):
      self.assertEqual(lines_cleaned[idx], line)

  # def test_clean_up(self):
  #   lines_messy = [
  #     ":) +------+ (*)=(*) ASCII ART 1 + 2 = 3",
  #     "<p>.",       # first char is the first word
  #     ".. ...",     # next two words
  #     "",           # empty line within paragraph ignored
  #     "... ",       # trailing space (*)
  #     "</p>",
  #     "   <(v_v)>", # not in paragraph, left alone
  #     "<p> ... ",
  #     ".. </p>"     # terminating with </p>
  #   ]

  #   lines_clean = [
  #     ":) +------+ (*)=(*) ASCII ART 1 + 2 = 3",
  #     "<p>. .. ...  ...  </p>",  # double space caused by (*)
  #     "   <(v_v)>",
  #     "<p> ...  .. </p>"
  #   ]

  #   lines_messy2 = [
  #     "<p>.",           # first char is the first word
  #     "...",
  #     "<p>.. ... </p>", # invalid <p> ignored
  #     "</p> <p>",       # should be ignored
  #   ]

  #   lines_clean2 = [
  #     "<p>. ... <p>.. ... </p>",
  #     "</p> <p>"
  #   ]

  #   test_buf = buffer_data.buffer_data()
  #   test_buf2 = buffer_data.buffer_data()

  #   test_buf.add_lines(lines_messy)
  #   test_buf2.add_lines(lines_messy2)

  #   for idx, line in enumerate(test_buf.clean_up()):
  #     self.assertEqual(lines_clean[idx], line)

  #   for idx, line in enumerate(test_buf2.clean_up()):
  #     self.assertEqual(lines_clean2[idx], line)

  # def test_str(self):
  #   lines = [
  #     ":) +------+ (*)=(*) ASCII ART 1 + 2 = 3",
  #     "<p>.",
  #     ".. ...",
  #     "",
  #     "... ",
  #     "</p>",
  #     "   <(v_v)>"
  #   ]

  #   test_buf = buffer_data.buffer_data()

  #   # convert lines to buffer
  #   test_buf.add_lines(lines)

  #   # convert buffer to str
  #   str = test_buf.str(numbers=False)

  #   # convert str back to buffer
  #   test_buf2 = buffer_data.buffer_data(str)

  #   # ensure lines are still correct
  #   for idx, line in enumerate(test_buf):
  #     self.assertEqual(test_buf[idx], test_buf2[idx])

  #   # convert back to str yet again
  #   str2 = test_buf2.str(numbers=False)

  #   self.assertEqual(str, str2)

  # def test_display(self):
  #   lines = [
  #     "... . . . .",
  #     "      .",
  #     "<p>... ..... ..... ",
  #     " ... ...... .... ... ....",
  #     " ....",
  #     " </p>",
  #     "",
  #     "... ",
  #     "</p>",
  #     "   ......."
  #   ]

  #   display_lines = [
  #     "... . . . .",
  #     "      .",
  #     "<p>... ..... ..... ... ...... .... ... .... ....</p>",
  #     "</p> <p>",      # lonely tags ignored
  #     "   ......."
  #   ]

  #   original_buf = buffer_data.buffer_data()
  #   original_buf.add_lines(lines)

  #   display_buf = original_buf.display(
  #     width=30,
  #     indent=True,
  #     color=False,
  #     numbers=False)

  #   for idx, line in enumerate(display_buf):
  #     self.assertEqual(display_buf[idx], display_lines[idx])

if __name__ == '__main__':
  unittest.main();