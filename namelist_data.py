class namelist_data:
  """May be used to identify an object, NPC, or any type of entity.
     aliases = a list of strings that may be used as identifiers"""
  def __init__(self, *aliases):
    self._aliases = list(aliases)

    if type(aliases) == list:
      for alias in aliases:
        if type(alias) == str:
          self.add_alias(alias)

  """add_alias(alias)    <- adds a new alias to self.aliases
     has_alias(alias)    <- check if alias is in self.aliases
     num_aliases()       <- count the number of aliases in self.alias
     remove_alias(alias) <- removes alias from self.aliases"""

  def add_alias(self, alias):
    if not self.has_alias(alias):
      self._aliases.append(alias)
      
  def has_alias(self, alias):
    return alias in self._aliases

  def num_aliases(self):
    return len(self._aliases)

  def remove_alias(self, alias):
    if self.has_alias(alias):
      self._aliases.remove(alias)

  def __contains__(self, keyword):
    return keyword in self._aliases

  def __getitem__(self, key):
    return self._aliases[key]

  def __len__(self):
    return len(self._aliases)

  def __str__(self):
    return str(self._aliases)

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

