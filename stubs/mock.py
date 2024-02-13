import unittest
from unittest import mock

class A:
	def __init__(self, new_x):
		self.x = new_x

	def double_x(self):
		self.x = self.x * 2

class B:
  def __init__(self):
  	self.Alist = list()

  def add_A(self, new_A):
  	self.Alist.append(new_A)

class TestB(unittest.TestCase):
	def test_B(self):
		A_object = mock.Mock(spec=A)
		
		A_object.double_x()
		A_object.double_x()

		#for key in A_object.__dict__.keys():
			#print(f"{key}: {A_object.__dict__[key]}")

		print(A_object.method_calls[0] == mock.call.double_x)

if __name__ == '__main__':
	unittest.main()