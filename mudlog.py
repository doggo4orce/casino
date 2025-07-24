import enum
import logging

# structure of log timestamps
logging.basicConfig(
  level=logging.INFO,
  format='%(asctime)s :: %(message)s',
  datefmt='%b %d %H:%M:%S',
)

class mudlog_type(enum.IntEnum):
  INFO = 0
  WARNING = 1
  ERROR = 2

def mudlog(type, msg):

  match type:
    case mudlog_type.INFO:
      log_func = logging.info
      msg = f"INFO: {msg}"
    case mudlog_type.WARNING:
      log_func = logging.warning
      msg = f"WARNING: {msg}"
    case mudlog_type.ERROR:
      log_func = logging.error
      msg = f"ERROR: {msg}"
    case _:
      logging.error(f"Unrecognized log type {type} received, assuming error.")
      log_func = logging.error

  lines = msg.split("\r\n")

  # TODO: remove time stamps on subsequent lines while preserving formatting
  log_func(lines[0])

  if len(lines) > 1:
    for line in lines[1:]:
      print(f"{15*'-'} :: {line}")

def info(msg):
  mudlog(mudlog_type.INFO, msg)

def warning(msg):
  mudlog(mudlog_type.WARNING, msg)

def error(msg):
  mudlog(mudlog_type.ERROR, msg)