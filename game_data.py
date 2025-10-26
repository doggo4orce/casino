import baccarat_dealer_data
import baccarat_table
import cards
import cmd_trig_data
import config
import hbeat_proc_data
import enum
import event_table_data
import glob
import mudlog
import object_data
import os
import npc_data
import room_data
import table_data
import string_handling
import zone_data

class game_data:
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

  """add_event(event)           <- add event to table
     list_events()              <- returns list of events in table
     num_events()               <- counts number of events in table
     cancel_event(event)        <- removes an event from table
     add_zone(zone)             <- adds a zone to the game
     list_zones()               <- returns list of zones in game
     num_zones()                <- counts zones in game
     zone_by_id(id)             <- iterate through self.zones zones to find zone with identifier id
     delete_zone(zone)          <- remove zone from game
     room_by_uid(zone_id, id)   <- look up room using uid
     npc_by_uid(zone_id, id)    <- look up npc prototype by code
     obj_by_uid(zone_id, id)    <- look up object prototype by code
     echo_around(ch, hide, msg) <- sends msg to all in room except ch and those in hide list
     add_char(ch)               <- add character to game, in ch.room or VOID_ROOM
     extract_char(ch)           <- extracts character from the game
     add_obj(obj)               <- these functions are the same
     extract_obj(obj)           <- except for objects instead
     assign_spec_procs()        <- assign special procedures to elements of npc_proto
     startup()                  <- populate world and call assign_spec_procs()
     load_npc(zone_id, id)      <- instantiate npc from prototype
     load_obj(zone_id, id)      <- instantiate obj from prototype
     pc_by_id(id)               <- look up pc in game with id
     lose_link(ch)              <- disconnects player from their d (seen by players)
     reconnect(d, ch)           <- reconnects player to their d (seen by players)
     heartbeat()                <- calls the event handlers heart_beat() function
     call_hbeat_procs(db)       <- calls all pulsing special procedures for npcs"""

  def add_event(self, event):
    self._events.add_event(event)

  def list_events(self):
    return self._events.list_events()

  def num_events(self):
    return self._events.num_events()

  def cancel_event(self, event):
    self._events.cancel_event(event)

  def add_zone(self, zone):
    if self.zone_by_id(zone.id) == None:
      self._zones[zone.id] = zone
    else:
      mudlog.error(f"Trying to add zone {zone.name} but id '{zone.id}' but already exists.")

  def list_zones(self):
    return [zone for zone in self._zones.values()]

  def num_zones(self):
    return len(self.list_zones())

  def zone_by_id(self, id):
    if id not in self._zones.keys():
      return None
    return self._zones[id]

  def delete_zone(self, zone):
    try:
      del self._zones[zone.id]
    except KeyError:
      mudlog.error(f"Trying to delete zone {zone} which did not exist!")

  def room_by_uid(self, zone_id, id):
    if zone_id == None or id == None:
      return None

    zone = self.zone_by_id(zone_id)

    if zone == None:
      return None
    
    return zone.room_by_id(id)
    
  def npc_by_uid(self, zone_id, id):
    if zone_id == None or id == None:
      return None

    zone = self.zone_by_id(zone_id)

    if zone == None:
      return None

    return zone.npc_by_id(id)

  def obj_by_uid(self, zone_id, id):
    if zone_id == None or id == None:
      return None

    zone = self.zone_by_id(zone_id)

    if zone == None:
      return None

    return zone.obj_by_id(id)

  def echo_around(self, ch, hide, msg):
    if hide == None:
      hide = [ ]
      
    hide_from.append(ch)
    self.room_by_uid(ch.room.zone_id, ch.room.id).echo(msg, exceptions = hide_from)

  def add_char(self, ch):
    void = unique_id_data.unique_id_data.from_string(config.VOID_ROOM)

    # place them in the world
    self._chars.append(ch)

    # if either zone or room code doesn't exist, move them to the VOID
    if ch.room == None or ch.room.zone_id == None or ch.room.id == None:
      ch.room = void

    # now find the actual room
    room = self.room_by_uid(ch.room.zone_id, ch.room.id)

    # if the room doesn't exist, again move them to the VOID
    if room == None:
      uid = unique_id_data.unique_id_data.from_string(config.VOID_ROOM)
      room = self.room_by_uid(uid.zone_id, uid.id)

    # finally we have somewhere to add them!
    room.add_char(ch)

  def extract_char(self, ch):
    # if they are in a room, remove them from that room
    if ch.room != None:
      uid = ch.room
      self.room_by_uid(uid.zone_id, uid.id).remove_char(ch)
    # now remove them from the world
    self._chars.remove(ch)

  def add_obj(self, obj):
    self._objects.append(obj)
    uid = obj.room
    room = self.room_by_uid(uid.zone_id, uid.id)
    if room != None:
      room.add_obj(obj)

  def extract_obj(self, obj):
    for ch in self._chars:
      if obj in ch.inventory:
        ch.inventory.remove(obj)

    if obj.room != None:
      self.room_by_code(ch.room).remove_obj(obj)

    self._objects.remove(obj)

  def assign_spec_procs(self):
    zone = self.zone_by_id("stockville")

    # todo, give out warning and avoid crash if these references don't exist
    b_dealer = self.npc_by_code('stockville[baccarat_dealer]')

    b_dealer.assign_spec_proc(
      cmd_trig_data.prefix_cmd_trig_data(
        "baccarat syntax handling", 
        baccarat_dealer.baccarat_dealer_syntax_parser
      )
    )
    b_dealer.assign_spec_proc(
      cmd_trig_data.prefix_cmd_trig_data(
        "baccarat shoe history",
        baccarat_dealer.baccarat_dealer_history
      )
    )
    b_dealer.assign_spec_proc(
      cmd_trig_data.suffix_cmd_trig_data(
        "baccarat dealer greeting",
        baccarat_dealer.baccarat_dealer_intro
      )
    )
    b_dealer.assign_spec_proc(
      hbeat_proc_data.hbeat_proc_data(
        "baccarat deals a shoe",
        baccarat_dealer.baccarat_dealing
      )
    )

    b_table = self.obj_by_uid('stockville', 'baccarat_table')

    b_table.assign_spec_proc(
      cmd_trig_data.prefix_cmd_trig_data(
        "baccarat table syntax parser",
        baccarat_table.baccarat_table_syntax_parser
      )
    )

  def load_world(self, db):
    db.load_world(self)

  def startup(self):
    self.assign_spec_procs()

    # populating world manually at startup
    b_dealer = self.load_npc('stockville', 'baccarat_dealer')
    b_dealer = cards.card_dealer.from_npc(b_dealer)
    b_dealer = baccarat_dealer.baccarat_dealer.from_card_dealer(b_dealer)
    b_dealer.room = unique_id_data.unique_id_data('stockville', 'casino')
    b_dealer.bac_state = baccarat_dealer.baccarat_dealer_state.BEGIN_SHOE
    self.add_char(b_dealer)

    baker = self.load_npc('stockville', 'baker')
    baker.room = unique_id_data.unique_id_data('stockville', 'recall')
    self.add_char(baker)

    bottle = self.load_obj('stockville', 'bottle')
    bottle.room = unique_id_data.unique_id_data('stockville', 'recall')
    self.add_obj(bottle)

    b_table = self.load_obj('stockville', 'baccarat_table')
    b_table = table.table.from_obj(b_table)
    b_table = baccarat_table.baccarat_table.from_table(b_table)
    b_table.dealer = b_dealer
    b_table.room = unique_id_data.unique_id_data('stockville', 'casino')
    self.add_obj(b_table)

  def load_npc(self, zone_id, id):
    proto_type = self.npc_by_uid(zone_id, id)

    if proto_type == None:
      logging.warning(f"Trying to load npc [{code}] which was not found.")
      return None

    return npc_data.npc_data(proto_type)

  def load_obj(self, zone_id, id):
    proto_type = self.obj_by_uid(zone_id, id)

    if proto_type == None:
      logging.warning(f"Trying to load object [{code}] which was not found.")
      return None

    return object.object(proto_type)

  def pc_by_id(self, id):
    for ch in self._chars:
      if type(ch) == pc_data.pc_data and ch.id == id:
        return ch
    return None

  def lose_link(self, ch):
    self.room_by_uid(ch.room.zone_id, ch.room.id).echo(f"{ch} has lost his link.\r\n")
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

  def heartbeat(self, db):
    self._events.heartbeat(self, db)

  def call_hbeat_procs(self, db):
    for mob in self._chars:
      if isinstance(mob, npc_data.npc_data):
        mob.call_hbeat_procs(self, db)

if __name__ == '__main__':
  pass