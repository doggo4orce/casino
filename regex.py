import re
import string_handling

str = r'verbatim<p>Go\r\nto the\r\nstore</p>ascii'

pattern = re.compile(
      r'((?:\r\n)?){}((?:.*?(?:\r\n)?)*?){}((?:\r\n)?(?:.*))'.format(
        '<p>',
        '</p>')
    )

match = re.search(pattern, str)

print(f"Group 0: {repr(match.group(0))}")
print(f"Group 1: {repr(match.group(1))}")
print(f"Group 2: {repr(match.group(2))}")
print(f"Group 3: {repr(match.group(3))}")
# print(f"Group 4: {repr(match.group(4))}")