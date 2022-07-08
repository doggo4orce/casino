class A:
  def __init__(self, x, y):
    self._private_x = x
    self._private_y = y

class B(A):
  def __init__(self, x, y, z):
    super().__init__(x,y)
    self._private_z = z

  @classmethod
  def from_A(cls, old_a, z):
    ret_val = cls(self, old_a.x, old_a.y)
    ret_val._private_z = z
    return ret_val

class C(B):
  def __init__(self, x, y, z, w):
  	super().__init__(x,y,z)
  	self._private_w = w

  @classmethod
  def from_B(cls, old_b, w):
  	ret_val = cls(old_b.x, old_b.y, old_b.z)
  	ret_val._private_w = w
  	return ret_val
