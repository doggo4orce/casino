class inner:
  def __init__(self):
    self.field = None

class outer:
  def __init__(self):
    self._inner = inner()

  @property
  def inner(self):
    return self._inner

  @inner.setter
  def inner(self, new_inner):
    self._inner = new_inner

foo = outer()


print(foo)
print(foo.inner)
print(foo.inner.field)

foo.inner.field = 3

print(foo)
print(foo.inner)
print(foo.inner.field)