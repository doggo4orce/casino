from color import *
import config
import glob
import logging
import os
import room
import string_handling
import structs

class zone:
  def __init__(self, folder=None):
    self._name = "a new zone"
    self._id = "new_zone"
    self.world = list()
    self.npc_proto = list()
    self.obj_proto = list()

    if folder != None:
      self.parse_folder(folder)

  @property
  def name(self):
    return self._name
  @property
  def id(self):
    return self._id

  @name.setter
  def name(self, new_name):
    self._name = new_name
  @id.setter
  def id(self, new_id):
    self._id = new_id

  def room_by_id(self, id):
    for room in self.world:
      if room.id == id:
        return room
    return None

  def parse_folder(self, folder):
    rf = open(folder + "/info.zon", "r")

    while True:
      line = rf.readline()
      # check for eof
      if line == "":
        break
      # allows us to ignore comments and blank/empty lines
      if line == "\n" or line[0] == '#':
        continue
      # expecting a tag for sure
      tag, value = string_handling.parse_tag(line)
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

    self.parse_rooms(folder + "/wld/")
    self.parse_npcs(folder + "/npc/")

  def parse_rooms(self, path):
    for file in glob.glob(path + "*.room"):
      rf = open(file, "r")
      self.parse_room(rf)

  def parse_room(self, rf):
    dir_tags = [dir.name for dir in room.direction]
    new_room = room.room()
    new_room.zone_id = self.id
    
    while True:
      line = rf.readline()
      # check for eof
      if line == "":
        break
      # allows us to ignore comments and blank/empty lines
      if line == "\n" or line[0] == '#':
        continue
      # expecting a tag for sure
      tag, value = string_handling.parse_tag(line)
      # if we don't get a tag this file is not formatted properly
      if tag[-1] != ":":
        logging.error(f"Error: Expected ':' at the end of tag {tag} while parsing {rf.name}.")
        return
      # remove the colon and convert to lowercase
      tag = tag[0:len(tag) - 1].lower()
      # ready to interpret the actual tag
      if tag == "name":
        new_room.name = value
      elif tag == "id":
        new_room.id = value
      elif tag == "desc":
        new_room.desc = value
      elif tag.upper() in dir_tags:
        # found an exit
        new_room.connect(room.direction(room.direction[tag.upper()]), value)
      else:
        logging.warning(f"Ignoring {value} from unrecognized tag {tag} while parsing {rf.name}.")

    self.world.append(new_room)

  def parse_npcs(self, path):
    for file in glob.glob(path + "*.npc"):
      rf = open(file, "r")
      self.parse_npc(rf)

  def parse_npc(self, rf):
    new_entity = structs.entity_data()
    new_npc_proto = structs.npc_proto_data()
    while True:
      line = rf.readline()
      # catches the end of the file
      if line == "":
        break
      # allows us to ignore comments and blank/empty lines
      if line == "\n" or line[0] == '#':
        continue
      # expecting a tag for sure
      tag, value = string_handling.parse_tag(line)
      # if we don't get a tag this file is not formatted properly
      if tag[-1] != ":":
        logging.error(f"Error: Expected ':' at the end of tag {tag} while loading")
        return
      # remove the colon and convert to lowercase
      tag = tag[0:len(tag) - 1].lower()
      # ready to interpret the actual tag
      if tag == "name":
        new_entity.name = value
      elif tag == "namelist":
        new_entity.namelist = value.split(" ")
      elif tag == "desc":
        new_entity.desc = value
      elif tag == "ldesc":
        new_entity.ldesc = value
      else:
        logging.warning(f"Ignoring {value} from unrecognized tag {tag} while parsing {rf.name}.")
    # all the data is loaded, now we can store it to the proto
    new_npc_proto.entity = new_entity

    self.npc_proto.append(new_npc_proto)

  def __str__(self):
    ret_val = f"Zone: {CYAN}{self.name}{NORMAL} ID: {CYAN}{self.id}{NORMAL}\r\n\r\n"
    ret_val += f"Rooms:\r\n"
    for rm in self.world:
      ret_val += f"    {rm.name} '{GREEN}{rm.zone_id}[{rm.id}]{NORMAL}'\r\n"
    ret_val += f"NPCs:\r\n"
    for npc in self.npc_proto:
      ret_val += f"    {npc.entity.name}\r\n"
    return ret_val


if __name__ == '__main__':
  casino = zone(config.WORLD_FOLDER + "cash casino/")

  print(casino)
  