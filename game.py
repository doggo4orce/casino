import baccarat_dealer
import baccarat_table
import cards
import cmd_trig_data
import config
import hbeat_proc_data
import enum
import event_data
import glob
import mudlog
import object_data
import os
import npc_data
import room_data
import table
import string_handling
import zone_data

# TODO : change reference format from global[local] to local@global

class game:
  def __init__(self):
    """Creates a game world with rooms, objects, and characters.
       zones     = list of zone folders which have been loaded from WORLD_FOLDER
       chars     = list of characters (including NPCS and PCs) in the game
       objects   = list of objects which are in the game
       events    = handles all events to take place in the future"""
    self._zones     = dict()
    self._chars     = list()
    self._objects   = list()
    self._events    = event_table_data.event_table_data()

  """add_event(e)               <- add event e to self_events
     heart_beat()               <- calls the event handlers heart_beat() function
     call_hbeat_procs()         <- calls all pulsing special procedures for npcs
     add_zone(zone)             <- adds a zone to the game
     zone_by_id(id)             <- iterate through self.zones zones to find zone with identifier id
     room_by_code(code)         <- look up room using unique_identifier code
     npc_by_code(code)          <- look up npc prototype by code
     obj_by_code(code)          <- look up object prototype by code
     echo_around(ch, hide, msg) <- sends msg to all in room except ch and those in hide list
     add_char(ch)               <- adds character ch to the wld, in the appropriate room or VOID_ROOM
     extract_char(ch)           <- extracts character ch from the wld and the appropriate room
     add_obj(obj)               <- these functions are the same
     extract_obj(obj)           <- except for objects instead
     assign_spec_procs()        <- assigns special procedures to elements of npc_proto
     startup()                  <- loads all of the zone folders in WORLD_FOLDER
     load_npc(code)             <- looks up the npc in self.npc_proto and returns it or None
     load_obj(vnum)             <- looks up the obj in self.objs and return a copy or None
     pc_by_id(id)               <- searches chars for a pc with id and returns it if found
     lose_link(ch)              <- disconnects player from their d (seen by players)
     reconnect(d, ch)           <- reconnects player to their d (seen by players)"""

  def add_event(self, e):
    self._events.add_event(e)

  def heart_beat(self, db):
    self._events.heartbeat(self, db)

  def call_hbeat_procs(self, db):
    for mob in self._chars:
      if isinstance(mob, npc_data.npc_data):
        mob.call_hbeat_procs(self, db)

  def add_zone(self, zn):
    if self.zone_by_id(zn.id) == None:
      self._zones[zn.id] = zn
    else:
      logging.warning(f"Trying to add zone {zn.name} but id '{zn.id}'' but already exists.")

  def zone_by_id(self, id):
    if id not in self._zones.keys():
      return None
    return self._zones[id]

  def room_by_uid(self, uid):
    zone_id = uid.zone_id
    room_id = uid.id

    if zone_id == None or id == None:
      return None

    zone = self.zone_by_id(zone_id)

    if zone == None:
      return None
    
    return zone.room_by_id(room_id)
    
  def npc_by_uid(self, uid):
    zone_id, npc_id = string_handling.parse_reference(uid)

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
    zone = self.zone_by_id("stockville")

    # todo, give out warning and avoid crash if these references don't exist
    b_dealer = self.npc_by_code('stockville[baccarat_dealer]')

    b_dealer.assign_spec_proc(cmd_trig_data.prefix_cmd_trig_data(
      "baccarat syntax handling", 
      baccarat_dealer.baccarat_dealer_syntax_parser
    ))
    b_dealer.assign_spec_proc(cmd_trig_data.prefix_cmd_trig_data(
      "baccarat shoe history",
      baccarat_dealer.baccarat_dealer_history
    ))
    b_dealer.assign_spec_proc(cmd_trig_data.suffix_cmd_trig_data(
      "baccarat dealer greeting",
      baccarat_dealer.baccarat_dealer_intro
    ))
    b_dealer.assign_spec_proc(hbeat_proc_data.hbeat_proc_data(
      "baccarat deals a shoe",
      baccarat_dealer.baccarat_dealing
    ))

    b_table = self.obj_by_code('stockville[baccarat_table]')
    b_table.assign_spec_proc(cmd_trig_data.prefix_cmd_trig_data(
      "baccarat table syntax parser",
      baccarat_table.baccarat_table_syntax_parser
    ))

  def load_world(self, db):
    db.load_world(self)

  def startup(self):
    self.assign_spec_procs()

    # populating world manually at startup
    b_dealer = self.load_npc('stockville[baccarat_dealer]')
    b_dealer = cards.card_dealer.from_npc(b_dealer)
    b_dealer = baccarat_dealer.baccarat_dealer.from_card_dealer(b_dealer)
    b_dealer.room = structs.unique_identifier.from_string('stockville[casino]')
    b_dealer.bac_state = baccarat_dealer.baccarat_dealer_state.BEGIN_SHOE
    self.add_char(b_dealer)

    baker = self.load_npc('stockville[baker]')
    baker.room = structs.unique_identifier.from_string('stockville[recall]')
    self.add_char(baker)

    bottle = self.load_obj('stockville[bottle]')
    bottle.room = structs.unique_identifier.from_string('stockville[recall]')
    self.add_obj(bottle)

    b_table = self.load_obj('stockville[baccarat_table]')
    b_table = table.table.from_obj(b_table)
    b_table = baccarat_table.baccarat_table.from_table(b_table)
    b_table.dealer = b_dealer
    b_table.room = structs.unique_identifier.from_string('stockville[casino]')
    self.add_obj(b_table)

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
      logging.warning(f"Trying to load object [{code}] which was not found.")
      return None

    new_obj = object.object(proto_type)
    
    return new_obj

  def pc_by_id(self, id):
    for ch in self._chars:
      if type(ch) == pc.pc and ch.id == id:
        return ch
    return None

  def lose_link(self, ch):
    self.room_by_code(ch.room).echo(f"{ch} has lost his link.\r\n")
    ch.descriptor = None

  def reconnect(self, d, ch):
    # they might already have a connection
    if ch.descriptor:
      # if so, kick it off
      ch.descriptor.disconnected = True
      ch.descriptor.character = None
    # now connect to the linkless char
    d.character = ch
    ch.descriptor = d

if __name__ == '__main__':
  pass