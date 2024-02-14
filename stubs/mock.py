import unittest
from unittest.mock import patch, Mock

class A:
	def __init__(self, new_x, a):
		self.x = new_x
		self.temp

	def double_x(self, temp):
		self.x = self.x * 2
		self.temp = temp

class B:
  def __init__(self):
  	self.Alist = list()

  def add_A(self, new_A):
  	self.Alist.append(new_A)

@patch('A')
@patch('B')
def test(MockClass1, MockClass2):
    A()
    B()
    assert MockClass1 is A
    assert MockClass2 is B
    assert MockClass1.called
    assert MockClass2.called

test()

# class TestB(unittest.TestCase):
# 	def test_B(self):
# 		A_object = mock.Mock(spec=A)
		
# 		A_object.double_x(2)

# 		for key in A_object.__dict__.keys():
# 			print(f"{key}: {A_object.__dict__[key]}")

# 		for call in A_object.method_calls:
# 			print(call)

# 		A_object.double_x.assert_called_with(2)

# if __name__ == '__main__':
# 	unittest.main()