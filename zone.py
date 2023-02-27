# python modules
import glob
import logging
import os

# local modules
from color import *
import config
import database
import exit
import room
import string_handling
import structs

class zone:
  """Creates a zone, which is a modular chunk of the game world.
    name      = name of the zone
    id        = unique identifier string to refer to the zone
    author    = name of author of zone (represented as string)
    path      = path to folder that contains zone files
    world     = dictionary (key=room id) of rooms which form the landscape of the zone
    npc_proto = dictionary (key=npc id) npc blueprints which are used to create npcs
    obj_proto = dictionary (key=object id) of object blueprints"""
  def __init__(self, folder=None):
    self._name = "a new zone"
    self._id = "new_zone"
    self._author = "unknown author"
    self._world = dict()
    self._npc_proto = dict()
    self._obj_proto = dict()
    if folder != None:
      self.parse_folder(folder)

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
    self._id = new_id
  @author.setter
  def author(self, new_author):
    self._author = new_author

  """add_room(new_room)     <- adds room with internal id
     add_npc(new_npcp)      <- adds npc_proto to _obj_protos
     add_obj(new_op)        <- adds obj_proto to _npc_protos
     room_by_id(id)         <- look up room in self.world
     npc_by_id(id)          <- look up npc in self.npc_proto
     obj_by_id(id)          <- look up object in self.obj_proto
     reset()                <- TODO: resets zone based on instructions"""

  def add_room(self, new_room):
    self._world[new_room.id] = new_room

  def add_npc(self, new_npc):
    self._npc_proto[new_npc.unique_id.id] = new_npc

  def add_obj(self, new_op):
    self._obj_proto[new_op.unique_id.id] = new_op

  def room_by_id(self, id):
    if id not in self._world.keys():
      return None
    return self._world[id]

  def npc_by_id(self, id):
    return self._npc_proto[id]

  def obj_by_id(self, id):
    if id not in self._obj_proto.keys():
      return None
    return self._obj_proto[id]

  def __str__(self):
    ret_val = f"Zone: {CYAN}{self.name}{NORMAL} ID: {CYAN}{self.id}{NORMAL}\r\n\r\n"
    ret_val += f"Rooms:\r\n"
    for rm in self._world.values():
      ret_val += f"    {rm.name} {GREEN}{rm.unique_id}{NORMAL}\r\n"
    ret_val += f"NPCs:\r\n"
    for npc in self._npc_proto.values():
      ret_val += f"    {npc.entity.name} {GREEN}{npc.unique_id}{NORMAL}\r\n"
    ret_val += f"Objs:\r\n"
    for obj in self._obj_proto.values():
      ret_val += f"    {obj.entity.name} {GREEN}{obj.unique_id}{NORMAL}\r\n"
    return ret_val

