import dataclasses
import logging
import structs

class object:
  """Creates an object which characters can get, drop, and otherwise interact with.
    entity = aggregates name, namelist, description, and room
    ldesc = one line description shown after room description"""
  def __init__(self, proto=None):
    self._entity = structs.entity_data()
    self._ldesc = "An unfinished object has been left here."

    if proto != None:
      self.ldesc = proto.ldesc
      self._entity = dataclasses.replace(proto.entity)

  @property
  def ldesc(self):
    return self._ldesc
  @property
  def room(self):
    return self._entity.room
  @property
  def name(self):
    return self._entity.name

  @ldesc.setter
  def ldesc(self, new_ldesc):
    self._ldesc = new_ldesc
  @room.setter
  def room(self, new_room):
  	self._room = new_room
  @name.setter
  def name(self, new_name):
    self._entity.name = new_name

  def has_alias(self, alias):
    return self._entity.has_alias(alias)

  def __str__(self):
    return self.name

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
  import game
  mud = game.game()
  mud.init_wld()
  mud.init_npcs()
  mud.init_objs()
  x = inventory()
  x.insert(mud.load_obj(3000))
  x.insert(mud.load_obj(3001))

  for item in x:
    print(item.name)
