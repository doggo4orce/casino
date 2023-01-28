# normal text color
NORMAL  = "\x1B[0m"

def ansi_color_sequence(num):
  if num == 0:
    return NORMAL

  return u"\u001b[38;5;{}m".format(num)

# basic 8 foreground colors
# BLACK   = ansi_color_sequence(0)
# for now, 0 reserved for NORMAL
RED     = ansi_color_sequence(1)
GREEN   = ansi_color_sequence(2)
YELLOW  = ansi_color_sequence(3)
BLUE    = ansi_color_sequence(4)
MAGENTA = ansi_color_sequence(5)
CYAN    = ansi_color_sequence(6)
WHITE   = ansi_color_sequence(7)

# brightened versions
BRIGHT_BLACK   = ansi_color_sequence(8)
BRIGHT_RED     = ansi_color_sequence(9)
BRIGHT_GREEN   = ansi_color_sequence(10)
BRIGHT_YELLOW  = ansi_color_sequence(11)
BRIGHT_BLUE    = ansi_color_sequence(12)
BRIGHT_MAGENTA = ansi_color_sequence(13)
BRIGHT_CYAN    = ansi_color_sequence(14)
BRIGHT_WHITE   = ansi_color_sequence(15)

# extended 256 colors
ORANGE    = ansi_color_sequence(208)
DARK_GRAY = ansi_color_sequence(246)

# background colors
BKGD_BLACK   = "\x1B[40m"
BKGD_RED     = "\x1B[41m"
BKGD_GREEN   = "\x1B[42m"
BKGD_YELLOW  = "\x1B[43m"
BKGD_BLUE    = "\x1B[44m"
BKGD_MAGENTA = "\x1B[45m"
BKGD_CYAN    = "\x1B[46m"
BKGD_WHITE   = "\x1B[47m"

# special sequences
UNDERLINE = "\x1B[4m"
FLASH = "\x1B[5m"
REVERSE = "\x1B[6m"



if __name__ == '__main__':
  print(f"{RED}red{BRIGHT_RED}bright{NORMAL}test")