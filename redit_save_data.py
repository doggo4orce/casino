import room_attribute_data

class redit_save_data:
  """There should be a field here for each of the fields in the main menu for redit.  Then the users
     selection for those fields can be saved here locally until they finish OLC and make their changes permanent.
     attributes   = uid, name, desc, exits
     dir_edit     = direction specified on previous command to edit an exit"""
  def __init__(self, zid=None, id=None):
    self.attributes = room_attribute_data.room_attribute_data(zid, id)
    self.attributes.name = "An Unfinished Room"
    self.attributes.desc = "It looks unfinished."
    self.dir_edit = None

  @property
  def attributes(self):
    return self._attributes
  @property
  def dir_edit(self):
    return self._dir_edit

  @attributes.setter
  def attributes(self, new_attributes):
    self._attributes = new_attributes

  @dir_edit.setter
  def dir_edit(self, new_dir):
    self._dir_edit = new_dir

  def connect(self, direction, *args):
    self.attributes.connect(direction, *args)

  def disconnect(self, direction):
    self.attributes.disconnect(direction)

  def destination(self, direction):
    return self.attributes.destination(direction)