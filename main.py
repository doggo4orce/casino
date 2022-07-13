import argparse
import logging
import os
import time

import config
import nanny
import game
import pbase
import server


# structure of log timestamps
logging.basicConfig(
  level=logging.INFO,
  format='%(asctime)s :: %(message)s',
  datefmt='%b %d %H:%M:%S',
)

# command line argument handling
parser = argparse.ArgumentParser(description='oMud Server')

parser.add_argument('port', type=int, help='port to run the server on')
parser.add_argument('-c', type=str, metavar='copyover_file', help='run the MUD using copyover (not intended for manual use')
parser.add_argument('-a', help='the MUD is being run from the autorun script')

cl_dict = vars(parser.parse_args())

logging.info("OurouborosMUD {}".format(config.OMUD_VERSION))
o_mud = game.game()
o_mud.startup()

mud_server = server.server()

logging.info(f"Running game on port {cl_dict['port']}")
mud_server.boot("0.0.0.0", cl_dict['port'])

# todo, call (and write) a function here which verifies that ever plr on the index actually exists a a .plr file
pbase.check_file_structure()
pbase.load_ptable()

# loading commands
nanny.init_commands()

if cl_dict['c'] != None:
  mud_server.copyover_recover(o_mud, cl_dict['c'])

try:
  loops_per_second = 10
  time_per_loop = float(1)/float(loops_per_second)

  while not mud_server.shutdown_cmd and not mud_server.copyover_cmd:
    mud_server.loop(o_mud)
    time.sleep(time_per_loop)
    o_mud.heart_beat()
    o_mud.call_heart_beat_procs()
    # TODO: find out how long this function took to call and adjust sleep time accordingly

except KeyboardInterrupt:
  logging.error("SYSERR: Received SIGHUP, SIGINT, or SIGTERM.  Shutting down...")

else:
  mud_server.shutdown()

  if mud_server.copyover_cmd:
    os.system(f"python3.7 main.py -c {config.COPYOVER_PATH} {cl_dict['port']}")
  else:
    logging.info("Done.")