import copy

class namelist_data:
  """May be used to identify an object, NPC, or any type of entity.
     aliases = a list of strings that may be used as identifiers"""
  def __init__(self, *aliases):
    self._aliases = list(aliases)

    if type(aliases) == list:
      for alias in aliases:
        if type(alias) == str:
          self.add_alias(alias)

  """add_alias(alias)    <- adds a new alias
     has_alias(alias)    <- check if alias exists
     num_aliases         <- count the number of aliases
     remove_alias(alias) <- removes alias
     remove_all()        <- removes all aliases
     reset(*aliases)     <- start fresh with new aliases
     list()              <- returns copy of _aliases"""

  def add_alias(self, alias):
    if not self.has_alias(alias):
      self._aliases.append(alias)
      
  def has_alias(self, alias):
    return alias in self._aliases

  @property
  def num_aliases(self):
    return len(self._aliases)

  def remove_alias(self, alias):
    if self.has_alias(alias):
      self._aliases.remove(alias)

  def remove_all(self):
    self._aliases = list()

  def reset(self, *aliases):
    self.remove_all()
    for alias in aliases:
      self.add_alias(alias)

  def list(self):
    return copy.copy(self._aliases)

  def __contains__(self, keyword):
    return keyword in self._aliases

  def __getitem__(self, key):
    return self._aliases[key]

  def __str__(self):
    return ' '.join(self._aliases)

class namelist_data_iterator:
  def __init__(self, namelist):
    self._namelist = namelist
    self._idx = 0

  def __next__(self):
    if self._idx < 0 or self._idx >= len(self._namelist._aliases):
      raise StopIteration

    ret_val = self._namelist._aliases[self._idx]
    self._idx += 1
    return ret_val

