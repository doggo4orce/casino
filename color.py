# basic 8 foreground colors
NORMAL  = "\x1B[0m"
BLACK   = "\x1B[30m"
RED     = "\x1B[31m"
GREEN   = "\x1B[32m"
YELLOW  = "\x1B[33m"
BLUE    = "\x1B[34m"
MAGENTA = "\x1B[35m"
CYAN    = "\x1B[36m"
WHITE   = "\x1B[37m"

# brightened versions
BRIGHT_BLACK   = "\x1B[1;30m"
BRIGHT_RED     = "\x1B[1;31m"
BRIGHT_GREEN   = "\x1B[1;32m"
BRIGHT_YELLOW  = "\x1B[1;33m"
BRIGHT_BLUE    = "\x1B[1;34m"
BRIGHT_MAGENTA = "\x1B[1;35m"
BRIGHT_CYAN    = "\x1B[1;36m"
BRIGHT_WHITE   = "\x1B[1;37m"

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

# extended 256 colors
ORANGE = u"\u001b[38;5;208m"
DARK_GRAY = u"\u001b[38;5;246m"

if __name__ == '__main__':
  print(f"{RED}red{BRIGHT_RED}bright{NORMAL}")