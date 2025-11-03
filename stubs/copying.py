import copy

class inner:
  def __init__(self):
    self._field1 = list()

class outer:
  def __init__(self):
    self.inner1 = inner()
    self.inner2 = "constant"

x = [1,2,3]
y = copy.copy(x)

print(x == y)
print(x is y)