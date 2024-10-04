import mudlog

class inventory_data:
  """Creates an inventory of objects (for rooms, characters, and containers)
    contents = list of objects held by the inventory"""
  def __init__(self):
    self._contents = []

  """add_object(obj)         <- add object to inventory
     has_object(obj)         <- check if object is in inventory
     remove_object(obj)      <- remove object from inventory
     object_by_alias(alias)  <- look up object in inventory by alias"""

  def add_object(self, obj):
    self._contents.append(obj)

  def has_object(self, obj):
    return obj in self

  def remove_object(self, obj):
    if self.has_object(obj):
      self._contents.remove(obj)
    else:
      mudlog.error(f"Trying to remove {obj} from inventory which doesn't contain it!")
    
  def object_by_alias(self, alias):
    for obj in self:
      if obj.has_alias(alias):
        return obj
    return None

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
    if self._index < len(self._inventory._contents):
      result = self._inventory._contents[self._index]
      self._index += 1
      return result
    raise StopIteration

