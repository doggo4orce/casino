import logging
import os
import select
import socket

from color import *
import config
import descriptor
import nanny
import pbase
import telnet
from typing import NamedTuple

class conn(NamedTuple):
  socket: socket.socket
  host: str

class server:
  GREETINGS = """                      OurouborosMud


By what name do you wish to be known? """

  def __init__(self):
    self.descriptors = {}
    self.new_connections = []
    self.disconnects = []
    self.just_leaving = []
    self.nextid = 0
    self.shutdown_cmd = False
    self.copyover_cmd = False

  def copyover_recover(self, mud, file):
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
        d.char = pbase.load_char_by_name(name)
        d.char.d = d

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
    d.socket.shutdown(1)
    d.socket.close()
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
      self.descriptors[id].socket.detach()

  def prepare_for_shutdown(self):
    for id in self.descriptors:
      self.descriptors[id].socket.shutdown(1)
      self.descriptors[id].socket.close()

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
      logging.info(f"Closing link to {d.client_info.host_name}.")
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

  def parse_telnet_q(self):
    for d in self.descriptors.values():
      if not d.disconnected:
        d.parse_telnet_q()

  def parse_input(self):
    for d in self.descriptors.values():
      if not d.disconnected:
        d.parse_input()

  def process_input(self, d, mud):
    nanny.handle_next_input(d, self, mud)

  def process_inputs(self, mud):
    for d in self.descriptors.values():
      self.process_input(d, mud)

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

  def loop(self, mud):
    # handle any new conections
    self.check_new_connections()
    self.handle_new_connections()

    # handle input
    self.poll_for_input()
    self.parse_input()
    self.process_telnet_qs()
    self.process_inputs(mud)

    # flush output with prompts if necessary
    self.write_prompts()
    self.flush_output()

    # check for lost connections
    self.check_for_disconnects()
    self.handle_disconnects(mud)

    # remove players who quit
    self.handle_quits()
