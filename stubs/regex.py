import re

# pattern = re.compile(r'(?:<c\d+>)+(<c\d+>)')
# print(re.search(pattern, "<c1><c2>").group(0))

lines = [
  "The quick brown ",
  "<p> fox <p>jumped over ",
  "the lazy </p> dog.  <p>",
  "This was funny.</p>"
]

str = '\r\n'.join(lines)

pattern = re.compile(r'((?:\r\n)?)<p>((?:.*?(?:\r\n)?)*?)</p>')

match = re.search(pattern, str)

print(rf"{match}")
print(rf"group 0:{match.group(0)}")
print(rf"group 1:{match.group(1) == ''}")
print(rf"group 2:{match.group(2)}")