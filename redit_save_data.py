import room_attribute_data

class redit_save_data:
  """There should be a field here for each of the fields in the main menu for redit.  Then the users
     selection for those fields can be saved here locally until they finish OLC and make their changes permanent.
     r_attr   = uid, name, desc, exits
     dir_edit = direction specified on previous command to edit an exit"""
  def __init__(self, zid=None, id=None):
    self.r_attr = room_attribute_data.room_attribute_data(zid, id)
    self.r_attr.name = "An Unfinished Room"
    self.r_attr.desc = "It looks unfinished."
    self.dir_edit = None

  @property
  def r_attr(self):
    return self._r_attr
  @property
  def dir_edit(self):
    return self._dir_edit

  @r_attr.setter
  def r_attr(self, new_attr):
    self._r_attr = new_attr
  @dir_edit.setter
  def dir_edit(self, new_dir):
    self._dir_edit = new_dir