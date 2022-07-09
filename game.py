import baccarat
import cards
import config
import db
import enum
import event
import glob
import logging
import object
import pc
import room
import structs

class game:
  def __init__(self):
    """Creates a game world with rooms, objects, and characters.
     wld       = a dictionary for which rooms may be looked up by their vnums
     chars     = a list of characters (including NPCS and PCs) in the game
     objects   = a list of objects which are in the game
     npc_proto = a dictionary of npc prototypes which can be loaded from
     obj_proto = a dictionary of object prototypes which can be loaded from
     events    = handles all events to take place in the future"""
    self.wld       = dict()
    self.chars     = list()
    self.objects   = list()
    self.npc_proto = dict()
    self.obj_proto = dict()
    self.events    = event.event_table()

  """heart_beat()            <- calls the event handlers heart_beat() function
     call_spec_procs()       <- calls all special procedures for npcs
     next_room_vnum()        <- next unused virtual number in self.wld
     next_npc_vnum()         <- next unused virtual number in self.npc_proto
     room_by_vnum(vnum)      <- look up room by virtual number in self.wld
     npc_by_vnum(vnum)       <- look up npc by virtual number in self.npc_proto
     add_char(ch)            <- adds character ch to the wld, in the appropriate room or The Void
     extract_char(ch)        <- extracts character ch from the wld and the appropriate room
     add_obj(obj)            <- these functions are the same
     extract_obj(obj)        <- except for objects instead
     init_wld()              <- calls read_wld_file on every .wld file in 'lib/world/wld' 
     init_npcs()             <- calls read_npc_file on every .npc file in 'lib/world/npc'
     init_objs()             <- calls read_obj_file on every .obj file in 'lib/world/obj'
     assign_spec_procs()     <- assigns special procedures to elements of npc_proto
     startup()               <- calls each of the init_*() functions and assign_spec_procs()
     load_npc(vnum)          <- looks up the npc in self.npc_proto and returns a copy or None
     load_obj(vnum)          <- looks up the obj in self.objs and return a copy or None
     read_wld_file(filename) <- reads all the rooms stored in filename
     read_npc_file(filename) <- reads all the npcs stored in filename
     read_obj_file(filename) <- reads all the objects stored in a filename
     pc_by_id(id)            <- searches chars for a pc with id and returns it if found
     lose_link(ch)           <- disconnects player from their d (seen by players)
     reconnect(d, ch)        <- reconnects player to their d (seen by players)"""

  def heart_beat(self):
    self.events.heart_beat(self)

  def call_spec_procs(self):
    for mob in self.chars:
      if isinstance(mob, pc.npc):
        mob.call_spec_procs(self, None, None, None)

  def next_room_vnum(self):
    # if the world is empty, 0 is the next vnum
    if len(self.wld) == 0:
      return 0
    # find the next unused slot and return its index
    for j in range(0, len(self.wld)):
      if j not in self.wld.keys():
        return j

  def next_npc_vnum(self):
    # if npc_proto is empty, 0 is the next vnum
    if len(self.npc_proto) == 0:
      return 0
    # find the next unused slot and return its index
    for j in range(0, len(self.npc_proto)):
      if j not in self.npc_proto.keys():
        return j

  def next_obj_vnum(self):
    # if obj_proto is empty, 0 is the next vnum
    if len(self.obj_proto) == 0:
      return 0
    # find the next unused slot and return its index
    for j in range(0, len(self.obj_proto)):
      if j not in self.obj_proto.keys():
        return j

  def room_by_vnum(self, vnum):
    if vnum not in self.wld:
      logging.warning(f"Trying to look up room {vnum} which was not found.")
      return None
    else:
      return self.wld[vnum]

  def npc_by_vnum(self, vnum):
    if vnum not in self.npc_proto:
      logging.warning(f"Trying to look up npc {vnum} which was not found.")
      return None
    else:
      return self.npc_proto[vnum]

  def obj_by_vnum(self, vnum):
    if vnum not in self.obj_proto:
      logging.warning(f"Trying to look up object {vnum} which was not found.")
      return None
    else:
      return self.obj_proto[vnum]

  def echo_around(self, ch, hide_from, msg):
    if hide_from == None:
      hide_from = [ ]
      
    hide_from.append(ch)
    self.room_by_vnum(ch.room).echo(msg, exceptions = hide_from)

  def add_char(self, ch):
    # place them in the world
    self.chars.append(ch)
    # check if they have a location
    room = self.room_by_vnum(ch.room)
    # add them to the room if so
    if room != None:
      room.add_char(ch)
    # otherwise put them in the void
    else:
      ch.room = config.VOID_ROOM
      self.room_by_vnum(config.VOID_ROOM).add_char(ch)

  def add_obj(self, obj):
    self.objects.append(obj)
    room = self.room_by_vnum(obj.room)
    if room != None:
      room.inventory.insert(obj)

  def extract_char(self, ch):
    # if they are in a room, remove them from that room
    if ch.room != None:
      self.room_by_vnum(ch.room).remove_char(ch)
    # now remove them from the world
    self.chars.remove(ch)

  def extract_obj(self, obj):
    if obj.room != None:
      self.room_by_vnum(ch.room).inventory.remove(obj)
    self.objects.remove(obj)

  def init_wld(self):
    for file in glob.glob(config.WLD_FOLDER + "*.wld"):
      self.read_wld_file(file)

  def init_npcs(self):
    for file in glob.glob(config.NPC_FOLDER + "*.npc"):
      self.read_npc_file(file)

  def init_objs(self):
    for file in glob.glob(config.OBJ_FOLDER + "*.obj"):
      self.read_obj_file(file)

  def assign_spec_procs(self):
    self.npc_proto[3002].specs.append(structs.special_procedure("baccarat dealer greeting", baccarat.baccarat_dealer_intro))
    self.npc_proto[3002].specs.append(structs.special_procedure("baccarat syntax handling", baccarat.baccarat_syntax_parser))
    self.npc_proto[3002].specs.append(structs.special_procedure("baccarat deals a shoe",    baccarat.baccarat_dealing))

  def startup(self):
    self.init_wld()
    self.init_npcs()
    self.init_objs()

    # temporary, will be replaced with self.init_zones() one day
    mob = self.load_npc(3000)
    mob.room = 3000
    self.add_char(mob)

    mob = self.load_npc(3001)
    mob.room = 3001
    self.add_char(mob)

    obj = self.load_obj(3000)
    obj.room = 3000
    self.add_obj(obj)

    obj = self.load_obj(3001)
    obj.room = 3001
    self.add_obj(obj)

    mob = self.load_npc(3002)
    mob.room = 3002

    # promote the mob to a card dealer
    mob = cards.card_dealer.from_npc(mob)

    # now promote them to a baccarat dealer
    mob = baccarat.baccarat_dealer.from_card_dealer(mob)

    self.add_char(mob)

    self.assign_spec_procs()


  def load_npc(self, vnum):
    if vnum not in self.npc_proto:
      logging.warning(f"Trying to load npc [{vnum}] which was not found.")
      return None
    new_npc = pc.npc()
    new_npc.entity = self.npc_proto[vnum].entity
    new_npc.vnum = vnum
    new_npc.specs = self.npc_proto[vnum].specs
    return new_npc

  def load_obj(self, vnum):
    if vnum not in self.obj_proto:
      logging.warning(f"Trying to load object [{vnum}] which was not found.")
      return None

    new_obj = object.object()
    new_obj.entity = self.obj_proto[vnum].entity
    return new_obj

  def read_wld_file(self, filename):
    rf = open(filename, 'r')
    while True:
      #expected #VNUM or $ (final line)
      line = rf.readline()
      # file is terminated with $
      if line[0] == '$':
        return
      # first thing is the virtual number
      vnum = int(line[1:])
      # now read the rest
      self.wld[vnum] = db.parse_room(rf)
      self.wld[vnum].vnum = vnum

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
    for ch in self.chars:
      if type(ch) == pc.pc and ch.id == id:
        return ch
    return None

  def lose_link(self, ch):
    self.wld[ch.room].echo(f"{ch} has lost his link.\r\n")
    ch.d = None

  def reconnect(self, d, ch):
    # check if ch isn't actually linkdead
    if ch.d:
      # disconnect the imposter
      ch.d.disconnected = True
      ch.d.char = None
    # connect d to linkless ch
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