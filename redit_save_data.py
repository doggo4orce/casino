import unique_id_data

class redit_save_data:
  """There should be a field here for each of the fields in the main menu for redit.  Then the users
     selection for those fields can be saved here locally until they finish OLC and make their changes permanent.
     uid        = unique identifier of room being edited
     room_name  = name of room being edited
     room_desc  = description of room being edited
     room_exits = dictionary of exit vrefs using directions as keys
     dir_edit   = direction specified on previous command to edit an exit"""
  def __init__(self, zid, id):
    self.uid = unique_id_data.unique_id_data(zid, id)
    self.name = "An unfinished room"
    self.desc = "You are in an unfinished room."
    self.exits = dict()
    self.dir_edit = None