import unittest

class parent:
  def __init__(self, name=None, age=None):
    self.name = name
    self.age = age

  def copy_from(self, other):
    self.name = other.name
    self.age = other.age

class child(parent):
  def __init__(self, name=None, age=None, hp=None, mp=None, mv=None):
    super().__init__(name, age)
    self.hp = hp
    self.mp = mp
    self.mv = mv

  def copy_from(self, other):
    super().copy_from(other)
    self.hp = other.hp
    self.mp = other.mp
    self.mv = other.mv

  @classmethod
  def from_parent(cls, p):
    ret_val = cls()
    super(cls, ret_val).copy_from(p)
    return ret_val

class TestCopy(unittest.TestCase):
  def test_copy(self):
    ch = child("roobiki", 40, 20, 100, 100)

    ch2 = child()
    ch2.copy_from(ch)

    self.assertEqual(ch.name, ch2.name)
    self.assertEqual(ch.age, ch2.age)
    self.assertEqual(ch.hp, ch2.hp)
    self.assertEqual(ch.mp, ch2.mp)
    self.assertEqual(ch.mv, ch2.mv)

    p = parent("bob", 50)
    ch3 = child.from_parent(p)

    self.assertEqual(ch3.name, "bob")
    self.assertEqual(ch3.age, 50)
    self.assertIsNone(ch3.hp)
    self.assertIsNone(ch3.mp)
    self.assertIsNone(ch3.mv)

if __name__ == "__main__":
  unittest.main()