class zedit_save_data:
  """Used to store changes until user quits OLC and finalizes.
     id     = unique identifier of zone
     name   = name of zone
     author = who to credit for the work
     folder = which folder to save the files to"""
  def __init__(self, id, name, author, folder):
    self.id = id
    self.name = name
    self.author = author
    self.folder = folder

  @property
  def id(self):
    return self._id

  @property
  def name(self):
    return self._name

  @property
  def author(self):
    return self._author

  @property
  def folder(self):
    return self._folder

  @id.setter
  def id(self, new_id):
    self._id = new_id

  @name.setter
  def name(self, new_name):
    self._name = new_name

  @author.setter
  def author(self, new_author):
    self._author = new_author

  @folder.setter
  def folder(self, new_folder):
    self._folder = new_folder