import config
import editor
import exit
import room
import string_handling
import sqlite3

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
  c.execute(CREATE_EXIT_TABLE)
  c.execute(CREATE_PLAYER_TABLE)
  c.execute(CREATE_WORLD_TABLE)
  c.execute(CREATE_ZONE_TABLE)

def zone_table_to_str(c):
  ret_val = ""

  c.execute("""SELECT * FROM z_table""")

  for item in c.fetchall():
    ret_val += f"{item[0]:<20}{item[1]:<30}{item[2]:<20}" + "\r\n"

  return ret_val

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

    ret_val += "\r\n"

  return ret_val

def exit_table_to_str(c):
  ret_val = ""

  c.execute("""SELECT * FROM ex_table""")

  ret_val = string_handling.proc_color_codes(f"<c6>Direction:   From:                           To:<c0>\r\n")

  for item in c.fetchall():
    ret_val += f"{exit.direction(item[0]).name:<12} {item[1]:<15} {item[2]:<15} {item[3]:<15} {item[4]:<15}" + "\r\n"

  return ret_val

def exit_table_add_exit(c, origin, ex):

  zone_id, id = string_handling.parse_reference(origin)

  if ex.internal:
    ex.zone_id = zone_id

  c.execute("INSERT INTO ex_table VALUES (:dir, :ozid, :orid, :dzid, :did)", {
    'dir':     ex.direction,
    'ozid':    zone_id,
    'orid':    id,
    'dzid':    ex.zone_id,
    'did':     ex.room_id})

def add_player_to_table(c, player):
  c.execute("INSERT INTO p_table VALUES (:id, :name)", {
    'id':      player.id,
    'name':    player.name})

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

def exit_table_has_exit(c, room_id, zone_id, exit):
  c.execute("SELECT * FROM exit_table WHERE direction=:dir AND id=:id AND zone_id=:zone_id", {
    'zone_id': zone_id,
    'id': room_id})

  if len(c.fetchall()) == 0:
    return False

  return True


def wld_table_contains_room(c, zone_id, id):
  c.execute("SELECT * FROM wld_table WHERE zone_id=:zone_id AND id=:id", {
    'zone_id': zone_id,
    'id': id})

  if len(c.fetchall()) == 0:
    return False

  return True

def add_zone_to_table(c, zn):
  c.execute("INSERT INTO z_table VALUES (:id, :name, :auth)", {
    'id':      zn.id,d
    'name':    zn.name,
    'auth':    zn.author})

def create_database(name):
  return sqlite3.connect(name)

def close_database(conn):
  conn.close()
