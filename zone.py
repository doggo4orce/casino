from color import *
import config
import exit
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

  # todo: factor some of this thorugh a similar function for obj_protos, npc_protos, and rooms?
  def save_to_folder(self):

    path = config.WORLD_FOLDER + self.folder + '/'

    obj_folder = path + "obj/"
    npc_folder = path + "npc/"
    wld_folder = path + "wld/"

    # make world folder (it might already exist)
    if not os.path.isdir(config.WORLD_FOLDER):
      print(f"World folder missing.  Creating it.")
      os.system(f"mkdir '{config.WORLD_FOLDER}'")

    # make zone folder (it might already exist)
    if not os.path.isdir(path):
      print(f"Zone folder missing.  Creating it.")
      os.system(f"mkdir '{path}'")

    # make info file if it doesn't already exist
    with open(path + "info.zon", "w+") as wf:
      wf.write(f"# Zone file for {self.name}\n")
      wf.write(f"name: {self.name}\n")
      wf.write(f"id: {self.id}\n")
      wf.write(f"author: {self.author}\n")

    # make room folder (it might already exist)
    if not os.path.isdir(wld_folder):
      os.system(f"mkdir '{wld_folder}'")

    for rm in self._world.values():

      with open(wld_folder + rm.id + ".room", "w") as wf:

        wf.write(f"name: {rm.name}\n")
        wf.write(f"id: {rm.id}\n")
        wf.write(f"desc:\n{rm.desc.raw_str()}~\n")

        for dir in exit.direction:
          dest = rm.get_destination(dir)
          if dest != None:
            wf.write(f"{dir.name.lower()}: {dest}\n")
  
    if not os.path.isdir(obj_folder):
      os.system(f"mkdir '{obj_folder}'")

    for proto in self._obj_proto.values():
      with open(obj_folder + proto.unique_id.id + ".obj", "w") as wf:
        wf.write(f"ldesc: {proto.ldesc}\n")
        wf.write(f"id: {proto.unique_id.id}\n")
        wf.write(f"name: {proto.entity.name}\n")
        wf.write(f"namelist: {' '.join(proto.entity.namelist)}\n")
        wf.write(f"desc:\n{proto.entity.desc.raw_str()}~\n")

    if not os.path.isdir(npc_folder):
      os.system(f"mkdir '{npc_folder}'")

    for proto in self._npc_proto.values():
      with open(npc_folder + proto.unique_id.id + ".npc", "w") as wf:
        wf.write(f"namelist: {' '.join(proto.entity.namelist)}\n")
        wf.write(f"id: {proto.unique_id.id}\n")
        wf.write(f"name: {proto.entity.name}\n")
        wf.write(f"ldesc: {proto.ldesc}\n")
        wf.write(f"desc:\n{proto.entity.desc.raw_str()}~\n")

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
  import object
  import pc
  import editor

  os.system(f"rm -rf 'lib/world/stockville city'")
  os.system(f"rm -rf 'lib/world/the newbie zone'")

  
  zn = zone()
  zn.name = "the city of stockville"
  zn.folder = "stockville city"
  zn.id = "stockville"
  zn.author = "kyle"

  rm = room.room()
  rm.name = "The Void"
  rm.id = "void"
  rm.desc = editor.display_buffer("<p>This is a nice, calm, relaxing space. Anything in this room probably wound up here because it's last known location no longer exists. Head down to return to recall.</p>")
  rm.connect(exit.direction.DOWN, 'recall')
  zn._world[rm.id] = rm

  rm = room.room()
  rm.name = "Stockville Casino"
  rm.id = "casino"
  rm.desc = editor.display_buffer("<p>The heavy weight of bad decisions hangs thick in the air.</p>")
  rm.connect(exit.direction.WEST, 'recall')
  zn._world[rm.id] = rm

  rm = room.room()
  rm.name = "Stockville Recall"
  rm.id = "recall"
  rm.desc = editor.display_buffer("<p>This is the recall point of Stockville City.  You should be able to get here by typing RECALL at any time.</p>")
  rm.connect(exit.direction.EAST, 'casino')
  rm.connect(exit.direction.WEST, 'reading')
  zn._world[rm.id] = rm

  rm = room.room()
  rm.name = "Reading Room"
  rm.id = "reading"
  rm.desc = editor.display_buffer("<p>This would a great place to catch up on news from the non-existent message board that should be here!  To the north is the entrance to a different zone.</p>")
  rm.connect(exit.direction.EAST, 'recall')
  rm.connect(exit.direction.NORTH, 'newbie_zone[hallway1]')
  zn._world[rm.id] = rm

  npcp = structs.npc_proto_data()
  npcp.entity.namelist = ['baccarat', 'dealer']
  npcp.entity.name = 'the baccarat card dealer'
  npcp.entity.desc = editor.display_buffer("<p>He looks like he's straight out of a bluegrass music video.</p>")
  npcp.ldesc = 'A dealer stands here ready to hand out cards.  Maybe you should say hi?'
  npcp.unique_id.zone_id = 'stockville'
  npcp.unique_id.id = 'baccarat_dealer'
  zn._npc_proto[npcp.unique_id.id] = npcp

  npcp = structs.npc_proto_data()
  npcp.entity.namelist = ['baker', 'fat']
  npcp.entity.name = 'the baker'
  npcp.entity.desc = editor.display_buffer("<p>He's a nice looking person, but you can see that he has seen battle by the many scars on his body.</p>")
  npcp.ldesc = "A baker is here, but don't give him a bottle."
  npcp.unique_id.zone_id = 'stockville'
  npcp.unique_id.id = 'baker'
  zn._npc_proto[npcp.unique_id.id] = npcp
  
  ob = structs.obj_proto_data()
  ob.entity.namelist = ['bottle']
  ob.entity.name = 'a bottle'
  ob.entity.desc = editor.display_buffer("<p>It's brown and smells sticky inside.</p>")
  ob.ldesc = 'An empty bottle has been dropped here.'
  ob.unique_id.zone_id = 'stockville'
  ob.unique_id.id = 'bottle'
  zn._obj_proto[ob.unique_id.id] = ob

  zn.save_to_folder()

  # now do the same for the newbie zone
  zn = zone()

  zn.name = "the newbie zone"
  zn.folder = "the newbie zone"
  zn.id = "newbie_zone"
  zn.author = "kyle"

  rm = room.room()
  rm.name = "The Beginning of a Damp Hallway"
  rm.id = "hallway1"
  rm.desc = editor.display_buffer("<p>This hallway leads onward into the darkness.  The floors are made of hard, compact gravel and dirt.  The walls consist of red bricks with white grout.  This place gives off a real, negative vibe.  To the south is Stockville City.</p>")
  rm.connect(exit.direction.NORTH, 'hallway2')
  rm.connect(exit.direction.SOUTH, 'stockville[reading]')
  zn._world[rm.id] = rm

  rm = room.room()
  rm.name = "A Dark Corner in the Hallway"
  rm.id = "hallway2"
  rm.desc = editor.display_buffer("<p>The hallway makes a sharp corner here, leading both east or south.</p>")
  rm.connect(exit.direction.SOUTH, 'hallway1')
  zn._world[rm.id] = rm

  npcp = structs.npc_proto_data()
  npcp.entity.namelist = ['newbie', 'monster']
  npcp.entity.name = 'the newbie monster'
  npcp.entity.desc = editor.display_buffer("<p>He has googly eyes and drools all over the place as he growls.</p>")
  npcp.ldesc = 'A newbie monster snarls furiously here.'
  npcp.unique_id.zone_id = 'newbie_zone'
  npcp.unique_id.id = 'newbie_monster'
  zn._npc_proto[npcp.unique_id.id] = npcp

  ob = structs.obj_proto_data()
  ob.entity.namelist = ['newbie', 'dagger']
  ob.entity.name = 'a newbie dagger'
  ob.entity.desc = editor.display_buffer("<p>It's so bright and shiny, even you can't lose it.</p>")
  ob.entity.ldesk = 'Some idiot (maybe you?) left a newbie dagger here.'
  ob.unique_id.zone_id = 'newbie_zone'
  ob.unique_id.id = 'newbie_dagger'
  zn._obj_proto[ob.unique_id.id] = ob

  zn.save_to_folder()





