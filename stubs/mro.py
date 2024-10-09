
class Left(object):
  def __init__(self):
    super(Left, self).__init__()
    print("left")

class Right(object):
  def __init__(self):
    super(Right, self).__init__()
    print("right")

class Child(Left, Right):
  def __init__(self):
    super(Child, self).__init__()
    print("child")

x = Child()