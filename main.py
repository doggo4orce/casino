# Python Modules
import argparse
import mudlog
import os
import time

# Local Modules
import config
import database
import game_data
import nanny
import server

# command line argument handling
parser = argparse.ArgumentParser(description='oMud Server')
parser.add_argument('port', type=int, help='port to run the server on')
parser.add_argument('-c', type=str, metavar='copyover_file', help='run the MUD using copyover (not intended for manual use')
parser.add_argument('-a', help='the MUD is being run from the autorun script')
cl_dict = vars(parser.parse_args())

mudlog.info(f"OurouborosMUD {config.OMUD_VERSION}")

# create game server
network = server.server()

# create world
mud = game_data.game_data()

# fire up database
db = database.database(":memory:")
db.connect()
db.create_tables()
db.load_stock()

# load contents of database
mud.load_world(db)

# populate world with npcs/objs and assign spec procs
mud.startup()

mudlog.info(f"Running game on port {cl_dict['port']}.")
network.boot("0.0.0.0", cl_dict['port'])

# loading commands
nanny.init_commands()

if cl_dict['c'] != None:
  network.copyover_recover(mud, cl_dict['c'], db)

try:
  loops_per_second = 10
  time_per_loop = float(1)/float(loops_per_second)

  while not network.shutdown_cmd and not network.copyover_cmd:
    network.loop(mud, db)
    time.sleep(time_per_loop)
    mud.heart_beat(db)
    mud.call_heart_beat_procs(db)
    # TODO: find out how long this function took to call and adjust sleep time accordingly

except KeyboardInterrupt:
  mudlog.error("SYSERR: Received SIGHUP, SIGINT, or SIGTERM.  Shutting down...")

else:
  network.shutdown()
  db.close()

  if network.copyover_cmd:
    os.system(f"python3 main.py -c {config.COPYOVER_PATH} {cl_dict['port']}")
  else:
    mudlog.info("Done.")
