#import object_data

class inventory:
  """Creates an inventory of objects (for rooms, characters, and containers)
    contents = list of objects held by the inventory"""
  def __init__(self):
    self._contents = []

  def insert(self, obj):
    self._contents.append(obj)

  def remove(self, obj):
    if obj in self:
      self._contents.remove(obj)
    else:
      logging.error(f"Trying to remove {obj} from inventory which doesn't contain it!")
    
  def obj_by_alias(self, alias):
    for obj in self._contents:
      if obj.has_alias(alias):
        return obj

  def __contains__(self, obj):
    return obj in self._contents

  def __iter__(self):
    return inventory_iterator(self)

  def __len__(self):
    return len(self._contents)

class inventory_iterator:
  def __init__(self, inventory):
    self._inventory = inventory
    self._index = 0

  def __next__(self):
    if self._index < len(self._inventory._contents):
      result = self._inventory._contents[self._index]
      self._index += 1
      return result
    raise StopIteration

if __name__ == "__main__":
  inv = inventory()

  inv.insert("dagger")
  inv.insert("sword")

  for o in inv:
    print(o)
  
