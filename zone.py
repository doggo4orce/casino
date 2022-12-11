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
    author    = name of author of zone (represented as string)
    path      = path to folder that contains zone files
    world     = dictionary (key=room id) of rooms which form the landscape of the zone
    npc_proto = dictionary (key=npc id) npc blueprints which are used to create npcs
    obj_proto = dictionary (key=object id) of object blueprints"""
  def __init__(self, folder=None):
    self._name = "a new zone"
    self._id = "new_zone"
    self._author = "unknown author"
    self._folder = folder
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
  @property
  def folder(self):
    return self._folder
  
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
  @folder.setter
  def folder(self, new_folder):
    self._folder = new_folder

  """add_room(id, new_room) <- adds room with internal id
     room_by_id(id)         <- look up room in self.world
     npc_by_id(id)          <- look up npc in self.npc_proto
     obj_by_id(id)          <- look up object in self.obj_proto
     parse_folder(path)     <- loads zone from path
     save_to_folder(path)   <- saves zone to files
     parse_generic(var, rf) <- loads room, obj, or npc file from rf to var
     parse_rooms(path)      <- calls parse_rno on each *.room file
     parse_npcs(path)       <- calls parse_rno on each *.npc file
     parse_objects(path)    <- calls parse_rno on each *.obj file
     save_to_folder()       <- saves zone to lib/world/<self.folder>/
     reset()                <- TODO: resets zone based on instructions in <??.filename>"""

  def add_room(self, id, new_room):
    self._world[id] = new_room

  def room_by_id(self, id):
    if id not in self._world.keys():
      return None
    return self._world[id]

  def npc_by_id(self, id):
    return self._npc_proto[id]

  def obj_by_id(self, id):
    return self._obj_proto[id]

  def parse_folder(self, path):

    # this is a hack that peels off the prefix lib/world and the final /
    self.folder = path[10:-1]

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
        self.name = value
      elif tag == "id":
        self.id = value
      elif tag == "author":
        self.author = value
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

  def save_to_folder(self):
    path = config.WORLD_FOLDER + self.folder + '/'

    # make zone folder (it might already exist)
    if not os.path.exists(path):
      os.system("mkdir '{}'".format(path))

    with open(path + "info.zon", "w") as wf:
      wf.write(f"# Zone file for {self.name}\n")
      wf.write(f"name: {self.name}\n")
      wf.write(f"id: {self.id}\n")
      wf.write(f"author: {self.author}\n")

    # make room folder (it might already exist)
    if not os.path.exists(f"'{path}wld/'"):
      os.system(f"mkdir '{path}wld/'")

    for rm in self._world.values():

      with open(path + "wld/" + rm.id + ".room", "w") as wf:

        wf.write(f"name: {rm.name}\n")
        wf.write(f"id: {rm.id}\n")
        wf.write(f"desc: {rm.desc}\n")

        for ex in rm.exits:
          wf.write(f"{ex.direction.name.lower()}: {ex.destination}\n")
  
    if not os.path.exists(f"'{path}obj/'"):
      os.system(f"mkdir '{path}obj/'")

    for proto in self._obj_proto.values():
      # go ahead and criticize this choice of extension,
      # it's Python and I'm not making any actual .obj files with C
      with open(path + "obj/" + proto.id + ".obj", "w"):
        wf.write(f"ldesc: {proto.ldesc}\n")
        wf.write(f"id: {proto.id}\n")
        wf.write(f"name: {proto.entity.name}\n")
        wf.write(f"namelist: {proto.entity.namelist}\n")
        wf.write(f"desc: {proto.entity.desc}\n")

    if not os.path.exists(f"'{path}npc/"):
      os.system(f"mkdir '{path}npc/'")

    # switching from mob to npc was not difficult,
    # but for some reason I refuse to change .obj to .item (see above)
    for proto in self._npc_proto.values():
      with open(path + "npc/" + proto.id + ".npc", "w") as wf:
        wf.write(f"namelist: {proto.entity.namelist}\n")
        wf.write(f"id: {proto.id}\n")
        wf.write(f"name: {proto.entity.name}\n")
        wf.write(f"ldesc: {proto.ldesc}\n")
        wf.write(f"desc: {proto.entity.desc}\n")

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
  import exit

  os.system(f"rm -rf 'lib/world/the newbie zone'")
  zone = zone()

  zone.name = "the newbie zone"
  zone.folder = "the newbie zone"
  zone.id = "newbie_zone"
  zone.author = "Kyle"

  rm = room.room()

  rm.name = "The Beginning of a Damp Hallway"
  rm.id = "hallway1"
  rm.desc = "This hallway leads onward into the darkness.  The floors are made of hard, compact gravel and dirt.  The walls consist of red bricks with white grout.  This place gives off a real, negative vibe."
  rm.connect(exit.direction.NORTH, 'hallway2')
  rm.connect(exit.direction.SOUTH, 'stockville[reading]')
  zone._world[rm.id] = rm

  rm = room.room()
  
  rm.name = "A Dark Corner in the Hallway"
  rm.id = "hallway2"
  rm.desc = "The hallway makes a sharp corner here, leading both east or south."
  rm.connect(exit.direction.SOUTH, 'hallway1')

  zone._world[rm.id] = rm

  zone.save_to_folder()





