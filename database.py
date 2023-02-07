import room
import sqlite3

def create_exit_table(c):
  c.execute("""CREATE TABLE ex_table (
               direction   integer,
               o_zone_id   text,
               o_id        text,
               d_zone_id   text,
               d_id        text,
               description text
               )""")

def create_player_table(c):
  c.execute("""CREATE TABLE p_table (
               id          integer,
               name        text
               )""")

def create_room_table(c):
  c.execute("""CREATE TABLE wld_table (
               zone_id     text,
               id          text,
               name        text,
               description text
               )""")

def create_zone_table(c):
  c.execute("""CREATE TABLE z_table (
               id   text,
               name text
               )""")

def add_exit(c, origin, ex):
  c.execute("INSERT INTO ex_table VALUES (:dir, :ozid, :orid, :dzid, :did, :dscn)", {
    'dir':     ex.direction,
    'ozid':    origin.zone_id,
    'orid':    origin.id,
    'dzid':    ex.zone_id,
    'did':     ex.room_id,
    'dscn':    ex.description})

def add_player(c, player):
  c.execute("INSERT INTO p_table VALUES (:id, :name)", {
    'id':      player.id,
    'name':    player.name})

def add_room(c, rm):
  c.execute("INSERT INTO wld_table VALUES (:zone_id, :id, :name, :dscn)", {
    'zone_id': rm.zone_id,
    'id':      rm.id,
    'name':    rm.name,
    'dscn':    rm.desc
  })

def add_zone(c, zone):
  c.execute("INSERT INTO z_table VALUES (:id, :name, :auth)", {
    'id':      zn.id,
    'name':    zn.name,
    'auth':    zn.author})

def create_database(name):
  return sqlite3.connect(name)

def close_database(conn):
  conn.close()
