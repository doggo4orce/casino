class A:
  var = 5


class B(A):
  var = 6

x = B()

# outputs 6
print(x.var)
