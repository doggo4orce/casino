import math
from nanny import cmd_dict

def list_columns(words, cols, gap, leading):

  if cols > len(words):
    cols = len(words)

  max_len = max([len(word) for word in words])

  print(f"The maximum word length is {max_len}.")

  rows = int(math.ceil(float(len(words))/float(cols)))

  plist = [words[i: i + cols] for i in range(0, len(words), cols)]

  print(plist)

  if not len(plist[-1]) == cols:
    plist[-1].extend(['']*(len(words) - len(plist[-1])))
  
  plist = zip(*plist)

  out_str = ""

  for p in plist:
    out_str += leading * ' ' + ''.join([c.ljust(max_len + gap) for c in p]) + '\n'
  
  print(out_str)

class A:
  def __init__(self):
    pass
class B(A):
  def __init__(self):
    super().__init__()
    pass

print(isinstance(B(), A))
