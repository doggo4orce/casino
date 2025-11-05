from color import *

# python modules
import os
import select
import socket
import telnet
import typing

# local modules
import config
import database
import descriptor_data
import mudlog
import nanny
import pc_data
import unique_id_data

class conn(typing.NamedTuple):
  socket: socket.socket
  host: str

class server:
  """Creates a server to keep track of client connections (descriptors).
     descriptors     = dict of connected clients handled (key = descriptor ID)
     new_connections = recent connections yet to be handled
     disconnects     = list of clients who have lost their connection
     just_leaving    = list of clients who chose to quit the game
     nextid          = ID to be assigned to next descriptor
     shutdown_cmd    = check whether someone used shutdown command
     copyover_cmd    = check whether someone used copyover command"""
  def __init__(self):
    self.mother          = None
    self._descriptors     = dict()
    self._new_connections = list()
    self._disconnects     = list()
    self._just_leaving    = list()
    self._nextid          = 0
    self.shutdown_cmd     = False
    self.copyover_cmd     = False



  @property
  def descriptors(self):\
    return self._descriptors

  """copyover_recover(mud,file,db) <- pause all connections, reboot game, and restore them
     add_descriptor(d)             <- add new client to descriptors and assign it's ID
     remove_descriptor_by_id(id)   <- delete descriptor from descriptors
     greet_descriptor(d)           <- send GREETINGS (config.py)
     shutdown()                    <- prepare for shutdown or copyover
     prepare_for_copyover()        <- detach all sockets in self.descriptors
     prepare_for_shutdown()        <- detach all sockets in self.descriptors
     boot(domain, port)            <- bind mother to (domain,port) and listen
     check_new_connections()       <- accepts pending connections, adds to new_connections
     handle_new_connections()      <- transfers from new_connections to descriptors and greets
     check_for_disconnects()       <- appends anyone with disconnected flag to disconnects
     handle_disconnects()          <- calls lose_link and removes disconnected descriptors
     quit(d)                       <- adds d.id to self._just_leaving
     handle_quits()                <- removes anyone self._just_leaving from descriptors
     poll_for_input(timeout)       <- call's each descriptor's poll_for_input function
     flush_output()                <- flush every descriptor's output
     write_prompts()               <- write prompts to descriptors who have processed output
     process_inputs(mud, db)       <- process input from all descriptors
     write_all(msg,exceptions)     <- write message to all descriptors
     send_all(bytes)               <- send bytes to all descriptors (bypasses out_buffer)
     process_telnet_qs()           <- process parsed telnet commands from each descriptor
     loop(mud,db)                  <- run through game loop (frequency determined in main.py)"""

  def copyover_recover(self, mud, file, db):
    mudlog.info("Recovering from Copyover.")

    with open(file) as rf:
      for line in rf:
        fd, name, typ, host, ttype, twidth, tlength = line.split()

        fd = int(fd)
        typ = int(typ)

        s = socket.socket(socket.AF_INET, typ, 0, fd)
        s.setblocking(False)

        d = descriptor_data.descriptor_data(s, host)

        d.state = descriptor_data.descriptor_state.CHATTING

        d.client.term_type = ttype
        d.client.term_width = twidth
        d.client.term_length = tlength

        # telnet won't send ttype again, and other clients send different data if you ask a second time
        d.send(bytes(telnet.do_naws))
        d.has_prompt = True

        # this needs to be factored through other code from when players enter the game?
        d.character = pc_data.pc_data()

        db.load_player(d.character, db.player_id_by_name(name))
        d.character.descriptor = d

        # put them in the start room for now
        uid = unique_id_data.unique_id_data.from_string(config.STARTING_ROOM)

        room = mud.room_by_uid(uid)
        mud.add_character_to_room(d.character, room)

        # add them to the game's list of descriptors
        self.add_descriptor(d)

    mudlog.info("Removing old Copyover File.")
    os.remove(config.COPYOVER_PATH)

  def add_descriptor(self, d):
    self._descriptors[self._nextid] = d
    d.id = self._nextid
    self._nextid += 1

  def remove_descriptor_by_id(self, id):
    d = self.descriptors[id]
    d.close()
    del self.descriptors[id]

  def greet_descriptor(self, d):
    d.send(bytes(telnet.do_ttype) + bytes(telnet.do_naws))
    d.write(config.GREETINGS)
    d.state = descriptor_data.descriptor_state.GET_NAME
    d.has_prompt = True # prompt is built-in to GREETINGS

  def shutdown(self):
    if self.copyover_cmd:
      self.prepare_for_copyover()
    elif self.shutdown_cmd:
      self.prepare_for_shutdown()

    self.mother.close()

  def prepare_for_copyover(self):
    for id in self.descriptors:
      self.descriptors[id].detach()
    # self._mother.close() ?

  def prepare_for_shutdown(self):
    for id in self.descriptors:
      self.descriptors[id].close()
    # self._mother.close() ?

  def boot(self, domain, port):
    mudlog.info("Opening mother connection.")
    self.mother = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.mother.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    mudlog.info("Binding to all IP interfaces on this host.")
    self.mother.bind((domain, port))
    self.mother.listen(1)
    self.mother.setblocking(False)

  def check_new_connections(self):
    while True:
      rlist, wlist, xlist = select.select([self.mother], [], [], 0)

      if not self.mother in rlist:
        break

      remote_sock, remote_addr = self.mother.accept()
      remote_sock.setblocking(False)

      addr, _ = remote_addr
      
      try:
        host = socket.gethostbyaddr(addr)[0]
      except Exception:
        host = "unresolved_host"

      mudlog.info(f"New connection from {host}.")
      self._new_connections.append(conn(remote_sock, host))

  def handle_new_connections(self):
    for cn in self._new_connections:
      d = descriptor_data.descriptor_data(cn.socket, cn.host)
      self.add_descriptor(d)
      self.greet_descriptor(d)

    self._new_connections.clear()

  def check_for_disconnects(self):
    for d in self._descriptors.values():
      if d.disconnected:
        self._disconnects.append(d.id)

  def handle_disconnects(self, mud):
    for id in self._disconnects:
      d = self._descriptors[id]
      mudlog.info(f"Closing link to {d.client.term_host}.")
      # if they were already logged in, their char is linkless
      if d.char:
        mud.lose_link(d.char)
      # if they were writing, it's gone
      if d.writing:
        d.write_buffer = None
      self.remove_descriptor_by_id(id)
    self._disconnects.clear()

  def quit(self, d):
    self._just_leaving.append(d.id)

  def handle_quits(self):
    for id in self._just_leaving:
      d = self._descriptors[id]
      mudlog.info(f"{d.character.name} has left the game.")
      self.remove_descriptor_by_id(id)

    self._just_leaving.clear()

  def poll_for_input(self):
    for id in self._descriptors:
      if not self._descriptors[id].disconnected:
        self._descriptors[id].poll_for_input()

  # should be deleted i think
  # def parse_telnet_q(self):
  #   for d in self.descriptors.values():
  #     if not d.disconnected:
  #       d.parse_telnet_q()

  # should be deleted i think
  # def parse_input(self):
  #   for d in self.descriptors.values():
  #     if not d.disconnected:
  #       d.parse_input()

  def flush_output(self):
    for d in self._descriptors.values(): 
      d.flush_output()

  def write_prompts(self):
    for d in self._descriptors.values():
      if not d.has_prompt:
        d.write_prompt()

  def process_inputs(self, mud, db):
    for d in self._descriptors.values():
      nanny.handle_next_input(d, self, mud, db)

  def write_all(self, msg, exceptions=None):
    if exceptions is None:
      exceptions = []

    for d in self._descriptors.values():
      if d not in exceptions:
        d.write(msg)

  def send_all(self, bytes):
    for d in self._descriptors.values():
      d.send(bytes)

  def process_telnet_qs(self):
    for d in self._descriptors.values():
      d.process_telnet_q()

  def loop(self, mud, db):
    # handle any new conections
    self.check_new_connections()
    self.handle_new_connections()

    # handle input
    self.poll_for_input()
#    self.parse_input()
    self.process_telnet_qs()
    self.process_inputs(mud, db)

    # flush output with prompts if necessary
    self.write_prompts()
    self.flush_output()

    # check for lost connections
    self.check_for_disconnects()
    self.handle_disconnects(mud)

    # remove players who quit
    self.handle_quits()
