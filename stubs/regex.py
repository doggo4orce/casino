import re

pattern = re.compile(r'(?:<c\d+>)+(<c\d+>)')

print(re.search(pattern, "<c1><c2>").group(0))