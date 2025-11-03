class A:
  def __init__(self):
    self.list = list()
    self.idx = 0

  def add_item(self, x):
    self.list.append(x)

  def __iter__(self):
    return self

  def __next__(self):
    if self.idx < 0 or self.idx >= len(self.list):
      raise StopIteration

    ret_val = self.list[self.idx]
    self.idx += 1
    return ret_val
  
  # not needed to iterate over As
  def __contains__(self, object):
    return object in self.list

  def __len__(self):
    return len(self.list)


if __name__ == '__main__':
  new_A = A()

  new_A.add_item("wef")
  new_A.add_item("few")

  print(' '.join(new_A))
