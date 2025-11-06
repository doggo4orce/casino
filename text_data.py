class text_data:
  def __init__(self, text):
    self.text = text

  @property
  def text(self):
    return self._text

  @text.setter
  def text(self, new_text):
    self._text = new_text