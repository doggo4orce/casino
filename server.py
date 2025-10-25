# python modules
from color import *
import logging
import os
import select
import socket
import telnet
import typing

# local modules
import config
import database
import descriptor
import nanny

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
    self._mother          = None
    self._descriptors     = dict()
    self._new_connections = list()
    self._disconnects     = list()
    self._just_leaving    = list()
    self._nextid          = 0
    self._shutdown_cmd    = False
    self._copyover_cmd    = False

  """copyover_recover(mud,file,db) <- pause all connections, reboot game, and restore them
     add_descriptor(d)             <- add new client to descriptors and assign it's ID
     remove_descriptor_by_id(id)   <- delete descriptor from descriptors
     greet_descriptor(d)           <- send GREETINGS (config.py)
     shutdown()                    <- prepare for shutdown or copyover
     prepare_for_copyover()        <- detach all sockets in self.descriptors
     prepare_for_shutdown()        <- detach all sockets in self.descriptors
     boot(domain,port)             <- bind mother to (domain,port) and listen
     check_new_connections()       <- accepts pending connections, adds to new_connections
     handle_new_connections()      <- transfers from new_connections to descriptors and greets
     check_for_disconnects()       <-
     handle_disconnects()          <-
     handle_quits()
     poll_for_input()
     flush_output()
     write_prompts()
     process_inputs(mud,db)
     write_all(msg,exceptions)
     send_all(bytes)
     process_telnet_qs()
     loop(mud,db)
     """


  def copyover_recover(self, mud, file, db):
    logging.info("Recovering from Copyover.")

    with open(file) as rf:
      for line in rf:
        fd, name, typ, host, ttype, twidth, tlength = line.split()

        fd = int(fd)
        typ = int(typ)

        s = socket.socket(socket.AF_INET, typ, 0, fd)
        d = descriptor.descriptor(s, host)

        d.state = descriptor.descriptor_state.CHATTING

        d.client_info.term_type = ttype
        d.client_info.term_width = twidth
        d.client_info.term_length = tlength

        # telnet won't send ttype again, and other clients send different data if you ask a second time
        d.send(bytes(telnet.do_naws))
        d.has_prompt = True

        # this needs to be factored through other code from when players enter the game?
        d.char = db.load_player(name)
        d.char.d = d

        db.load_flag_prefs(d.char)

        mud.add_char(d.char)
        self.add_descriptor(d)

    logging.info("Removing old Copyover File.")
    os.remove(config.COPYOVER_PATH)

  def add_descriptor(self, d):
    self.descriptors[self.nextid] = d
    d.id = self.nextid
    self.nextid += 1

  def remove_descriptor_by_id(self, id):
    d = self.descriptors[id]
    d.close()
    del self.descriptors[id]

  def greet_descriptor(self, d):
    d.send(bytes(telnet.do_ttype) + bytes(telnet.do_naws))
    d.write(self.GREETINGS)
    d.state = descriptor.descriptor_state.GET_NAME
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
    logging.info("Opening mother connection.")
    self.mother = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.mother.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    logging.info("Binding to all IP interfaces on this host.")
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

      logging.info(f"New connection from {host}.")
      self.new_connections.append(conn(remote_sock, host))

  def handle_new_connections(self):
    for cn in self.new_connections:
      d = descriptor.descriptor(cn.socket, cn.host)
      self.add_descriptor(d)
      self.greet_descriptor(d)

    self.new_connections.clear()

  def check_for_disconnects(self):
    for d in self.descriptors.values():
      if d.disconnected:
        self.disconnects.append(d.id)

  def handle_disconnects(self, mud):
    for id in self.disconnects:
      d = self.descriptors[id]
      logging.info(f"Closing link to {d.client_info.term_host}.")
      # if they were already logged in, their char is linkless
      if d.char:
        mud.lose_link(d.char)
      # if they were writing, it's gone
      if d.writing:
        d.write_buffer = None
      self.remove_descriptor_by_id(id)
    self.disconnects.clear()

  def handle_quits(self):
    for id in self.just_leaving:
      d = self.descriptors[id]
      logging.info(f"{d.char.name} has left the game.")
      self.remove_descriptor_by_id(id)

    self.just_leaving.clear()

  def poll_for_input(self):
    for id in self.descriptors:
      if not self.descriptors[id].disconnected:
        self.descriptors[id].poll_for_input()

  def flush_output(self):
    for d in self.descriptors.values():
      d.flush_output()

  def write_prompts(self):
    for d in self.descriptors.values():
      if not d.has_prompt:
        d.write_prompt()

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

  def process_inputs(self, mud, db):
    for d in self.descriptors.values():
      nanny.handle_next_input(d, self, mud, db)

  def write_all(self, msg, exceptions=None):
    if exceptions is None:
      exceptions = []

    for d in self.descriptors.values():
      if d not in exceptions:
        d.write(msg)

  def send_all(self, bytes):
    for d in self.descriptors.values():
      d.send(bytes)

  def process_telnet_qs(self):
    for d in self.descriptors.values():
      d.process_telnet_q()

  def loop(self, mud, db):
    # handle any new conections
    self.check_new_connections()
    self.handle_new_connections()

    # handle input
    self.poll_for_input()
    self.parse_input()
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
