import buffer
import unittest

class TestBuffer(unittest.TestCase):

  def test_add_delete_clear(self):
    lines = [
      "This is the first line.",
      "This is the second line.",
      "This is the third line.",
      "This is the fourth line."
    ]

    test_buf = buffer.buffer();

    self.assertTrue(test_buf.is_empty)
    self.assertEqual(test_buf.num_lines, 0)

    test_buf.add_line(lines[0])
    self.assertEqual(test_buf.num_lines, 1)

    test_buf.add_line(lines[1])
    self.assertEqual(test_buf.num_lines, 2)

    test_buf.add_line(lines[2])
    self.assertEqual(test_buf.num_lines, 3)

    test_buf.add_line(lines[3])
    self.assertEqual(test_buf.num_lines, 4)

    self.assertFalse(test_buf.is_empty)

    # clear all lines
    test_buf.clear()

    self.assertTrue(test_buf.is_empty)
    self.assertEqual(test_buf.num_lines, 0)

    # add the lines back all at once
    for line in lines:
      test_buf.add_line(line)

    # test deleting initial line
    test_buf.delete_line(0)

    for idx in range(0, len(lines) - 1):
      self.assertEqual(test_buf[idx], lines[idx+1])

    self.assertEqual(test_buf.num_lines, 3)

    # reset
    test_buf.clear()
    for line in lines:
      test_buf.add_line(line)

    # test deleting middle line
    test_buf.delete_line(2)

    self.assertEqual(test_buf[0], lines[0])
    self.assertEqual(test_buf[1], lines[1])
    self.assertEqual(test_buf[2], lines[3])

    self.assertEqual(test_buf.num_lines, 3)

    # reset
    test_buf.clear()
    for line in lines:
      test_buf.add_line(line)

    # test deleting final line
    test_buf.delete_line(len(lines) - 1)

    for idx in range(0, len(lines) - 1):
      self.assertEqual(test_buf[idx], lines[idx])

    self.assertEqual(test_buf.num_lines, 3)

  def test_iterator(self):
    lines = [
      "This is the first line.",
      "This is the second line.",
      "This is the third line.",
      "This is the fourth line."
    ]

    par = '\n'.join(lines)

    test_buf = buffer.buffer(par)

    self.assertEqual(test_buf.num_lines, len(lines))

    idx = 0
    with self.assertRaises(StopIteration):
      i = iter(test_buf)
      j = iter(lines)
      while(True):
        l1 = next(i)
        l2 = next(j)

if __name__ == '__main__':
  unittest.main();