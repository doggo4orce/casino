def f(x):
  return x+1

func = None

try:
  func(3,5)
except TypeError:
  print("type error")
except Exception as e:
  print("other error")
