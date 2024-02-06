import buffer
import unittest

class TestBuffer(unittest.TestCase):

  def test_iterator_clear(self):
    lines = [
      "This is the first line.",
      "This is the second line.",
      "This is the third line.",
      "This is the fourth line."
    ]

    par = '\n'.join(lines)

    test_buf = buffer.buffer(par)

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

    test_buf = buffer.buffer();

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
    test_buf = buffer.buffer()

    for line in lines:
      test_buf.add_line(line)

    # test deleting middle line
    test_buf.delete_line(2)

    self.assertEqual(test_buf[0], lines[0])
    self.assertEqual(test_buf[1], lines[1])
    self.assertEqual(test_buf[2], lines[3])

    self.assertEqual(test_buf.num_lines, 3)

    # reset
    test_buf = buffer.buffer()

    for line in lines:
      test_buf.add_line(line)

    # test deleting final line
    test_buf.delete_line(len(lines) - 1)

    for idx in range(0, len(lines) - 1):
      self.assertEqual(test_buf[idx], lines[idx])

    self.assertEqual(test_buf.num_lines, 3)

  def test_insert(self):
    lines = [
      "This is the first line.",
      "This is the second line.",
      "This is the third line.",
      "This is the fourth line."
    ]

    test_buf = buffer.buffer()

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

    test_buf1 = buffer.buffer()
    test_buf2 = buffer.buffer()

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

    test_buf1 = buffer.buffer()
    test_buf2 = buffer.buffer()

    for j in range(0,3):
      test_buf1.add_line(lines[j])

    test_buf2 = test_buf1.make_copy()

    for idx in range(0,3):
      self.assertEqual(test_buf1[idx], test_buf2[idx])

    test_buf1[0] = "This line has changed."

    # check that changing the original doesn't change the first
    self.assertNotEqual(test_buf1[0], test_buf2[0])

  def test_display(self):
    lines = [
      "The quick brown ",
      " fox jumped over",
      "       the",
      "lazy dog."
    ]

    
if __name__ == '__main__':
  unittest.main();