class base:
  def __init__(self):
    self.x = None

  @property
  def x(self):
    print("base class getter called")
    return self._x

  @x.setter
  def x(self, new_x):
    print("base class setter called")
    self._x = new_x

class derived(base):
  def __init__(self):
    super().__init__()
    self.x = 1

  @property
  def x(self):
    print("derived class getter called")

  @x.setter
  def x(self, new_x):
    pass

var = derived()

print(var.x)