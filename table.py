import logging
import object
import string_handling

class table(object.object):
  """guests          = list of guests' names at the table
     num_guests      = number of guests at the table
     num_seats       = maximum number of guests
     full            = True if the table is full, False otherwise"""

  DEFAULT_NUM_SEATS = 2
  def __init__(self, num_seats=None, proto=None):
    if num_seats == None:
      num_seats = self.DEFAULT_NUM_SEATS

    if num_seats < 0:
      logging.warning(f"Trying to create table with {num_seats} seats, which is negative.")
      num_seats = 0

    super().__init__(proto)
    self._guests = list()
    self._num_seats = num_seats

  """from_obj(obj)      = create a table from an existing object
     add_guest(name)    = seat guest at table
     remove_guest(name) = remove guest from table
     is_seated(name)    = check if guest is at the table"""

  @property
  def guests(self):
    return self._guests
  @property
  def num_guests(self):
    return len(self.guests)
  @property
  def num_seats(self):
    return self._num_seats
  @property
  def full(self):
    return len(self._guests) >= self.num_seats

  @guests.setter
  def guests(self, new_guests):
    self._guests = new_guests
  @num_seats.setter
  def num_seats(self, new_num_seats):
    self._num_seats = new_num_seats

  @classmethod
  def from_obj(cls, old_obj, num_seats=None):
    if num_seats == None:
      num_seats = cls.DEFAULT_NUM_SEATS

    ret_val = cls(num_seats)
    ret_val.entity = old_obj.entity
    ret_val.ldesc = old_obj.ldesc
    ret_val.prefix_command_triggers = old_obj.prefix_command_triggers
    ret_val.suffix_command_triggers = old_obj.suffix_command_triggers
    ret_val.heart_beat_procs = old_obj.heart_beat_procs
    ret_val.num_seats = num_seats
    return ret_val

  def add_guest(self, name):
    if self.full:
      logging.warning(f"Trying to add guest: {name} at full table: {self.name}.")
      return
    self._guests.append(name)

  def remove_guest(self, name):
    if not self.is_seated(name):
      logging.warning(f"Trying to remove non-existant guest: {name} from {self.name}.")
    self._guests.remove(name)

  def is_seated(self, name):
    return name in self.guests

  def debug(self):
    ret_val = super().debug()
    ret_val += f"Total Seats: {self.num_seats}\r\n"
    for guest in self.guests:
      ret_val += f"  {guest}\r\n"
    ret_val += f"Full: {string_handling.yesno(self.full)}\r\n"

    return ret_val