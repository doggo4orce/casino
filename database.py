import config
import editor
import exit
import room
import string_handling
import structs
import sqlite3
import zone

CREATE_EXIT_TABLE = """
CREATE TABLE ex_table (
  direction   integer,
  o_zone_id   text,
  o_id        text,
  d_zone_id   text,
  d_id        text
)"""

CREATE_PLAYER_TABLE = """
CREATE TABLE p_table (
  id          integer,
  name        text
)"""

CREATE_WORLD_TABLE = """
CREATE TABLE wld_table (
  zone_id     text,
  id          text,
  name        text,
  description text
)"""

CREATE_ZONE_TABLE = """
CREATE TABLE z_table (
  id          text,
  name        text,
  author      text
)"""

def create_tables(c):
  """Create's all the database tables:
    ex_table     Exit Table
    p_table      Player Table
    wld_table    Room Table
    z_table      Zone Table"""
  c.execute(CREATE_EXIT_TABLE)
  c.execute(CREATE_PLAYER_TABLE)
  c.execute(CREATE_WORLD_TABLE)
  c.execute(CREATE_ZONE_TABLE)

def ex_table_contains_exit(c, rm, ex):
  """Check's if a room's exit matchs with an existing entry's direction in ex_table."""
  room_id = rm.id
  zone_id = rm.zone_id

  c.execute("SELECT * FROM ex_table WHERE o_zone_id=:zone_id AND o_id=:room_id AND direction=:dir", {
    'zone_id': zone_id,
    'room_id': room_id,
    'dir':     ex.direction})

  if len(c.fetchall()) == 0:
    return False

  return True

def ex_table_add_exit(c, rm, ex):
  """Saves a room's exit to ex_table."""
  id = rm.id
  zone_id = rm.zone_id

  if ex.internal:
    ex.zone_id = zone_id

  c.execute("INSERT INTO ex_table VALUES (:dir, :ozid, :orid, :dzid, :did)", {
    'dir':     ex.direction,
    'ozid':    zone_id,
    'orid':    id,
    'dzid':    ex.zone_id,
    'did':     ex.room_id})

def ex_table_delete_exit(c, rm, ex):
  """Delete's a room's exit to ex_table."""
  room_id = rm.id
  zone_id = rm.zone_id

  c.execute("DELETE FROM ex_table WHERE zone_id=:zone_id AND room_id=:room_id AND dir=:dir", {
    'zone_id': zone_id,
    'room_id': room_id,
    'dir':     ex.direction})

def ex_table_to_str(c):
  """Returns a string built from rows of ex_table separated by newlines, prefixed by column headers."""
  c.execute("SELECT * FROM ex_table")

  ret_val = string_handling.proc_color_codes(f"<c6>Direction:   From:                           To:<c0>\r\n")

  for item in c.fetchall():
    ret_val += f"{exit.direction(item[0]).name:<12} {item[1]:<15} {item[2]:<15} {item[3]:<15} {item[4]:<15}\r\n"

  return ret_val

def p_table_contains_player(c, p):
  c.execute("SELECT * FROM p_table WHERE id=:id", {'id':p.id})

  if len(c.fetchall()) == 0:
    return False

  return True

def p_table_add_player(c, p):
  c.execute("INSERT INTO p_table VALUES (:id, :name)", {
    'id',   p.id,
    'name', p.name})

def p_table_delete_player(c, p):
  c.execute("DELETE FROM p_table WHERE id=:id", {'id':p.id})

def p_table_to_str(c):
  c.execute("SELECT * FROM p_table")

  ret_val = string_handling.proc_color_codes(f"<c6>ID:   Name:<c0>\r\n")
 
  for item in c.fetchall():
    ret_val += f"{item[0]:<6}{item[1]}\r\n"

  return ret_val

def z_table_contains_zone(c, zn):
  c.execute("SELECT * FROM z_table WHERE id=:id", {'id' : zn.id})

  if len(c.fetchall()) == 0:
    return False

  return True

def z_table_add_zone(c, zn):
  c.execute("INSERT INTO z_table VALUES (:id, :name, :auth)", {
    'id':      zn.id,
    'name':    zn.name,
    'auth':    zn.author})

def z_table_delete_zone(c, zn):
  c.execute("DELETE FROM z_table where id=:id", {'id':zn.id})

def z_table_to_str(c):
  c.execute("""SELECT * FROM z_table""")

  ret_val = string_handling.proc_color_codes(f"<c6>{'Id:':<{config.MAX_ZONE_ID_LENGTH + 2}}{'Name:':<{config.MAX_ZONE_NAME_LENGTH + 2}}Author:<c0>\r\n")

  for item in c.fetchall():
    ret_val += f"{item[0]:<{config.MAX_ZONE_ID_LENGTH + 2}}{item[1]:<{config.MAX_ZONE_NAME_LENGTH + 2}}{item[2]:<20}" + "\r\n"

  return ret_val

def wld_table_contains_room(c, rm):
  c.execute("SELECT * FROM wld_table WHERE zone_id=:zone_id AND id=:id", {
    'zone_id': rm.zone_id,
    'id': rm.id})

  if len(c.fetchall()) == 0:
    return False

  return True

def wld_table_add_room(c, rm):
  c.execute("INSERT INTO wld_table VALUES (:zone_id, :id, :name, :dscn)", {
    'zone_id': rm.zone_id,
    'id':      rm.id,
    'name':    rm.name,
    'dscn':    str(rm.desc)})

def wld_table_delete_room(c, rm):
  c.execute("DELETE FROM wld_table WHERE zone_id=:zone_id AND id=:id", {
    'zone_id' : zone_id,
    'id' : id})

def wld_table_to_str(c, width=80, format=True, indent=False, numbers=False, color=True):
  ret_val = ""
  c.execute("""SELECT * FROM wld_table""")

  ret_val = string_handling.proc_color_codes(f"<c6>{'Zone:':<{config.MAX_ZONE_ID_LENGTH + 2}}Id:       Name:                           Description:<c0>\r\n")

  for item in c.fetchall():
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

def create_database(name):
  return sqlite3.connect(name)

def close_database(conn):
  conn.close()

if __name__ == '__main__':
  import object
  import pc
  import editor

  conn = create_database(':memory:')
  c = conn.cursor()

  create_tables(c)

  stockville = zone.zone()
  stockville.name = "the city of stockville"
  stockville.folder = "stockville city"
  stockville.id = "stockville"
  stockville.author = "kyle"

  z_table_add_zone(c, stockville)
  
  rm = room.room()
  rm.name = "The Void"
  rm.zone_id = "stockville"
  rm.id = "void"
  rm.desc = editor.buffer("<p>This is a nice, calm, relaxing space. Anything in this room probably wound up here because it's last known location no longer exists. Head down to return to recall.</p>")
  rm.connect(exit.direction.DOWN, 'recall')
  stockville._world[rm.id] = rm

  rm.save_to_db(c)

  rm = room.room()
  rm.name = "Stockville Casino"
  rm.zone_id = "stockville"
  rm.id = "casino"
  rm.desc = editor.buffer("<p>The heavy weight of bad decisions hangs thick in the air.</p>")
  rm.connect(exit.direction.WEST, 'recall')
  stockville._world[rm.id] = rm

  rm.save_to_db(c)

  rm = room.room()
  rm.name = "Stockville Recall"
  rm.zone_id = "stockville"
  rm.id = "recall"
  rm.desc = editor.buffer("<p>This is the recall point of Stockville City.  You should be able to get here by typing <c11>RECALL<c0> at <c6>a<c2>n<c5>y<c0> time.</p>")
  rm.connect(exit.direction.EAST, 'casino')
  rm.connect(exit.direction.WEST, 'reading')
  stockville._world[rm.id] = rm

  rm.save_to_db(c)

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

  rm.save_to_db(c)

  npcp = structs.npc_proto_data()
  npcp.entity.namelist = ['baccarat', 'dealer']
  npcp.entity.name = 'the baccarat card dealer'
  npcp.entity.desc = editor.buffer("<p>He looks like he's straight out of a bluegrass music video.</p>")
  npcp.ldesc = 'A dealer stands here ready to hand out cards.  Maybe you should say hi?'
  npcp.unique_id.zone_id = 'stockville'
  npcp.unique_id.id = 'baccarat_dealer'
  stockville._npc_proto[npcp.unique_id.id] = npcp

  npcp = structs.npc_proto_data()
  npcp.entity.namelist = ['baker', 'fat']
  npcp.entity.name = 'the baker'
  npcp.entity.desc = editor.buffer("<p>He's a nice looking person, but you can see that he has seen battle by the many scars on his body.</p>")
  npcp.ldesc = "A baker is here, but don't give him a bottle."
  npcp.unique_id.zone_id = 'stockville'
  npcp.unique_id.id = 'baker'
  stockville._npc_proto[npcp.unique_id.id] = npcp
  
  ob = structs.obj_proto_data()
  ob.entity.namelist = ['bottle']
  ob.entity.name = 'a bottle'
  ob.entity.desc = editor.buffer("<p>It's brown and smells sticky inside.</p>")
  ob.ldesc = 'An empty bottle has been dropped here.'
  ob.unique_id.zone_id = 'stockville'
  ob.unique_id.id = 'bottle'
  stockville._obj_proto[ob.unique_id.id] = ob

  stockville.save_to_folder()

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

  rm.save_to_db(c)

  rm = room.room()
  rm.name = "A Dark Corner in the Hallway"
  rm.zone_id = "newbie_zone"
  rm.id = "hallway2"
  rm.desc = editor.buffer(
"""<p>I'll start off with a paragraph tag. Then I will add some more lines haphazardly, as I think of
them. Then I can close the tag whenever I want to, and I will!</p>

<p>The proofread <c5>option is made for situations like <c1>this where you could have <c9>really
<c0>awkard spaces between words and tags. Just simply due to the way you enter words through the
editor, they may come through one at a time. And you may put a period after some spaces and forget to
capitalize a word.</p>""")
  rm.connect(exit.direction.SOUTH, 'hallway1')
  newbie_zone._world[rm.id] = rm

  rm.save_to_db(c)

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

  z_table_add_zone(c, newbie_zone)

  rm = stockville._world['recall']

  newbie_zone.save_to_folder()

  print(z_table_to_str(c) + "\r\n")
  print(wld_table_to_str(c) + "\r\n")
  print(ex_table_to_str(c) + "\r\n")

  if wld_table_contains_room(c, rm):
    print(f"The wld_table contains the stockville recall.")
  else:
    print(f"The wld_table does not contain the stockville recall.")

  close_database(conn)

  help(create_tables)
