class zedit_save_data:
  """Used to store changes until user quits OLC and finalizes.
     id     = unique identifier of zone
     name   = name of zone
     author = who to credit for the work"""
  def __init__(self, id=None, name=None, author=None):
    self.id = id
    self.name = name
    self.author = author

  @property
  def id(self):
    return self._id

  @property
  def name(self):
    return self._name

  @property
  def author(self):
    return self._author

  @id.setter
  def id(self, new_id):
    self._id = new_id

  @name.setter
  def name(self, new_name):
    self._name = new_name

  @author.setter
  def author(self, new_author):
    self._author = new_author