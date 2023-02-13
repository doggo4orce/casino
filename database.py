import config
import editor
import exit
import object
import pc
import room
import string_handling
import structs
import sqlite3
import zone

class database:
  def __init__(self, name):
    self._name = name
    self._conn = sqlite3.connect(name)
    self._cursor = self._conn.cursor()

  """create_tables()       <-- creates all database tables
     execute(line)         <-- execute a line of SQL code
     fetchall()            <-- returns _cursor.fetchall()

     contains_exit(rm, ex) <-- check if the exit will collide with an existing exit
     _add_exit(rm, ex)     <-- add ex from rm to the database
     _delete_exit(rm, ex)  <-- delete ex from rm from the database
     save_exit(rm, ex)     <-- creates or updates ex from rm in the database

     contains_player(p)    <-- check whether p will collide with an existing player
     _add_player(p)        <-- add p to the database
     _delete_player(p)     <-- delete p from the database
     save_player(p)        <-- creates or updates p in the database

     contains_npc(np)      <-- checks whether np (npc_proto) will collide with existing entry
     _add_npc(np)          <-- add np to the database
     _delete_npc(np)       <-- deletes np from the database
     save_npc(np)          <-- creates or updates np in the database

     contains_room(rm)     <-- check whether rm will collide with an existing room
     _add_room(rm)         <-- adds rm to the database
     _delete_room(rm)      <-- deletes rm from the database
     save_room(rm)         <-- creates or updates rm in the database

     contains_zone(zn)     <-- check whether zn will collide with an existing zone
     _add_zone(zn)         <-- add zn to the database
     _delete_zone(zn)      <-- deletes zn from the database
     save_zone(zn)         <-- creates or updates zn in the database

     ex_table()            <-- ascii render of ex_table
     p_table()             <-- ascii render of p_table
     rm_table()            <-- ascii render of rm_table
     z_table()             <-- ascii render of z_table

     close_database()      <-- closes _conn"""

  def create_tables(self):

    self.execute("""CREATE TABLE ex_table (
        direction   integer,
        o_zone_id   text,
        o_id        text,
        d_zone_id   text,
        d_id        text)""")

    self.execute("""CREATE TABLE p_table (
        id          integer,
        name        text)""")

    self.execute("""CREATE TABLE npc_table (
        zone_id     text,
        id          text,
        name        text,
        ldesc       text,
        dscn        text)""")

    self.execute("""CREATE TABLE obj_table (
        zone_id     text,
        id          text,
        name        text,
        ldesc       text,
        dscn        text)""")

    self.execute("""CREATE TABLE wld_table (
        zone_id     text,
        id          text,
        name        text,
        description text)""")

    self.execute("""CREATE TABLE z_table (
        id          text,
        name        text,
        author      text)""")

  def execute(self, line, parameters=()):
    self._cursor.execute(line, parameters)

  def fetchall(self):
    return self._cursor.fetchall()

  def contains_exit(self, rm, ex):
    room_id = rm.id
    zone_id = rm.zone_id

    self.execute("SELECT * FROM ex_table WHERE o_zone_id=:zone_id AND o_id=:room_id AND direction=:dir", {
      'zone_id': zone_id,
      'room_id': room_id,
      'dir':     ex.direction})

    if len(self.fetchall()) == 0:
      return False

    return True

  def _add_exit(self, rm, ex):
    id = rm.id
    zone_id = rm.zone_id

    if ex.internal:
      ex.zone_id = zone_id

    self.execute("INSERT INTO ex_table VALUES (:dir, :ozid, :orid, :dzid, :did)", {
      'dir':     ex.direction,
      'ozid':    zone_id,
      'orid':    id,
      'dzid':    ex.zone_id,
      'did':     ex.room_id})

  def _delete_exit(self, rm, ex):
    room_id = rm.id
    zone_id = rm.zone_id

    self.execute("DELETE FROM ex_table WHERE zone_id=:zone_id AND room_id=:room_id AND dir=:dir", {
      'zone_id': zone_id,
      'room_id': room_id,
      'dir':     ex.direction})

  def save_exit(self, rm, ex):
    if self.contains_exit(rm, ex):
      self._delete_exit(rm, ex)
    self._add_exit(rm, ex)

  def contains_player(self, p):
    self.execute("SELECT * FROM p_table WHERE id=:id", {'id':p.id})

    if len(self.fetchall()) == 0:
      return False

    return True

  def _add_player(self, p):
    self.execute("INSERT INTO p_table VALUES (:id, :name)", {
      'id':   p.id,
      'name': p.name})

  def _delete_player(self, p):
    self.execute("DELETE FROM p_table WHERE id=:id", {'id':p.id})

  def save_player(self, p):
    if self.contains_player(p):
      self._delete_player(p)
    self._add_player(p)

  def contains_npc(self, np):
    self.execute("SELECT * from npc_table WHERE zone_id=:zone_id AND id=:id", {
      'zone_id' : np.unique_id.zone_id,
      'id':       np.unique_id.id})

    if len(self.fetchall()) == 0:
      return False

    return True

  def _add_npc(self, np):
    self.execute("INSERT INTO npc_table VALUES (:zone_id, :id, :name, :ldesc, :dscn)", {
      'zone_id': np.unique_id.zone_id,
      'id': np.unique_id.id,
      'name': np.entity.name,
      'ldesc': np.ldesc,
      'dscn': np.entity.desc.str()})

  def _delete_npc(self, np):
    self.execute("DELETE * FROM npc_table WHERE zone_id=:zone_id AND id=:id", {
      'zone_id': np.unique_id.zone_id,
      'id':      np.unique_id.id})

  def save_npc(self, np):
    if self.contains_npc(np):
      self._delete_npc(np)
    self._add_npc(np)

  def contains_obj(self, op):
    self.execute("SELECT * FROM obj_table WHERE zone_id=:zone_id AND id=:id", {
      'zone_id': op.unique_id.zone_id,
      'id':      op.unique_id.id})

    if len(self.fetchall()) == 0:
      return False

    return True

  def _add_obj(self, op):
    self.execute("INSERT INTO obj_table VALUES (:zone_id, :id, :name, :ldesc, :dscn)", {
      'zone_id': op.unique_id.zone_id,
      'id':      op.unique_id.id,
      'name':    op.entity.name,
      'ldesc':   op.ldesc,
      'dscn':    op.entity.desc.str()})

  def _delete_obj(self, op):
    self.execute("DELETE * FROM obj_table WHERE zone_id=:zone_id and id=:id", {
      'zone_id': op.unique_id.zone_id,
      'id':      op.unique_id.id})

  def save_obj(self, op):
    if self.contains_obj(op):
      self.delete_obj(op)
    self._add_obj(op)

  def contains_room(self, rm):
    self.execute("SELECT * FROM wld_table WHERE zone_id=:zone_id AND id=:id", {
      'zone_id': rm.zone_id,
      'id':      rm.id})

    if len(self.fetchall()) == 0:
      return False

    return True

  def _add_room(self, rm):
    self.execute("INSERT INTO wld_table VALUES (:zone_id, :id, :name, :dscn)", {
      'zone_id': rm.zone_id,
      'id':      rm.id,
      'name':    rm.name,
      'dscn':    rm.desc.str()})

  def _delete_room(self, rm):
    self.execute("DELETE FROM wld_table WHERE zone_id=:zone_id AND id=:id", {
      'zone_id' : rm.zone_id,
      'id' : rm.id})

  def save_room(self, rm):
    if self.contains_room(rm):
      self._delete_room(rm)
    self._add_room(rm)

    for dir in exit.direction:
      ex = rm.exit(dir)
      if ex != None:
        self.save_exit(rm, ex)

  def contains_zone(self, zn):
    self.execute("SELECT * FROM z_table WHERE id=:id", {'id' : zn.id})

    if len(self.fetchall()) == 0:
      return False

    return True

  def _add_zone(self, zn):
    self.execute("INSERT INTO z_table VALUES (:id, :name, :auth)", {
      'id':      zn.id,
      'name':    zn.name,
      'auth':    zn.author})

  def _delete_zone(self, zn):
    self.execute("DELETE FROM z_table where id=:id", {'id':zn.id})

  def save_zone(self, zn):
    if self.contains_zone(zn):
      self._delete_zone(zn)
    self._add_zone(zn)

    for rm in zn._world.values():
      self.save_room(rm)

    for np in zn._npc_proto.values():
      self.save_npc(np)

    for op in zn._obj_proto.values():
      self.save_obj(op)      

  def ex_table(self):
    self.execute("SELECT * FROM ex_table")

    ret_val = string_handling.proc_color_codes(f"<c6>Direction:   From:                           To:<c0>\r\n")

    for item in self.fetchall():
      ret_val += f"{exit.direction(item[0]).name:<12} {item[1]:<15} {item[2]:<15} {item[3]:<15} {item[4]:<15}\r\n"

    return ret_val

  def npc_table(self):
    self.execute("SELECT * FROM npc_table")

    ret_val = string_handling.proc_color_codes(f"<c6>Zone:         Id:              Name:                         Desc:<c0>\r\n")
 
    for item in self.fetchall():
      desc_buffer = editor.buffer(item[4])
      ret_val += f"{item[0]:<14}{item[1]:<17}{item[2]:<30}{desc_buffer.preview(30)}\r\n"

    return ret_val

  def obj_table(self):
    self.execute("SELECT * FROM obj_table")

    ret_val = string_handling.proc_color_codes(f"<c6>Zone:         Id:              Name:                         Desc:<c0>\r\n")
 
    for item in self.fetchall():
      desc_buffer = editor.buffer(item[4])
      ret_val += f"{item[0]:<14}{item[1]:<17}{item[2]:<30}{desc_buffer.preview(30)}\r\n"

    return ret_val

  def p_table(self):
    self.execute("SELECT * FROM p_table")

    ret_val = string_handling.proc_color_codes(f"<c6>ID:   Name:<c0>\r\n")
 
    for item in self.fetchall():
      ret_val += f"{item[0]:<6}{item[1]}\r\n"

    return ret_val

  def rm_table(self):
    ret_val = ""
    self.execute("""SELECT * FROM wld_table""")

    ret_val = string_handling.proc_color_codes(f"<c6>{'Zone:':<{config.MAX_ZONE_ID_LENGTH + 2}}Id:       Name:                           Description:<c0>\r\n")

    for item in self.fetchall():
      desc_buffer = editor.buffer(item[3])

      #todo: this will crash if item[0] == None
      #insert a try/catch here to prevent that
      ret_val += f"{item[0]:<{config.MAX_ZONE_ID_LENGTH + 2}}{item[1]:<10}{item[2]:<32}"

      if not desc_buffer.is_empty:
        ret_val += desc_buffer.preview(30)
 
      else:
        ret_val += "(null)"

      ret_val += "\r\n"

    return ret_val

  def z_table(self):
    self.execute("""SELECT * FROM z_table""")

    ret_val = string_handling.proc_color_codes(f"<c6>{'Id:':<{config.MAX_ZONE_ID_LENGTH + 2}}{'Name:':<{config.MAX_ZONE_NAME_LENGTH + 2}}Author:<c0>\r\n")
    for item in self.fetchall():
      ret_val += f"{item[0]:<{config.MAX_ZONE_ID_LENGTH + 2}}{item[1]:<{config.MAX_ZONE_NAME_LENGTH + 2}}{item[2]:<20}" + "\r\n"

    return ret_val

  def close_database(self):
    self._conn.close()

if __name__ == '__main__':
  db = database(':memory:')

  db.create_tables()

  p=pc.pc()
  p.id = 14
  p.name = "Charlie"
  db.save_player(p)

  stockville = zone.zone()
  stockville.name = "the city of stockville"
  stockville.folder = "stockville city"
  stockville.id = "stockville"
  stockville.author = "kyle"

  rm = room.room()
  rm.name = "The Void"
  rm.zone_id = "stockville"
  rm.id = "void"
  rm.desc = editor.buffer("<p>This is a nice, calm, relaxing space. Anything in this room probably wound up here because it's last known location no longer exists. Head down to return to recall.</p>")
  
  rm.connect(exit.direction.DOWN, 'recall')
  stockville._world[rm.id] = rm

  rm = room.room()
  rm.name = "Stockville Casino"
  rm.zone_id = "stockville"
  rm.id = "casino"
  rm.desc = editor.buffer("<p>The heavy weight of bad decisions hangs thick in the air.</p>")
  rm.connect(exit.direction.WEST, 'recall')
  stockville._world[rm.id] = rm

  db.save_zone(stockville)

  rm = room.room()
  rm.name = "Stockville Recall"
  rm.zone_id = "stockville"
  rm.id = "recall"
  rm.desc = editor.buffer("<p>This is the recall point of Stockville City.  You should be able to get here by typing <c11>RECALL<c0> at <c6>a<c2>n<c5>y<c0> time.</p>")
  rm.connect(exit.direction.EAST, 'casino')
  rm.connect(exit.direction.WEST, 'reading')
  stockville._world[rm.id] = rm
  db.save_room(rm)

  rm = room.room()
  rm.name = "Reading Room"
  rm.zone_id = "stockville"
  rm.id = "reading"
  rm.desc = editor.buffer("""<p>This would a great place to catch up on news from the non-existent message board that should be here!  To the north is the entrance to a different zone.</p>

  <c9>HINT HINT<c0>:  Time to make a message board!
  ---------
       But you can see here that this text
       is not formatted along with the
       paragraph above.  I can even use the
       format command while editing this
       room and this mini pargraph will not
       be harmed!  <(^_^)7   6(*-*)^

<p>But now I've entered paragraph mode again. So all of this text will be formatted according to my user-set preference of how wide I want my screen to be.</p>""")
  rm.connect(exit.direction.EAST, 'recall')
  rm.connect(exit.direction.NORTH, 'newbie_zone[hallway1]')
  stockville._world[rm.id] = rm
  db.save_room(rm)

  npcp = structs.npc_proto_data()
  npcp.entity.namelist = ['baccarat', 'dealer']
  npcp.entity.name = 'the baccarat card dealer'
  npcp.entity.desc = editor.buffer("<p>He looks like he's straight out of a bluegrass music video.</p>")
  npcp.ldesc = 'A dealer stands here ready to hand out cards.  Maybe you should say hi?'
  npcp.unique_id.zone_id = 'stockville'
  npcp.unique_id.id = 'baccarat_dealer'
  stockville._npc_proto[npcp.unique_id.id] = npcp
  db.save_npc(npcp)

  npcp = structs.npc_proto_data()
  npcp.entity.namelist = ['baker', 'fat']
  npcp.entity.name = 'the baker'
  npcp.entity.desc = editor.buffer("<p>He's a nice looking person, but you can see that he has seen battle by the many scars on his body.</p>")
  npcp.ldesc = "A baker is here, but don't give him a bottle."
  npcp.unique_id.zone_id = 'stockville'
  npcp.unique_id.id = 'baker'
  stockville._npc_proto[npcp.unique_id.id] = npcp
  db.save_npc(npcp)
  
  ob = structs.obj_proto_data()
  ob.entity.namelist = ['bottle']
  ob.entity.name = 'a bottle'
  ob.entity.desc = editor.buffer("<p>It's brown and smells sticky inside.</p>")
  ob.ldesc = 'An empty bottle has been dropped here.'
  ob.unique_id.zone_id = 'stockville'
  ob.unique_id.id = 'bottle'
  stockville._obj_proto[ob.unique_id.id] = ob

  # now do the same for the newbie zone
  newbie_zone = zone.zone()

  newbie_zone.name = "the newbie zone"
  newbie_zone.folder = "the newbie zone"
  newbie_zone.id = "newbie_zone"
  newbie_zone.author = "kyle"

  rm = room.room()
  rm.name = "The Beginning of a Damp Hallway"
  rm.zone_id = "newbie_zone"
  rm.id = "hallway1"
  rm.desc = editor.buffer("<p>This hallway leads onward into the darkness.  The floors are made of hard, compact gravel and dirt.  The walls consist of red bricks with white grout.  This place gives off a real, negative vibe.  To the south is Stockville City.</p>")
  rm.connect(exit.direction.NORTH, 'hallway2')
  rm.connect(exit.direction.SOUTH, 'stockville[reading]')
  newbie_zone._world[rm.id] = rm

  rm = room.room()
  rm.name = "A Dark Corner in the Hallway"
  rm.zone_id = "newbie_zone"
  rm.id = "hallway2"
  rm.desc = editor.buffer("""<p>I'll start off with a paragraph tag. Then I will add some more lines haphazardly, as I think of
them. Then I can close the tag whenever I want to, and I will!</p>

<p>The proofread <c5>option is made for situations like <c1>this where you could have <c9>really
<c0>awkard spaces between words and tags. Just simply due to the way you enter words through the
editor, they may come through one at a time. And you may put a period after some spaces and forget to
capitalize a word.</p>""")
  rm.connect(exit.direction.SOUTH, 'hallway1')
  newbie_zone._world[rm.id] = rm

  npcp = structs.npc_proto_data()
  npcp.entity.namelist = ['newbie', 'monster']
  npcp.entity.name = 'the newbie monster'
  npcp.entity.desc = editor.buffer("<p>He has googly eyes and drools all over the place as he growls.</p>")
  npcp.ldesc = 'A newbie monster snarls furiously here.'
  npcp.unique_id.zone_id = 'newbie_zone'
  npcp.unique_id.id = 'newbie_monster'
  newbie_zone._npc_proto[npcp.unique_id.id] = npcp

  ob = structs.obj_proto_data()
  ob.entity.namelist = ['newbie', 'dagger']
  ob.entity.name = 'a newbie dagger'
  ob.entity.desc = editor.buffer("<p>It's so bright and shiny, even you can't lose it.</p>")
  ob.entity.ldesk = 'Some idiot left a newbie dagger here.'
  ob.unique_id.zone_id = 'newbie_zone'
  ob.unique_id.id = 'newbie_dagger'
  newbie_zone._obj_proto[ob.unique_id.id] = ob
  db.save_zone(newbie_zone)

  print("Zone Table")
  print(db.z_table() + "\r\n")
  print("Room Table")
  print(db.rm_table() + "\r\n")
  print("Player Table")
  print(db.p_table() + "\r\n")
  print("Exit Table")
  print(db.ex_table() + "\r\n")
  print("Zone Table")
  print(db.z_table() + "\r\n")
  print("Object Table")
  print(db.obj_table() + "\r\n")

  db.close_database()
