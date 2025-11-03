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

class B:
  def __init__(self, new_x, new_y):
    self.inner = A(new_x, new_y)


weffer = B(2,3)

weffer.wef = "hello"

print(vars(weffer))

weffer.inner.z = None

print(vars(weffer))