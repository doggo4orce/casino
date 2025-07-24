import copy
import mudlog

class inventory_data:
  """Creates an inventory of objects (for rooms, characters, and containers)
    contents = list of objects held by the inventory"""
  def __init__(self):
    self._contents = []

  """add_object(obj)        <- add object to inventory
     contents()             <- returns a copy of self._contents
     empty()                <- check if inventory is empty
     has_object(obj)        <- check if object is in inventory
     remove_object(obj)     <- remove object from inventory
     remove_all()           <- remove all objects from inventory
     object_by_alias(alias) <- look up object in inventory by alias
     transfer_obj(obj, inv) <- transfer object to new inventory
     transfer_all(inv)      <- transfer all contents to new inventory"""

  def add_object(self, obj):
    self._contents.append(obj)

  def contents(self):
    return copy.copy(self._contents)

  def empty(self):
    return len(self) == 0

  def has_object(self, obj):
    return obj in self

  def remove_object(self, obj):
    if self.has_object(obj):
      self._contents.remove(obj)
    else:
      mudlog.error(f"Trying to remove {obj} from inventory which doesn't contain it!")

  def remove_all(self):
    for obj in self.contents():
      self.remove_object(obj)

  def object_by_alias(self, alias):
    for obj in self:
      if obj.has_alias(alias):
        return obj
    return None

  def transfer_obj(self, obj, inv):
    if obj == None:
      mudlog.error(f"Trying to transfer object None from inventory.")
    elif inv == None:
      mudlog.error(f"Trying to transfer object from inventory None.")
    else:
      self.remove_object(obj)
      inv.add_object(obj)

  def transfer_all(self, inv):
    if inv == None:
      mudlog.error(f"Trying to transfer_all into inventory None.")
      return

    for obj in self.contents():
      self.transfer_obj(obj, inv)

  def __getitem__(self, key):
    return self._contents[key]

  def __contains__(self, obj):
    return obj in self._contents

  def __iter__(self):
    return inventory_data_iterator(self)

  def __len__(self):
    return len(self._contents)

class inventory_data_iterator:
  def __init__(self, inventory):
    self._inventory = inventory
    self._index = 0

  def __next__(self):
    if self._index < len(self._inventory):
      result = self._inventory[self._index]
      self._index += 1
      return result
    raise StopIteration

