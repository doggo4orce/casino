import re
import string_handling

str = ":) +------+ (*)=(*) ASCII ART 1 + 2 = 3<p> Hello,   buddy I         miss you !     Oh I     forgot to  close \
the paragraph . </p>"

pattern = re.compile(r'((?:\r\n)?){}((?:.*?(?:\r\n)?)*?){}((?:\r\n)?)'.format(
	'<p>', '</p>'))

match = re.search(pattern, str)

j = match.span()[0]

paragraph = string_handling.proofread(match.group(2))
print(paragraph)
#print(match.span()[0])