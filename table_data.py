from color import *
import mudlog
import object_data
import string_handling

#TODO: change name to table_data?
class table_data(object_data.object_data):
  """guests          = list of char's seated at the table
     num_guests      = number of guests at the table
     num_seats       = maximum number of guests"""

  DEFAULT_NUM_SEATS = 2

  def __init__(self, num_seats=None, proto=None):
    if num_seats == None:
      num_seats = self.DEFAULT_NUM_SEATS

    if num_seats < 0:
      logging.warning(f"Trying to create table with {num_seats} seats, which is negative.")
      num_seats = 0

    super().__init__(proto)
    self._guests = list()
    self.num_seats = num_seats

  """guests()           = return (copy of) list of guests at table
     num_guests()       = count the guests currently sitting at the table
     from_obj(obj)      = create a table from an existing object
     full()             = check if all seats are filled
     empty()            = check if table is empty
     add_guest(name)    = seat guest at table
     remove_guest(name) = remove guest from table
     is_seated(name)    = check if guest is at the table"""

  def guests(self):
    return [guest for guest in self._guests]

  def num_guests(self):
    return len(self.guests())

  @classmethod
  def from_obj(cls, old_obj, num_seats=None):
    if num_seats == None:
      num_seats = cls.DEFAULT_NUM_SEATS

    ret_val = cls(num_seats)

    # copy general object data
    super().copy_from(ret_val, old_obj)

    # set table specific data
    ret_val.num_seats = num_seats

    return ret_val

  def full(self):
    return len(self.guests()) >= self.num_seats

  def empty(self):
    return len(self.guests()) == 0

  def add_guest(self, ch):
    if self.full():
      logging.warning(f"Trying to add guest: {ch.name} at full table: {self.name}.")
      return
    self._guests.append(ch)

  def remove_guest(self, ch):
    if not self.is_seated(ch):
      logging.warning(f"Trying to remove non-existant guest: {ch.name} from {self.name}.")
    self._guests.remove(ch)

  def is_seated(self, ch):
    return ch in self.guests()

  def debug(self):
    ret_val = super().debug() + "\r\n"
    ret_val += f"Seats: {CYAN}{self.num_seats}{NORMAL}\r\n"
    ret_val += f"Num Guests: {CYAN}{self.num_guests()}{NORMAL}\r\n"
    ret_val += f"Guests: "
    if self.empty():
      ret_val += f"{CYAN}None{NORMAL}\r\n"
    else:
      ret_val += CYAN + ', '.join([guest.name for guest in self.guests()]) + NORMAL + '\r\n'

    ret_val += f"Full: {CYAN}{string_handling.yesno(self.full())}{NORMAL}\r\n"
    ret_val += f"Empty: {CYAN}{string_handling.yesno(self.empty())}{NORMAL}\r\n"

    return ret_val