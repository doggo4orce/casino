import config
import editor
import exit
import logging
import object
import os
import pc
import room
import string_handling
import structs
import sqlite3
import zone

class database:
  def __init__(self, name):
    self._name = name
   
    if os.path.exists(name):
      self._conn = sqlite3.connect(name)
      self._cursor = self._conn.cursor()
    else:
      self._conn = sqlite3.connect(name)
      self._cursor = self._conn.cursor()
      self.create_tables()
      self.load_stock()

  """create_tables()         <-- creates all database tables
     execute(line)           <-- returns execution of (SQL line)
     fetchall()              <-- returns cursor.fetchall()
     fetchone()              <-- returns cursor.fetchone()

     contains_exit(rm, dir, ex) <-- check if the exit will collide with an existing exit
     add_exit(rm, ex)        <-- add ex from rm to the database
     delete_exit(rm, ex)     <-- delete ex from rm from the database
     save_exit(rm, ex)       <-- creates or updates ex from rm in the database

     contains_obj(obj)       <-- check whether obj (obj_proto) will collide with existing entry
     add_obj(obj)            <-- add obj to the database
     delete_obj(obj)         <-- deletes obj from the database
     save_obj(obj)           <-- creates or updates obj in the database

     contains_player(p)      <-- check whether p will collide with an existing player
     add_player(p)           <-- add p to the database
     delete_player(p)        <-- delete p from the database
     save_player(p)          <-- creates or updates p in the database

     contains_pref(p, tag)   <-- check whether cpref will collide with an existing preference
     add_pref(p, tag, val)   <-- add p's pref with tag as val
     delete_pref(p, tag)     <-- delete p's pref with tag
     save_pref(p, tag, val)  <-- creates or updates p's pref with tag in the database as val

     contains_npc(np)        <-- check whether np (npc_proto) will collide with existing entry
     add_npc(np)             <-- add np to the database
     delete_npc(np)          <-- deletes np from the database
     save_npc(np)            <-- creates or updates np in the database

     contains_room(rm)       <-- check whether rm will collide with an existing room
     add_room(rm)            <-- adds rm to the database
     delete_room(rm)         <-- deletes rm from the database
     save_room(rm)           <-- creates or updates rm in the database

     contains_zone(zn)       <-- check whether zn will collide with an existing zone
     add_zone(zn)            <-- add zn to the database
     delete_zone(zn)         <-- deletes zn from the database
     save_zone(zn)           <-- creates or updates zn in the database

     load_ptable(mud)        <-- load all player id's and names
     load_zones(mud)         <-- load all zones
     load_npcs(mud)          <-- load all npc_proto's
     load_objs(mud)          <-- load all obj_proto's
     load_game(mud)          <-- load entire database

     ex_table()              <-- loads exit table
     ex_table_str()          <-- print exit table
     npc_table()             <-- loads npc table
     npc_table_str()         <-- print npc table
     obj_table()             <-- loads obj table
     obj_table_str()         <-- print obj table
     p_table_str()           <-- loads player table
     p_table_str()           <-- print player table
     rm_table()              <-- loads room table
     rm_table_str()          <-- print room table
     z_table()               <-- loads zone table
     z_table_str()           <-- print zone table

     load_stock()            <-- hard-codes a stock world into the DB
     load_world(mud)         <-- loads zones, rooms, obj/npc_protos into mud

     next_unused_pid()       <-- figure out the lowest player ID not in use
     name_used(name)         <-- check if a player with name exists
     check_pwd(name, pwd)    <-- check if the password is correct for the player
     player_name_by_id(id)   <-- player name that corresponds to id
     player_id_by_name(name) <-- player id that corresponds to id

     Used for debugging info (called in commands.do_db)
     table_list()            <-- returns a list of table names
     row_count(table_name)   <-- counts number of rows loaded to table_name
     close()                 <-- closes conn"""
      
  def create_tables(self):

    self.execute("""CREATE TABLE ex_table (
        direction   integer,
        o_zone_id   text,
        o_id        text,
        d_zone_id   text,
        d_id        text)""")

    self.execute("""CREATE TABLE p_table (
        id          integer,
        name        text,
        password    text)""")

    self.execute("""CREATE TABLE pref_table_numeric (
        id          integer,
        tag         text,
        value       integer)""")

    self.execute("""CREATE TABLE pref_table_text (
        id          integer,
        tag         text,
        value       text)""")

    self.execute("""CREATE TABLE pref_table_flag (
        id          integer,
        tag         text,
        value       integer)""")

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
    try:
      ret_val = self._cursor.execute(line, parameters)
    except sqlite3.ProgrammingError:
      logging.error(f"SQL Programming Error with line {line} and parameters {parameters}.")
    else:
      self._conn.commit()
      return ret_val

  def fetchall(self):
    return self._cursor.fetchall()

  def fetchone(self):
    return self._cursor.fetchone()

  def contains_exit(self, rm, ex):
    room_id = rm.id
    zone_id = rm.zone_id

    self.execute("SELECT * FROM ex_table WHERE o_zone_id=:zone_id AND o_id=:room_id AND direction=:dir", {
      'zone_id': zone_id,
      'room_id': room_id,
      'dir':     rm.direction(ex)})
    return len(self.fetchall()) != 0

  def _add_exit(self, rm, ex):
    id = rm.id
    zone_id = rm.zone_id

    if ex.internal:
      ex.zone_id = zone_id

    self.execute("INSERT INTO ex_table VALUES (:dir, :ozid, :orid, :dzid, :did)", {
      'dir':     rm.direction(ex),
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
      'dir':     rm.direction(ex)})

  def save_exit(self, rm, ex):
    if self.contains_exit(rm, ex):
      self._delete_exit(rm, ex)
    self._add_exit(rm, ex)

  def contains_obj(self, op):
    self.execute("SELECT * FROM obj_table WHERE zone_id=:zid AND id=:id", {
      'zid':     op.zone_id, 
      'id':      op.id})
    return len(self.fetchall()) != 0

  def _add_obj(self, op):
    self.execute("INSERT INTO obj_table VALUES (:zone_id, :id, :name, :ldesc, :dscn)", {
      'zone_id': op.zone_id,
      'id':      op.id,
      'name':    op.entity.name,
      'ldesc':   op.ldesc,
      'dscn':    op.entity.desc.str()})

  def _delete_obj(self, op):
    self.execute("DELETE FROM obj_table WHERE zone_id=:zid AND id=:id", {
      'zid': op.zone_id,
      'id':  op.id})

  def save_obj(self, op):
    if self.contains_obj(op):
      self.delete_obj(op)
    self._add_obj(op)

  def contains_flag_pref(self, p, attr):
    self.execute("SELECT * FROM pref_table_flag WHERE id=:id AND tag=:tag", {
      'id': p.id,
      'tag': attr})
    return len(self.fetchall()) != 0

  def _add_flag_pref(self, p, attr, value):
    self.execute("INSERT INTO pref_table_flag VALUES(:id, :tag, :value)", {
      'id': p.id,
      'tag': attr,
      'value': int(value)}) # save flag as 1 or 0

  def _delete_flag_pref(self, p, attr):
    self.execute("DELETE FROM pref_table_flag WHERE id=:id AND tag=:tag", {
     'id': p.id,
     'tag': attr})

  def save_flag_pref(self, p, attr, value):
    if self.contains_flag_pref(p, attr):
      self._delete_flag_pref(p, attr)
    self._add_flag_pref(p, attr, value)

  def contains_numeric_pref(self, p, attr):
    self.execute("SELECT * FROM pref_table_numeric WHERE id=:id AND tag=:tag", {
      'id': p.id,
      'tag': attr})
    return len(self.fetchall()) != 0

  def _add_numeric_pref(self, p, attr, value):
    self.execute("INSERT INTO pref_table_numeric VALUES(:id, :tag, :value)", {
      'id': p.id,
      'tag': attr,
      'value': value})

  def _delete_numeric_pref(self, p, attr):
    self.execute("DELETE FROM pref_table_numeric WHERE id=:id AND tag=:tag", {
     'id': p.id,
     'tag': attr})

  def save_numeric_pref(self, p, attr, value):
    if self.contains_numeric_pref(p, attr):
      self._delete_numeric_pref(p, attr)
    self._add_numeric_pref(p, attr, value)

  def contains_text_pref(self, p, attr):
    self.execute("SELECT * FROM pref_table_text WHERE id=:id AND tag=:tag", {
      'id': p.id,
      'tag': attr})
    return len(self.fetchall()) != 0

  def _add_text_pref(self, p, attr, value):
    self.execute("INSERT INTO pref_table_text VALUES(:id, :tag, :value)", {
      'id': p.id,
      'tag': attr,
      'value': value})

  def _delete_text_pref(self, p, attr):
    self.execute("DELETE FROM pref_table_text WHERE id=:id AND tag=:tag", {
     'id': p.id,
     'tag': attr})

  def save_text_pref(self, p, attr, value):
    if self.contains_text_pref(p, attr):
      self._delete_text_pref(p, attr)
    self._add_text_pref(p, attr, value)

  def contains_player(self, p):
    self.execute("SELECT * FROM p_table WHERE id=:id", {'id':p.id})
    return len(self.fetchall()) != 0

  def _add_player(self, p):
    self.execute("INSERT INTO p_table VALUES (:id, :name, :pwd)", {
      'id':   p.id,
      'name': p.name,
      'pwd':  p.pwd})

  def _delete_player(self, p):
    self.execute("DELETE FROM p_table WHERE id=:id", {'id':p.id})

  def save_player(self, p):
    if self.contains_player(p):
      self._delete_player(p)
    self._add_player(p)

  def name_used(self, name):
    return self.id_by_name(name) != None

  def check_pwd(self, name, pwd):
    self.execute("SELECT * FROM p_table WHERE name=:name AND password=:pwd", {
      'name': name,
      'pwd':  pwd})
    return len(self.fetchall()) != 0

  def name_by_id(self, id):
    self.execute("SELECT * FROM p_table WHERE id=:id", {'id': id})

    rows = self.fetchall()
    if(len(rows)) == 0:
      return None

    return rows[0][1]

  def id_by_name(self, name):
    self.execute("SELECT * FROM p_table WHERE name=:name", {'name': name})

    rows = self.fetchall()
    if(len(rows)) == 0:
      return None

    return rows[0][0]

  def next_unused_pid(self):
    j = 1;

    while self.name_by_id(j) != None:
      j += 1

    return j

  def num_players(self):
    self.execute("SELECT * FROM p_table")
    return len(self.fetchall())

  def load_player(self, name):
    ret_val = pc.pc()

    self.execute("SELECT * FROM p_table WHERE name=:name", {'name': name})

    row = self.fetchone()

    if row == None:
      return None

    ret_val.id   = row[0]
    ret_val.name = row[1]
    ret_val.pwd  = row[2]

    return ret_val
    
  def contains_npc(self, np):
    self.execute("SELECT * from npc_table WHERE zone_id=:zone_id AND id=:id", {
      'zone_id' : np.unique_id.zone_id,
      'id':       np.unique_id.id})
    return len(self.fetchall()) != 0

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

  def contains_room(self, rm):
    self.execute("SELECT * FROM wld_table WHERE zone_id=:zone_id AND id=:id", {
      'zone_id': rm.zone_id,
      'id':      rm.id})
    return len(self.fetchall()) != 0

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
    return len(self.fetchall()) != 0

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
    return self.fetchall()

  def ex_table_str(self):
    ret_val = string_handling.proc_color_codes(f"<c6>Direction:   From:                           To:<c0>\r\n")

    for item in self.ex_table():
      ret_val += f"{exit.direction(item[0]).name:<12} {item[1]:<15} {item[2]:<15} {item[3]:<15} {item[4]:<15}\r\n"

    return ret_val

  def npc_table(self):
    self.execute("SELECT * FROM npc_table")
    return self.fetchall()

  def npc_table_str(self):
    ret_val = string_handling.proc_color_codes(f"<c6>Zone:         Id:              Name:                         Desc:<c0>\r\n")
 
    for item in self.npc_table():
      desc_buffer = editor.buffer(item[4])
      ret_val += f"{item[0]:<14}{item[1]:<17}{item[2]:<30}{desc_buffer.preview(30)}\r\n"

    return ret_val

  def obj_table(self):
    self.execute("SELECT * FROM obj_table")
    return self.fetchall()

  def obj_table_str(self):
    ret_val = string_handling.proc_color_codes(f"<c6>Zone:         Id:              Name:                         Desc:<c0>\r\n")
 
    for item in self.obj_table():
      desc_buffer = editor.buffer(item[4])
      ret_val += f"{item[0]:<14}{item[1]:<17}{item[2]:<30}{desc_buffer.preview(30)}\r\n"

    return ret_val

  def pref_table(self):
    self.execute("SELECT * FROM pref_table")
    return self.fetchall()

  def p_table(self):
    self.execute("SELECT * FROM p_table")
    return self.fetchall()

  def p_table_str(self):
    ret_val = string_handling.proc_color_codes(f"<c6>ID:   Name:<c0>\r\n")
 
    for item in self.p_table():
      ret_val += f"{item[0]:<6}{item[1]}\r\n"

    return ret_val

  def wld_table(self):
    self.execute("""SELECT * FROM wld_table""")
    return self.fetchall()

  def wld_table_str(self):
    self.execute("""SELECT * FROM wld_table""")

    ret_val = string_handling.proc_color_codes(f"<c6>{'Zone:':<{config.MAX_ZONE_ID_LENGTH + 2}}Id:       Name:                           Description:<c0>\r\n")

    for item in self.wld_table():
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
    return self.fetchall()

  def z_table_str(self):
    ret_val = string_handling.proc_color_codes(f"<c6>{'Id:':<{config.MAX_ZONE_ID_LENGTH + 2}}{'Name:':<{config.MAX_ZONE_NAME_LENGTH + 2}}Author:<c0>\r\n")
    for item in self.z_table():
      ret_val += f"{item[0]:<{config.MAX_ZONE_ID_LENGTH + 2}}{item[1]:<{config.MAX_ZONE_NAME_LENGTH + 2}}{item[2]:<20}" + "\r\n"

    return ret_val

  def close(self):
    self._conn.close()

  def table_list(self):
    ret_val = list()

    self.execute("""SELECT name FROM sqlite_master WHERE type='table';""")

    for item in self.fetchall():
      ret_val.append(item[0])

    return ret_val

  def row_count(self, table_name):
    if table_name not in self.table_list():
      return 0

    self.execute(f"SELECT * FROM {table_name}")
    return len(self.fetchall())

  def column_list(self, table_name):
    ret_val = list()

    if table_name not in self.table_list():
      return ret_val

    data = self.execute(f"SELECT * FROM {table_name}")
    for item in data.description:
      ret_val.append(item[0])

    return ret_val

  def load_stock(self):
    stockville = zone.zone()
    stockville.name = "the city of stockville"
    stockville.folder = "stockville city"
    stockville.id = "stockville"
    stockville.author = "kyle"
    self.save_zone(stockville)

    rm = room.room()
    rm.name = "The Void"
    rm.zone_id = "stockville"
    rm.id = "void"
    rm.desc = editor.buffer("<p>This is a nice, calm, relaxing space. Anything in this room probably wound up here because it's last known location no longer exists. Head down to return to recall.</p>")
  
    rm.connect(exit.direction.DOWN, 'recall')
    stockville._world[rm.id] = rm
    self.save_room(rm)

    rm = room.room()
    rm.name = "Stockville Casino"
    rm.zone_id = "stockville"
    rm.id = "casino"
    rm.desc = editor.buffer("<p>The heavy weight of bad decisions hangs thick in the air.</p>")
    rm.connect(exit.direction.WEST, 'recall')
    stockville._world[rm.id] = rm
    self.save_room(rm)

    rm = room.room()
    rm.name = "Stockville Recall"
    rm.zone_id = "stockville"
    rm.id = "recall"
    rm.desc = editor.buffer("<p>This is the recall point of Stockville City.  You should be able to get here by typing <c11>RECALL<c0> at <c6>a<c2>n<c5>y<c0> time.</p>")
    rm.connect(exit.direction.EAST, 'casino')
    rm.connect(exit.direction.WEST, 'reading')
    stockville._world[rm.id] = rm
    self.save_room(rm)

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
    self.save_room(rm)

    npcp = structs.npc_proto_data()
    npcp.entity.namelist = ['baccarat', 'dealer']
    npcp.entity.name = 'the baccarat card dealer'
    npcp.entity.desc = editor.buffer("<p>He looks like he's straight out of a bluegrass music video.</p>")
    npcp.ldesc = 'A dealer stands here ready to hand out cards.  Maybe you should say hi?'
    npcp.unique_id.zone_id = 'stockville'
    npcp.unique_id.id = 'baccarat_dealer'
    stockville._npc_proto[npcp.unique_id.id] = npcp
    self.save_npc(npcp)

    npcp = structs.npc_proto_data()
    npcp.entity.namelist = ['baker', 'fat']
    npcp.entity.name = 'the baker'
    npcp.entity.desc = editor.buffer("<p>He's a nice looking person, but you can see that he has seen battle by the many scars on his body.</p>")
    npcp.ldesc = "A baker is here, but don't give him a bottle."
    npcp.unique_id.zone_id = 'stockville'
    npcp.unique_id.id = 'baker'
    stockville._npc_proto[npcp.unique_id.id] = npcp
    self.save_npc(npcp)

    op = structs.obj_proto_data()
    op.entity.namelist = ['bottle']
    op.entity.name = 'a bottle'
    op.entity.desc = editor.buffer("<p>It's brown and smells sticky inside.</p>")
    op.ldesc = 'An empty bottle has been dropped here.'
    op.unique_id.zone_id = 'stockville'
    op.unique_id.id = 'bottle'
    stockville._obj_proto[op.unique_id.id] = op
    self.save_obj(op)

    # now do the same for the newbie zone
    newbie_zone = zone.zone()

    newbie_zone.name = "the newbie zone"
    newbie_zone.folder = "the newbie zone"
    newbie_zone.id = "newbie_zone"
    newbie_zone.author = "kyle"
    self.save_zone(newbie_zone)

    rm = room.room()
    rm.name = "The Beginning of a Damp Hallway"
    rm.zone_id = "newbie_zone"
    rm.id = "hallway1"
    rm.desc = editor.buffer("<p>This hallway leads onward into the darkness.  The floors are made of hard, compact gravel and dirt.  The walls consist of red bricks with white grout.  This place gives off a real, negative vibe.  To the south is Stockville City.</p>")
    rm.connect(exit.direction.NORTH, 'hallway2')
    rm.connect(exit.direction.SOUTH, 'stockville[reading]')
    newbie_zone._world[rm.id] = rm
    self.save_room(rm)

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
    self.save_room(rm)

    npcp = structs.npc_proto_data()
    npcp.entity.namelist = ['newbie', 'monster']
    npcp.entity.name = 'the newbie monster'
    npcp.entity.desc = editor.buffer("<p>He has googly eyes and drools all over the place as he growls.</p>")
    npcp.ldesc = 'A newbie monster snarls furiously here.'
    npcp.unique_id.zone_id = 'newbie_zone'
    npcp.unique_id.id = 'newbie_monster'
    newbie_zone._npc_proto[npcp.unique_id.id] = npcp
    self.save_npc(npcp)

    op = structs.obj_proto_data()
    op.entity.namelist = ['newbie', 'dagger']
    op.entity.name = 'a newbie dagger'
    op.entity.desc = editor.buffer("<p>It's so bright and shiny, even you can't lose it.</p>")
    op.entity.ldesk = 'Some idiot left a newbie dagger here.'
    op.unique_id.zone_id = 'newbie_zone'
    op.unique_id.id = 'newbie_dagger'
    newbie_zone._obj_proto[op.unique_id.id] = op
    self.save_obj(op)

  def load_world(self, mud):
    for item in self.z_table():
      new_zone = zone.zone()
      new_zone.id = item[0]
      new_zone.name = item[1]
      zone_author = item[2]
      mud.add_zone(new_zone)

    for item in self.wld_table():
      new_room = room.room()
      new_room.zone_id = item[0]
      new_room.id = item[1]
      new_room.name = item[2]
      new_room.desc = editor.buffer(item[3])
      mud.zone_by_id(new_room.zone_id).add_room(new_room)

    for item in self.ex_table():
      dir = exit.direction(item[0])
      o_zone = item[1]
      o_room = item[2]
      d_zone = item[3]
      d_room = item[4]

      if o_zone == d_zone:
        dest_ref = d_room
      else:
        dest_ref = f"{d_zone}[{d_room}]"

      origin = mud.zone_by_id(o_zone).room_by_id(o_room)
      dest = mud.zone_by_id(d_zone).room_by_id(d_room)
      new_exit = exit.exit(dest_ref)

      rm = mud.zone_by_id(o_zone).room_by_id(o_room)
      rm.connect(dir, dest_ref)

    for item in self.npc_table():
      new_npcp = structs.npc_proto_data()
      new_npcp.unique_id.zone_id = item[0]
      new_npcp.unique_id.id = item[1]
      new_npcp.entity.name = item[2]
      new_npcp.ldesc = item[3]
      new_npcp.desc = editor.buffer(item[4])
      mud.zone_by_id(new_npcp.unique_id.zone_id).add_npc(new_npcp)

    for item in self.obj_table():
      new_op = structs.obj_proto_data()
      new_op.unique_id.zone_id = item[0]
      new_op.unique_id.id = item[1]
      new_op.entity.name = item[2]
      new_op.ldesc = item[3]
      new_op.desc = editor.buffer(item[4])
      mud.zone_by_id(new_op.unique_id.zone_id).add_obj(new_op)

if __name__ == '__main__':
  os.system(f"rm test.db")
  db = database("test.db")

  # print("Zone Table")
  # print(db.z_table_str() + "\r\n")
  # print("Room Table")
  # print(db.wld_table_str() + "\r\n")
  # print("Player Table")
  # print(db.p_table_str() + "\r\n")
  # print("Exit Table")
  # print(db.ex_table_str() + "\r\n")
  # print("Zone Table")
  # print(db.z_table_str() + "\r\n")
  # print("Object Table")
  # print(db.obj_table_str() + "\r\n")
  # print("NPC Table")
  # print(db.npc_table_str() + "\r\n")

  
  print(db.table_list())
  db.close()
