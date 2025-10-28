# python modules
import socket
import time
import unittest

# local modules
import config
import database
import descriptor_data
import game_data
import mudlog
import nanny
import pc_data
import server
import telnet

# this is the game loop, for reference
# try:
#   loops_per_second = 30
#   time_per_loop = float(1)/float(loops_per_second)
#
#   while not network.shutdown_cmd and not network.copyover_cmd:
#     network.loop(mud, db)
#     time.sleep(time_per_loop)
#     mud.heartbeat(db)
#     mud.call_hbeat_procs(db)


class TestNanny(unittest.TestCase):
  def test_login(self):
    mudlog.info(f"OurouborosMUD {config.OMUD_VERSION}")
    
    # create game server
    network = server.server()

    # create world
    mud = game_data.game_data()

    # fire up database
    db = database.database(":memory:")
    db.connect()
    db.create_tables()

    # set the mud up on the port
    mudlog.info(f"Running game on port 1234.")
    network.boot("0.0.0.0", 1234)

    # create a connection
    client = socket.socket()
    #client.setblocking(False)
    client.connect(('localhost', 1234))

    # perform one game loop
    network.loop(mud, db)

    # should receive do_ttype and GREETINGS
    print(client.recv(1024)[5:].decode("utf-8"))

    d = network._descriptors[0]
    print(d.debug())

    # enter name
    client.send(b"Kyle\r\n")
    time.sleep(0.5)

    network.loop(mud, db)
    mud.heartbeat(db)

    time.sleep(0.5)

    # client asked to confirm name
    print(client.recv(1024))

    time.sleep(0.5)

    # perform another game loop
    network.loop(mud, db)
    mud.heartbeat(db)

    time.sleep(0.5)

    # confirm name
    client.send(b"y\r\n")

    time.sleep(0.5)

    network.loop(mud, db)
    mud.heartbeat(db)

    time.sleep(0.5)

    # client asked to enter password
    print(client.recv(1024))

    network.loop(mud, db)
    mud.heartbeat(db)

    time.sleep(0.5)

    # perform another game loop
    network.loop(mud, db)
    mud.heartbeat(db)

    time.sleep(0.5)

    print(d.debug())

    # give password
    client.send(b"asdf\r\n")

    time.sleep(0.5)

    network.loop(mud, db)
    mud.heartbeat(db)

    time.sleep(0.5)

    print(client.recv(1024))

    print(d.debug())

    network.loop(mud, db)
    mud.heartbeat(db)

    time.sleep(0.5)

    # confirm password
    client.send(b"asdf\r\n")

    time.sleep(0.5)

    print(d.character.debug())

    time.sleep(0.5)

    network.loop(mud, db)
    mud.heartbeat(db)

    time.sleep(0.5)

    print(d.debug())

    # game loop
    network.loop(mud, db)
    mud.heartbeat(db)
    time.sleep(2)

    print(client.recv(1024))

    # teardown
    network.shutdown()
    db.close()
    mudlog.info("Done.")

    client.close()



if __name__ == "__main__":
  unittest.main()