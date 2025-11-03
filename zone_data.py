# python modules
import glob
import os

# local modules
from color import *
import config
import exit_data
import room_data
import mudlog
import string_handling

class zone_data:
  """Creates a zone, which is a modular chunk of the game world.
    id        = identifier of zone
    name      = name of the zone
    author    = name of author of zone
    world     = dictionary of rooms in zone
    npc_proto = dictionary of npc_proto_datas in zone
    obj_proto = dictionary of obj_proto_datas in zone"""
  def __init__(self):
    self.id = "new_zone"
    self.name = "a new zone"
    self.author = "unknown author"
    self._world = dict()
    self._npc_proto = dict()
    self._obj_proto = dict()
    
  # Getters
  @property
  def name(self):
    return self._name
  @property
  def id(self):
    return self._id
  @property
  def author(self):
    return self._author
  
  # Setters
  @name.setter
  def name(self, new_name):
    self._name = new_name
  
  @id.setter
  def id(self, new_id):
    if not string_handling.valid_id(new_id):
      mudlog.error(f"Trying to set invalid zone_id {new_id}.")
      return
    self._id = new_id

  @author.setter
  def author(self, new_author):
    self._author = new_author

  """add_room(room)  <- add room to self._world
     delete_room(id) <- remove room from self._world
     add_npc(proto)  <- adds npc_proto to self._obj_proto
     delete_npc(id)  <- remove npc_proto from self._obj_proto
     add_obj(proto)  <- adds obj_proto to self._npc_proto
     delete_obj(id)  <- remove obj_proto from self._obj_proto
     room_by_id(id)  <- look up room in self._world
     has_room(id)    <- check if id is in self._world.keys()
     npc_by_id(id)   <- look up npc in self._npc_proto
     has_npc(id)     <- check if id is in self._npc_proto.keys()
     obj_by_id(id)   <- look up object in self._obj_proto
     has_obj(id)     <- check if id is in self._obj_proto.keys()
     num_rooms()     <- count rooms in zone
     num_npcs()      <- count npcs in zone
     num_objs()      <- count objects in zone"""

  def add_room(self, new_room):
    self._world[new_room.id] = new_room

  def delete_room(self, id):
    if id not in self._world.keys():
      mudlog.error(f"Trying to delete non-existant room {id} from zone {self.id}.")
      return
    del self._world[id]

  def add_npc(self, proto):
    self._npc_proto[proto.id] = proto

  def delete_npc(self, id):
    if id not in self._npc_proto.keys():
      mudlog.error(f"Trying to delete non-existant npc {id} from zone {self.id}.")
      return
    del self._npc_proto[id]

  def add_obj(self, proto):
    self._obj_proto[proto.id] = proto

  def delete_obj(self, id):
    if id not in self._obj_proto.keys():
      mudlog.error(f"Trying to delete non-existant object {id} from zone {self.id}.")
      return
    del self._obj_proto[id]

  def room_by_id(self, id):
    if not self.has_room(id):
      return None
    return self._world[id]

  def has_room(self, id):
    return id in self.list_room_ids()

  def npc_by_id(self, id):
    if not self.has_npc(id):
      return None
    return self._npc_proto[id]

  def has_npc(self, id):
    return id in self.list_npc_ids()

  def obj_by_id(self, id):
    if not self.has_obj(id):
      return None
    return self._obj_proto[id]

  def has_obj(self, id):
    return id in self.list_obj_ids()

  def list_room_ids(self):
    return self._world.keys()

  def list_npc_ids(self):
    return self._npc_proto.keys()

  def list_obj_ids(self):
    return self._obj_proto.keys()

  def num_rooms(self):
    return len(self._world)

  def num_npcs(self):
    return len(self._npc_proto)

  def num_objs(self):
    return len(self._obj_proto)

  def debug(self):
    ret_val = f"ID: {CYAN}{self.id}{NORMAL}\r\n"
    ret_val += f"Name: {CYAN}{self.name}{NORMAL}\r\n"
 
    if self.num_rooms() > 0:
      ret_val += f"Rooms:\r\n"
      for rm in self._world.values():
        ret_val += f"  {CYAN}{rm.id}{NORMAL}\r\n"
    if self.num_npcs() > 0:
      ret_val += f"NPCs:\r\n"
      for npc in self._npc_proto.values():
        ret_val += f"  {CYAN}{npc.id}{NORMAL}\r\n"
    if self.num_objs() > 0:
      ret_val += f"Objs:\r\n"
      for obj in self._obj_proto.values():
        ret_val += f"  {CYAN}{obj.id}{NORMAL}\r\n"

    return ret_val[:-2] # peel off final \r\n

