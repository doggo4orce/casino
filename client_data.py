class client_data:
  """term_type      = client name
     term_width     = width of terminal window
     term_length    = length of terminal window
     term_host      = name or IP of host as a string (does this belong here?)"""
  def __init__(self, term_type=None, term_width=None, term_length=None, term_host=None):
    self.term_type = term_type
    self.term_width = term_width
    self.term_length = term_length
    self.term_host = term_host

  @property
  def term_type(self):
    return self._term_type

  @property
  def term_width(self):
    return self._term_width

  @property
  def term_length(self):
    return self._term_length

  @property
  def term_host(self):
    return self._term_host

  @term_type.setter
  def term_type(self, new_term_type):
    self._term_type = new_term_type

  @term_width.setter
  def term_width(self, new_term_width):
    self._term_width = new_term_width

  @term_length.setter
  def term_length(self, new_term_length):
    self._term_length = new_term_length

  @term_host.setter
  def term_host(self, new_term_host):
    self._term_host = new_term_host