class A:
  def __init__(self, new_x, new_y):
    self.x = new_x
    self.y = new_y

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

x = A(2,3)

print(vars(x))