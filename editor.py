import dataclasses

@dataclasses.dataclass
class document:
  def __init__(self):
    self.lines = ["This is a brand new document, with a single short paragraph."]

@dataclasses.dataclass
class editor:
  pass