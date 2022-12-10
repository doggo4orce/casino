import baccarat
import cards
import config
import dataclasses
import enum
import event
import glob
import logging
import object
import os
import pc
import room
import spec_procs
import string_handling
import structs
import zone

class game:
  def __init__(self):
    """Creates a game world with rooms, objects, and characters.
       zones     = a list of zone folders which have been loaded from WORLD_FOLDER
       chars     = a list of characters (including NPCS and PCs) in the game
       objects   = a list of objects which are in the game
       events    = handles all events to take place in the future"""
    self._zones     = dict()
    self._chars     = list()
    self._objects   = list()
    self._events    = event.event_table()

  """add_event(e)            <- add event e to self_events
     heart_beat()            <- calls the event handlers heart_beat() function
     call_heart_beat_procs() <- calls all pulsing special procedures for npcs
     zone_by_id(id)          <- iterate through self.zones zones to find zone with identifier id
     room_by_code(code)      <- look up room using unique_identifier code
     npc_by_code(code)       <- look up npc prototype by code
     obj_by_code(code)       <- look up object prototype by code
     echo_around(ch, hide, msg) <- sends msg to all chars in room except ch and those in hide list
     add_char(ch)            <- adds character ch to the wld, in the appropriate room or VOID_ROOM
     extract_char(ch)        <- extracts character ch from the wld and the appropriate room
     add_obj(obj)            <- these functions are the same
     extract_obj(obj)        <- except for objects instead
     assign_spec_procs()     <- assigns special procedures to elements of npc_proto
     startup()               <- loads all of the zone folders in WORLD_FOLDER
     load_npc(code)          <- looks up the npc in self.npc_proto and returns it or None
     load_obj(vnum)          <- looks up the obj in self.objs and return a copy or None
     read_npc_file(filename) <- reads all the npcs stored in filename
     read_obj_file(filename) <- reads all the objects stored in a filename
     pc_by_id(id)            <- searches chars for a pc with id and returns it if found
     lose_link(ch)           <- disconnects player from their d (seen by players)
     reconnect(d, ch)        <- reconnects player to their d (seen by players)"""

  def add_event(self, e):
    self._events.add_event(e)

  def heart_beat(self):
    self._events.heart_beat(self)

  def call_heart_beat_procs(self):
    for mob in self._chars:
      if isinstance(mob, pc.npc):
        mob.call_heart_beat_procs(self)

  def zone_by_id(self, id):
    if id not in self._zones.keys():
      return None
    return self._zones[id]

  def room_by_code(self, code):
    # expects a structs.unique_identifier() code
    zone_id = code.zone_id
    room_id = code.id

    print(f"room_by_code claled with :zoneid = {zone_id} room_id = {room_id}")
    if zone_id == None and room_id == None:
      return None

    zone = self.zone_by_id(zone_id)

    if zone == None:
      return None

    return zone.room_by_id(room_id)

  def npc_by_code(self, code):
    zone_id, npc_id = string_handling.parse_reference(code)

    if zone_id == None or npc_id == None:
      return None

    zone = self.zone_by_id(zone_id)

    if zone == None:
      return None

    return zone.npc_by_id(npc_id)

  def obj_by_code(self, code):
    zone_id, obj_id = string_handling.parse_reference(code)

    if zone_id == None or obj_id == None:
      return None

    zone = self.zone_by_id(zone_id)
    return zone.obj_by_id(obj_id)

  def echo_around(self, ch, hide_from, msg):
    if hide_from == None:
      hide_from = [ ]
      
    hide_from.append(ch)
    self.room_by_code(ch.room).echo(msg, exceptions = hide_from)

  def add_char(self, ch):
    THE_VOID = structs.unique_identifier.from_string(config.VOID_ROOM)

    # place them in the world
    self._chars.append(ch)

    # check if they have a location
    zone_id = ch.room.zone_id
    room_id = ch.room.id

    # if either zone or room code doesn't exist, move them to the VOID
    if zone_id == None or room_id == None:
      ch.room = THE_VOID

    # now find the actual room
    room = self.room_by_code(ch.room)

    # if the room doesn't exist, again move them to the VOID
    if room == None:
      room = self.room_by_code(structs.unique_identifier.from_string(config.VOID_ROOM))

    # finally we have somewhere to add them!
    room.add_char(ch)

  def extract_char(self, ch):
    # if they are in a room, remove them from that room
    if ch.room != None:
      self.room_by_code(ch.room).remove_char(ch)
    # now remove them from the world
    self._chars.remove(ch)

  def add_obj(self, obj):
    self._objects.append(obj)
    room = self.room_by_code(obj.room)
    if room != None:
      # todo: write room.add_obj(obj) function
      room.inventory.insert(obj)

  def extract_obj(self, obj):
    for ch in self._chars:
      if obj in ch.inventory:
        ch.inventory.remove(obj)

    if obj.room != None:
      self.room_by_code(ch.room).inventory.remove(obj)
    self._objects.remove(obj)

  def assign_spec_procs(self):
    b_dealer = self.npc_by_code('stockville[baccarat_dealer]')
    b_dealer.assign_spec_proc(spec_procs.prefix_command_trigger("baccarat syntax handling", baccarat.baccarat_syntax_parser))
    b_dealer.assign_spec_proc(spec_procs.prefix_command_trigger("baccarat shoe history", baccarat.baccarat_dealer_history))
    b_dealer.assign_spec_proc(spec_procs.suffix_command_trigger("baccarat dealer greeting", baccarat.baccarat_dealer_intro))
    b_dealer.assign_spec_proc(spec_procs.heart_beat_proc("baccarat deals a shoe", baccarat.baccarat_dealing))

  def startup(self):
    for folder in glob.glob(config.WORLD_FOLDER + "*"):
      # all zones are stored in folders so ignore any loose files in here
      if not os.path.isdir(folder):
        continue
      # otherwise we found a new zone
      new_zone = zone.zone()
      new_zone.parse_folder(folder + "/")
      self._zones[new_zone.id] = new_zone

    self.assign_spec_procs()

    # populating world manually at startup
    mob = self.load_npc('stockville[baccarat_dealer]')
    mob = cards.card_dealer.from_npc(mob)
    mob = baccarat.baccarat_dealer.from_card_dealer(mob)
    mob.room = structs.unique_identifier.from_string('stockville[casino]')
    self.add_char(mob)

    mob = self.load_npc('stockville[baker]')
    mob.room = structs.unique_identifier.from_string('stockville[recall]')
    self.add_char(mob)

    bottle = self.load_obj('stockville[bottle]')
    bottle.room = structs.unique_identifier.from_string('stockville[reading]')
    self.add_obj(bottle)

  def load_npc(self, code):
    proto_type = self.npc_by_code(code)

    if proto_type == None:
      logging.warning(f"Trying to load npc [{code}] which was not found.")
      return None

    new_npc = pc.npc(proto_type)

    return new_npc

  def load_obj(self, code):
    proto_type = self.obj_by_code(code)

    if proto_type == None:
      logging.warning(f"Trying to load object [{vnum}] which was not found.")
      return None

    new_obj = object.object(proto_type)
    
    return new_obj

  def read_npc_file(self, filename):
    rf = open(filename, "r")
    while True:
      # expecting #VNUM or $ (final line)
      line = rf.readline()
      # file is terminated with $
      if line[0] == '$':
        return
      # first thing is the virtual number
      vnum = int(line[1:])
      # now read the rest of the mob
      self.npc_proto[vnum] = db.parse_npc(rf)

  def read_obj_file(self, filename):
    rf = open(filename, "r")
    while True:
      # expecting #VNUM or $ (final line)
      line = rf.readline()
      # file is terminated with $
      if line[0] == '$':
        return
      # first thing is the virtual number
      vnum = int(line[1:])
      # now read the rest of the mob
      self.obj_proto[vnum] = db.parse_obj(rf)

  def pc_by_id(self, id):
    for ch in self._chars:
      if type(ch) == pc.pc and ch.id == id:
        return ch
    return None

  def lose_link(self, ch):
    self.wld[ch.room].echo(f"{ch} has lost his link.\r\n")
    ch.d = None

  def reconnect(self, d, ch):
    # they might already have a connection
    if ch.d:
      # if so, kick it off
      ch.d.disconnected = True
      ch.d.char = None
    # now connect to the linkless char
    d.char = ch
    ch.d = d

if __name__ == '__main__':
  mud = game()
  mud.init_wld()
  mud.init_npcs()
  mud.init_objs()
  obj = mud.load_obj(3000)
  npc = mud.load_npc(3001)
  print(mud.room_by_vnum(3001).name)
  print(mud.room_by_vnum(3001).vnum)
  print(str(obj))
  print(mud.obj_by_vnum(3001).entity.ldesc)
  print(str(npc))
  print(mud.npc_by_vnum(3001).entity.ldesc)