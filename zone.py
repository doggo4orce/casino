from color import *
import config
import file_handling
import glob
import logging
import os
import room
import string_handling
import structs

class zone:
  """Creates a zone, which is a modular chunk of the game world.
    name      = name of the zone
    id        = unique identifier string to refer to the zone
    world     = dictionary (key=room id) of rooms which form the landscape of the zone
    npc_proto = dictionary (key=npc id) npc blueprints which are used to create npcs
    obj_proto = dictionary (key=object id) of object blueprints"""
  def __init__(self, folder=None):
    self._name = "a new zone"
    self._id = "new_zone"
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

  # Setters
  @name.setter
  def name(self, new_name):
    self._name = new_name
  @id.setter
  def id(self, new_id):
    self._id = new_id

  """room_by_id(id)         <- look up room in self.world
     npc_by_id(id)          <- look up npc in self.npc_proto
     obj_by_id(id)          <- look up object in self.obj_proto
     parse_folder(path)     <- loads zone from path
     parse_generic(var, rf) <- loads room, obj, or npc file from rf to var
     parse_rooms(path)      <- calls parse_rno on each *.room file
     parse_npcs(path)       <- calls parse_rno on each *.npc file
     parse_objects(path)    <- calls parse_rno on each *.obj file"""
  def room_by_id(self, id):
    return self._world[id]

  def npc_by_id(self, id):
    return self._npc_proto[id]

  def obj_by_id(self, id):
    return self._obj_proto[id]

  def parse_folder(self, path):
    rf = open(path + "info.zon", "r")
    while True:
      line = rf.readline()
      # check for eof
      if line == "":
        break
      # allows us to ignore comments and blank/empty lines
      if line == "\n" or line[0] == '#':
        continue
      # expecting a tag for sure
      tag, value = string_handling.split_tag_value(line)
      # if we don't get a tag this file is not formatted properly
      if tag[-1] != ":":
        logging.error(f"Error: Expected ':' at the end of tag {tag} while parsing {rf.name}.")
        return
      # remove the colon and convert to lowercase
      tag = tag[0:len(tag) - 1].lower()
      # ready to interpret the actual tag
      if tag == "name":
        self._name = value
      elif tag == "id":
        self._id = value
      else:
        logging.warning(f"Ignoring {value} from unrecognized tag {tag} while parsing {rf.name}.")
    self.parse_rooms(path + "wld/")
    self.parse_npcs(path + "npc/")
    self.parse_objects(path + "obj/")

  def parse_rooms(self, path):
    for file in glob.glob(path + "*.room"):
      rf = open(file, "r")
      new_room = room.room()
      new_room.unique_id.update(self.id, "no_id")
      file_handling.parse_generic(new_room, rf)
      self._world[new_room.unique_id.id] = new_room

  def parse_npcs(self, path):
    for file in glob.glob(path + "*.npc"):
      rf = open(file, "r")
      new_npc_proto = structs.npc_proto_data()
      new_npc_proto.unique_id.update(self.id, "no_id")
      file_handling.parse_generic(new_npc_proto, rf)
      self._npc_proto[new_npc_proto.unique_id.id] = new_npc_proto

  def parse_objects(self, path):
    for file in glob.glob(path + "*.obj"):
      rf = open(file, "r")
      new_obj_proto = structs.obj_proto_data()
      new_obj_proto.unique_id.update(self.id, "no_id")
      file_handling.parse_generic(new_obj_proto, rf)
      self._obj_proto[new_obj_proto.unique_id.id] = new_obj_proto

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

if __name__ == '__main__':
  casino = zone(config.WORLD_FOLDER + "cash casino/")

  print(casino)
  