import baccarat_dealer_data
import baccarat_table_data
import baccarat_procs
import card_data
import card_dealer_data
import cmd_trig_data
from color import *
import config
import hbeat_proc_data
import enum
import event_table_data
import glob
import mudlog
import object_data
import os
import npc_data
import pc_data
import room_data
import string_handling
import table_data
import unique_id_data
import zone_data

class game_data:
  def __init__(self):
    """Creates a game world with rooms, objects, and characters.
       zones     = list of zone folders which have been loaded from WORLD_FOLDER
       chars     = list of characters (including NPCS and PCs) in the game
       objects   = list of objects which are in the game
       events    = handles all events to take place in the future
       mini_mode = MUD will not boot from DB"""
    self._zones      = dict()
    self._characters = list()
    self._objects    = list()
    self._events     = event_table_data.event_table_data()
    self._mini_mode  = False

  """add_event(event)                <- add event to table
     list_events()                   <- returns list of events in table
     scheduled(event)                <- check if event is scheduled
     num_events()                    <- counts number of events in table
     cancel_event(event)             <- removes an event from table
     add_zone(zone)                  <- adds a zone to the game
     list_zones()                    <- returns list of zones in game
     num_zones()                     <- counts zones in game
     zone_by_id(id)                  <- search for zone with given id
     delete_zone(zone)               <- remove zone from game
     add_character_to_room(ch, room) <- add character to game in specified room
     list_characters()               <- return list of characters in game
     has_character(ch)               <- check if character is in the game
     num_characters()                <- count the number of characters in the game
     extract_character(ch)           <- extracts character completely from the game
     room_by_uid(zone_id, id)        <- look up room using uid, room_by_uid(uid) also works
     npc_by_uid(zone_id, id)         <- look up npc prototype by code
     obj_by_uid(zone_id, id)         <- look up object prototype by code
     echo_around(ch, hide, msg)      <- sends msg to all in room except ch and those in hide list
     add_obj_to_room(obj, room)      <- put object on the ground in room
     add_obj(obj)                    <- add object to game
     list_objects()                  <- returns list of objects in the game
     extract_obj(obj)                <- except for objects instead
     assign_spec_procs()             <- assign special procedures to elements of npc_proto
     load_world(db)                  <- load world from database
     mini_boot()                     <- create single room world if db fails verification
     startup()                       <- populate world and call assign_spec_procs()
     load_npc(zone_id, id)           <- instantiate npc from prototype
     load_obj(zone_id, id)           <- instantiate obj from prototype
     pc_by_id(id)                    <- look up pc in game with id
     lose_link(ch)                   <- disconnects player from their d (seen by players)
     reconnect(d, ch)                <- reconnects player to their d (seen by players)
     heartbeat()                     <- calls the event handlers heart_beat() function
     call_hbeat_procs(db)            <- calls all pulsing special procedures for npcs"""

  def add_event(self, event):
    self._events.add_event(event)

  def list_events(self):
    return self._events.list_events()

  def scheduled(self, event):
    return event in self.list_events()

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

  def add_character_to_room(self, ch, room):
    ch.room = unique_id_data.unique_id_data(room.zone_id, room.id)
    self._add_character(ch)

  def _add_character(self, ch):
    void = unique_id_data.unique_id_data.from_string(config.VOID_ROOM)

    # place them in the world
    self._characters.append(ch)

    # if either zone or room code doesn't exist, move them to the VOID
    if ch.room is None or ch.room.zone_id is None or ch.room.id is None:
      ch.room = void

    # now find the actual room
    room = self.room_by_uid(ch.room)

    # if the room doesn't exist, again move them to the VOID
    if room == None:
      uid = unique_id_data.unique_id_data.from_string(config.VOID_ROOM)
      room = self.room_by_uid(uid)

    # finally we have somewhere to add them!
    room.add_char(ch)

  def list_characters(self):
    return [ch for ch in self._characters]

  def has_character(self, ch):
    return ch in self.list_characters()

  def num_characters(self):
    return len(self.list_characters())

  def extract_character(self, ch):
    # if they are in a room, remove them from that room
    if ch.room is not None:
      self.room_by_uid(ch.room).remove_char(ch)
    # now remove them from the world
    self._characters.remove(ch)

  def room_by_uid(self, *args):
    if len(args) == 2:
      # room_by_uid(zone_id, id)
      zone_id = args[0]
      id = args[1]
    elif len(args) == 1:
      zone_id = args[0].zone_id
      id = args[0].id

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

  def echo_around(self, ch, hide_from, msg):
    if hide_from == None:
      hide_from = [ ]
      
    hide_from.append(ch)
    self.room_by_uid(ch.room.zone_id, ch.room.id).echo(msg, exceptions = hide_from)

  """Note: One this mud boots, the room field of objects will be removed, as well as
     that of entities, and we will make it so entities just know what inventory they
     are in.  Rooms will have two inventories (one for objects, another for characters)."""
  def add_obj_to_room(self, obj, room):
    obj.room = unique_id_data.unique_id_data(room.zone_id, room.id)
    self.add_obj(obj)

  def add_obj(self, obj):
    void = unique_id_data.unique_id_data.from_string(config.VOID_ROOM)

    # place it in the world
    self._objects.append(obj)

    # if either zone or room code doesn't exist, move it to the VOID
    if obj.room is None or obj.room.zone_id is None or obj.room.id is None:
      obj.room = void

    # now find the actual room
    room = self.room_by_uid(obj.room)

    if room is not None:
      room.add_obj(obj)

  def list_objects(self):
    return [obj for obj in self._objects]

  def extract_obj(self, obj):
    for ch in self._characters:
      if obj in ch.inventory:
        ch.inventory.remove(obj)

    if obj.room is not None:
      self.room_by_uid(obj.room).remove_object(obj)

    self._objects.remove(obj)

  def assign_spec_procs(self):
    zone = self.zone_by_id("stockville")

    # todo, give out warning and avoid crash if these references don't exist
    b_dealer = self.npc_by_uid('stockville', 'baccarat_dealer')

    b_dealer.assign_spec_proc(
      cmd_trig_data.prefix_cmd_trig_data(
        "baccarat syntax handling", 
        baccarat_procs.baccarat_dealer_syntax_parser
      )
    )

    b_dealer.assign_spec_proc(
      cmd_trig_data.prefix_cmd_trig_data(
        "baccarat shoe history",
        baccarat_procs.baccarat_dealer_history
      )
    )

    b_dealer.assign_spec_proc(
      cmd_trig_data.suffix_cmd_trig_data(
        "baccarat dealer greeting",
        baccarat_procs.baccarat_dealer_intro
      )
    )

    b_dealer.assign_spec_proc(
      hbeat_proc_data.hbeat_proc_data(
        "baccarat deals a shoe",
        baccarat_procs.baccarat_dealing
      )
    )

    b_table = self.obj_by_uid('stockville', 'baccarat_table')

    b_table.assign_spec_proc(
      cmd_trig_data.prefix_cmd_trig_data(
        "baccarat table syntax parser",
        baccarat_procs.baccarat_dealer_syntax_parser
      )
    )

  def load_world(self, db):
    db.load_world(self)

  def mini_boot(self):
    self._mini_mode = True

    void = unique_id_data.unique_id_data.from_string(config.VOID_ROOM)

    zone = zone_data.zone_data()
    zone.id = void.zone_id
    zone.name = "Empty World"
    zone.author = "N/A"

    room = room_data.room_data()
    room.id = void.id
    room.zone_id = "stockville"
    room.name = "Empty Room"
    room.desc.text = """You are in this room because the database did not load correctly.\r\n\r\n  <c9>Coming Soon:<c0> more database tools which you can use here to diagnose/fix the problem"""

    zone.add_room(room)
    self.add_zone(zone)

  def startup(self):
    self.assign_spec_procs()

    # populating world manually at startup
    b_dealer = self.load_npc('stockville', 'baccarat_dealer')
    b_dealer = card_dealer_data.card_dealer_data.from_npc(b_dealer)
    b_dealer = baccarat_dealer_data.baccarat_dealer_data.from_card_dealer(b_dealer)
    self.add_character_to_room(b_dealer, self.room_by_uid('stockville', 'casino'))

    baker = self.load_npc('stockville', 'baker')
    self.add_character_to_room(baker, self.room_by_uid('stockville', 'recall'))

    bottle = self.load_obj('stockville', 'bottle')
    bottle.room = unique_id_data.unique_id_data('stockville', 'recall')
    self.add_obj(bottle)

    b_table = self.load_obj('stockville', 'baccarat_table')
    b_table = table_data.table_data.from_obj(b_table)
    b_table.num_seats = 3
    b_table = baccarat_table_data.baccarat_table_data.from_table(b_table)
    b_table.dealer = b_dealer
    b_table.room = unique_id_data.unique_id_data('stockville', 'casino')
    self.add_obj(b_table)

  def load_npc(self, zone_id, id):
    proto_type = self.npc_by_uid(zone_id, id)

    if proto_type == None:
      mudlog.warning(f"Trying to load npc [{code}] which was not found.")
      return None

    return npc_data.npc_data(proto_type)

  def load_obj(self, zone_id, id):
    proto_type = self.obj_by_uid(zone_id, id)

    if proto_type == None:
      mudlog.warning(f"Trying to load object [{code}] which was not found.")
      return None

    return object_data.object_data(proto_type)

  def pc_by_id(self, id):
    for ch in self._characters:
      if type(ch) == pc_data.pc_data and ch.player_id == id:
        return ch
    return None

  def lose_link(self, ch):
    self.room_by_uid(ch.room).echo(f"{ch} has lost his link.\r\n")
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

  def heartbeat(self, db):
    self._events.heartbeat(self, db)

  def call_hbeat_procs(self, db):
    for mob in self._characters:
      if isinstance(mob, npc_data.npc_data):
        mob.call_hbeat_procs(self, db)

  def debug(self):
    ret_val = f"Zones: {CYAN}{', '.join([zone.id for zone in self.list_zones()])}{NORMAL}\r\n"
    for zone in self.list_zones():
      ret_val += f"{zone.id}: {CYAN}{', '.join(zone.list_room_ids())}{NORMAL}\r\n"
    return ret_val

if __name__ == '__main__':
  pass