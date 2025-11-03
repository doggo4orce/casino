
class SomeClass:
  def __init__(self):
    self.x = 1
    self.y = 2

  @property
  def x(self):
    return self._x

  @property
  def y(self):
    return self._y

  @x.setter
  def x(self, new_x):
    self._x = new_x

  @y.setter
  def y(self, new_y):
    self._y = new_y

z = SomeClass()

print(z.__dict__)