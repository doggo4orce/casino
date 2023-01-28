OPEN_PARAGRAPH  = "<p>"
CLOSE_PARAGRAPH = "</p>"

class buffer:
  """Used to keep organize editor input for writing rooms, messages, etc.
     contents = the raw contents of buffer, one line at a time"""
  def __init__(self, str=None):
    self._contents = list()

  """num_lines()           <- returns number of lines in the buffer
     is_empty()            <- returns True is there aren't any lines in the buffer
     add_line()            <- adds a line to the buffer
     insert_line(idx, str) <- adds a line in position idx and re-orders if necessary
     delete_line(idx)      <- deletes the line and re-orders
     clear()               <- empty self._contents
     make_copy()           <- returns a new buffer with identical contents
     copy_from(buf)        <- resets the contents to be identical from those of buf
     display(width)        <- returns buffer as string formatted to width.
                              optional flags: format, indent, numbers
     clean_up()            <- returns lines with paragraphs tidied up, optionally fix typos
     str(numbers)          <- converts to string, with optional line numbers"""