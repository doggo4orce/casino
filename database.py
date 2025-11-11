import db_handler
import db_table
import exit_data
import mudlog
import npc_proto_data
import obj_proto_data
import room_data
import text_data
import zone_data

class database:
  ALIAS_TABLE        = "alias_table"
  EXIT_TABLE         = "ex_table"
  PREF_NUMERIC_TABLE = "pref_table_numeric"
  PREF_TEXT_TABLE    = "pref_table_text"
  PREF_FLAG_TABLE    = "pref_table_flags"
  NPC_PROTO_TABLE    = "npc_proto_table"
  OBJ_PROTO_TABLE    = "obj_proto_table"
  WORLD_TABLE        = "wld_table"
  PLAYER_TABLE       = "p_table"
  ZONE_TABLE         = "z_table"

  def __init__(self, db_file=None):
    self._db_file = db_file
    self._handler = db_handler.db_handler()

  """connect()                           <- connect to self._db_file
     close()                             <- close connection

     table_by_name(table_name)           <- look up table by name
     table_exists(table_name)            <- check if table exists
     list_tables()                       <- list all tables loaded in db_file
     list_columns(table)                 <- list all columns in table
     fetch_record(table, **clause)       <- fetch
     fetch_records(table, **clause)      <- view table as result set
     num_records(table)                  <- count records in table

     name_used(name)                     <- check if player exists with name
     next_unused_pid()                   <- find smallest unused player ID

     save_exit(zone_id, id, exit)        <- save exit
     has_exit(zone_id, id, direction)    <- check if exit already saved
     delete_exit(zone_id, id, direction) <- delete exit
     num_exits()                         <- count exits

     save_preferences(pc)                <- save all numeric/text/flag prefs

     load_all_prefs_numeric(pc)          <- load all numeric preferences to pc     
     save_pref_numeric(pc, field, value) <- save numeric preference
     save_all_prefs_numeric(pc)          <- save all numeric preferences
     has_pref_numeric(id, field)         <- check if preference already saved
     delete_pref_numeric(id, field)      <- delete preference from database
     delete_all_prefs_numeric(id)        <- delete all numeric preferences by id
     num_prefs_numeric()                 <- count text preferences in database

     load_all_prefs_text(pc)             <- load all text preferences to pc
     save_pref_text(pc, field, value)    <- save text preference
     save_all_prefs_text(pc)             <- save all text preferences
     has_pref_text(id, field)            <- check if preference already saved
     delete_pref_text(id, field)         <- delete preference from database
     delete_all_prefs_text(id)           <- delete all text preferences by id
     num_prefs_text()                    <- count text preferences in database

     load_all_prefs_flag(pc)             <- load all flag preferences to pc
     save_pref_flag(pc, field, value)    <- save flag preference
     save_all_prefs_flag(pc)             <- save all flag preferences
     has_pref_flag(id, field)            <- check if preference already saved
     delete_pref_flag(id, field)         <- delete preference from database
     delete_all_prefs_flag(id)           <- delete all flag preferences by id
     num_prefs_flag()                    <- count flag preferences in database

     save_npc_proto(proto)               <- save npc prototype
     has_npc_proto(zone_id, id)          <- check if npc prototype already saved
     delete_npc_proto(zone_id, id)       <- delete npc prototype from database
     num_npc_protos()                    <- count npc prototypes in database

     save_obj_proto(proto)               <- save object prototype
     has_obj_proto(zone_id, id)          <- check if object prototype already saved
     delete_obj_proto(zone_id, id)       <- delete object prototype
     num_obj_protos()                    <- count object prototypes in database

     save_room(room)                     <- save room (with exits)
     has_room(zone_id, id)               <- check if room already saved
     delete_room(zone_id, id)            <- delete room (with exits) from database
     num_rooms()                         <- count rooms in database

     load_player(pc)                     <- loads player data to player
     save_player(pc)                     <- save player
     has_player(id)                      <- check if player already saved
     delete_player(id)                   <- delete player from database
     num_players()                       <- count players in database

     load_player(pc)                     <- load player from database
     check_password(name, password)      <- check if password is correct
     player_id_by_name(name)             <- lookup player id by name

     create_tables()                     <- creates all world data tables
     show_table(name)                    <- displays contents of table

     zone_table()                        <- displays zones as result set
     world_table()                       <- lists all rooms as result set
     exit_table()                        <- lists all exits as result set
     npc_table()                         <- lists all npc_protos as result set
     obj_table()                         <- lists all obj_protos as result set
     alias_table()                       <- lists all aliases as result set"""

  def connect(self):
    if self._db_file == None:
      mudlog.error("Trying to connect to non-existent database file.")
      return

    self._handler.connect(self._db_file)

  def close(self):
    self._handler.close()

  def table_by_name(self, table_name):
    return self._handler.table_by_name(table_name)

  def table_exists(self, table_name):
    return self._handler.table_exists(table_name)

  def list_tables(self):
    return self._handler.list_tables()

  def list_columns(self, table):
    return self._handler.list_columns(table)

  def list_records(self, table):
    return self._handler.list_records(table)

  def num_records(self, table):
    return self._handler.num_records(table)

  def name_used(self, name):
    return self._handler.get_record(database.PLAYER_TABLE,name=name) is not None

  def next_unused_pid(self):
    j = 1;

    while self.has_player(j):
      j += 1

    return j

  def save_exit(self, zone_id, id, exit):
    if self.has_exit(zone_id, id, exit.direction):
      self.delete_exit(zone_id, id, exit.direction)
  
    ex_table = self.table_by_name(database.EXIT_TABLE)
    ex_table.insert(
      direction=int(exit.direction),
      o_zone_id=zone_id,
      o_id=id,
      d_zone_id=exit.zone_id,
      d_id=exit.id
    )

  def has_exit(self, zone_id, id, direction):
    ex_table = self.table_by_name(database.EXIT_TABLE)
    return ex_table.get_by_pk(direction=int(direction), o_zone_id=zone_id, o_id=id) is not None

  def delete_exit(self, zone_id, id, direction):
    if not self.has_exit(zone_id, id, direction):
      mudlog.error(f"Trying to delete non-existent exit from room {id}@{zone_id} to the {direction.name}.")
      return

    ex_table = self.table_by_name(database.EXIT_TABLE)
    ex_table.delete(direction=int(direction), o_zone_id=zone_id, o_id=id)

  def num_exits(self):
    return self._handler.num_records(database.EXIT_TABLE)

  def load_preferences(self, pc):
    self.load_all_prefs_numeric(pc)
    self.load_all_prefs_text(pc)
    self.load_all_prefs_flag(pc)

  def save_preferences(self, pc):
    self.save_all_prefs_numeric(pc)
    self.save_all_prefs_text(pc)
    self.save_all_prefs_flag(pc)

  def save_pref_numeric(self, pc, field, value):
    if self.has_pref_numeric(pc.player_id, field):
      self.delete_pref_numeric(pc.player_id, field)

    self.table_by_name(database.PREF_NUMERIC_TABLE).insert(id=pc.player_id, field=field, value=value)

  def load_all_prefs_numeric(self, pc):
    for record in self.table_by_name(database.PREF_NUMERIC_TABLE).search(id=pc.player_id):
      pc.set_pref(record['field'], record['value'])

  def save_all_prefs_numeric(self, pc):
    for field in pc.numeric_prefs.fields():
      self.save_pref_numeric(pc, field, getattr(pc.numeric_prefs, field))

  def has_pref_numeric(self, id, field):
    return self.table_by_name(database.PREF_NUMERIC_TABLE).get_by_pk(id=id, field=field) is not None

  def delete_pref_numeric(self, id, field):
    if not self.has_pref_numeric(id, field):
      mudlog.error(f"Trying to delete non-existent numeric preference {field} for {name}.")
      return

    self.table_by_name(database.PREF_NUMERIC_TABLE).delete(id=id, field=field)

  def delete_all_prefs_numeric(self, id):
    self.table_by_name(database.PREF_NUMERIC_TABLE).delete(id=id)

  def num_prefs_numeric(self):
    return self.table_by_name(database.PREF_NUMERIC_TABLE).num_records()

  def save_pref_text(self, pc, field, value):
    if self.has_pref_text(pc.player_id, field):
      self.delete_pref_text(pc.player_id, field)

    self.table_by_name(database.PREF_TEXT_TABLE).insert(id=pc.player_id, field=field, value=value)

  def load_all_prefs_text(self, pc):
    for record in self.table_by_name(database.PREF_TEXT_TABLE).search(id=pc.player_id):
      pc.set_pref(record['field'], record['value'])

  def save_all_prefs_text(self, pc):
    for field in pc.text_prefs.fields():
      self.save_pref_text(pc, field, getattr(pc.text_prefs, field))

  def has_pref_text(self, id, field):
    return self.table_by_name(database.PREF_TEXT_TABLE).get_by_pk(id=id, field=field) is not None

  def delete_pref_text(self, id, field):
    if not self.has_pref_text(id, field):
      mudlog.error(f"Trying to delete non-existant text preference {field} for {name}.")
      return

    self.table_by_name(database.PREF_TEXT_TABLE).delete(id=id, field=field)

  def delete_all_prefs_text(self, id):
    self.table_by_name(database.PREF_TEXT_TABLE).delete(id=id)

  def num_prefs_text(self):
    return self.table_by_name(database.PREF_TEXT_TABLE).num_records()

  def load_all_prefs_flag(self, pc):
    for record in self.table_by_name(database.PREF_FLAG_TABLE).search(id=pc.player_id):
      pc.set_pref(record['field'], bool(record['value']))

  def save_pref_flag(self, pc, field, value):
    if self.has_pref_flag(pc.player_id, field):
      self.delete_pref_flag(pc.player_id, field)

    self.table_by_name(database.PREF_FLAG_TABLE).insert(id=pc.player_id, field=field, value=int(value))

  def save_all_prefs_flag(self, pc):
    for field in pc.flag_prefs.fields():
      self.save_pref_flag(pc, field, getattr(pc.flag_prefs, field))

  def has_pref_flag(self, id, field):
    return self.table_by_name(database.PREF_FLAG_TABLE).get_by_pk(id=id, field=field) is not None

  def delete_pref_flag(self, id, field):
    if not self.has_pref_flag(id, field):
      mudlog.error(f"Trying to delete non-existent preference flag {field} for player {id}.")

    self.table_by_name(database.PREF_FLAG_TABLE).delete(id=id,field=field)

  def delete_all_prefs_flags(self, id):
    self.table_by_name(database.PREF_FLAG_TABLE).delete(id=id)

  def num_prefs_flag(self):
    return self._handler.num_records(database.PREF_FLAG_TABLE)

  def save_npc_proto(self, proto):
    if self.has_npc_proto(proto.zone_id, proto.id):
      self.delete_npc_proto(proto.zone_id. proto.id)

    self.table_by_name(database.NPC_PROTO_TABLE).insert(
      zone_id=proto.zone_id,
      id=proto.id,
      name=proto.name,
      ldesc=proto.ldesc,
      desc=proto.ldesc
    )

    for alias in proto.aliases():
      self.save_alias(proto.zone_id, proto.id, 'npc', alias)

  def has_npc_proto(self, zone_id, id):
    return self.table_by_name(database.NPC_PROTO_TABLE).get_by_pk(zone_id=zone_id, id=id) is not None

  def delete_npc_proto(self, zone_id, id):
    if not self.has_npc_proto(zone_id, id):
      mudlog.error(f"Trying to delete non-existent npc proto {id}@{zone_id}.")
      return

    self.table_by_name(database.NPC_PROTO_TABLE).delete(zone_id=zone_id, id=id)
    self.table_by_name(database.ALIAS_TABLE).delete(zone_id=zone_id, id=id, type='npc')

  def num_npc_protos(self):
    return self._handler.num_records(database.NPC_PROTO_TABLE)

  def save_obj_proto(self, proto):
    if self.has_obj_proto(proto.zone_id, proto.id):
      self.delete_obj_proto(proto.zone_id, proto.id)

    self.table_by_name(database.OBJ_PROTO_TABLE).insert(
      zone_id=proto.zone_id,
      id=proto.id,
      name=proto.name,
      ldesc=proto.ldesc,
      desc=proto.desc
    )

    for alias in proto.aliases():
      self.save_alias(proto.zone_id, proto.id, 'obj', alias)

  def has_obj_proto(self, zone_id, id):
    obj_proto_table = self.table_by_name(database.OBJ_PROTO_TABLE)
    return obj_proto_table.get_by_pk(zone_id=zone_id, id=id) is not None

  def delete_obj_proto(self, zone_id, id):
    if not self.has_obj_proto(zone_id, id):
      mudlog.error(f"Trying to delete non-existent object proto {id}@{zone_id}.")
      return

    obj_proto_table = self.table_by_name(database.OBJ_PROTO_TABLE)
    obj_proto_table.delete(zone_id=zone_id, id=id)

    alias_table = self.table_by_name(database.ALIAS_TABLE)
    alias_table.delete(zone_id=zone_id, id=id, type='obj')

  def num_obj_protos(self):
    obj_proto_table = self.table_by_name(database.OBJ_PROTO_TABLE)
    return obj_proto_table.num_records()

  def save_room(self, room):
    if self.has_room(room.zone_id, room.id):
      self.delete_room(room.zone_id, room.id)

    wld_table = self.table_by_name(database.WORLD_TABLE)
    wld_table.insert(
      zone_id=room.zone_id,
      id=room.id,
      name=room.name,
      desc=room.desc.text,
    )

    for ex in room.exits:
      self.save_exit(room.zone_id, room.id, ex)

  def has_room(self, zone_id, id):
    return self.table_by_name(database.WORLD_TABLE).get_by_pk(zone_id=zone_id, id=id) != None

  def delete_room(self, zone_id, id):
    if not self.has_room(zone_id, id):
      mudlog.error(f"Trying to delete non-existent room {id}@{zone_id}.")
      return

    wld_table = self.table_by_name(database.WORLD_TABLE)
    wld_table.delete(zone_id=zone_id, id=id)

    ex_table = self.table_by_name(database.EXIT_TABLE)
    ex_table.delete(o_zone_id=zone_id, o_id=id)

  def num_rooms(self):
    return self.table_by_name(database.WORLD_TABLE).num_records()

  def save_player(self, pc):
    if self.has_player(pc.player_id):
      self.delete_player(pc.player_id)

    p_table = self.table_by_name(database.PLAYER_TABLE)
    p_table.insert(id=pc.player_id, name=pc.name, password=pc.password)

  def has_player(self, id):
    return self.table_by_name(database.PLAYER_TABLE).get_by_pk(id=id) is not None

  def delete_player(self, id):
    if not self.has_player(id):
      mudlog.error(f"Trying to delete non-existent player with id {pc.player_id}.")
      return

    self.table_by_name(database.PLAYER_TABLE).delete(id=id)

  def num_players(self):
    return self.table_by_name(database.PLAYER_TABLE).num_records()

  def load_player(self, pc, player_id):
    record = self.table_by_name(database.PLAYER_TABLE).get_by_pk(id=player_id)

    pc.name = record['name']
    pc.password = record['password']
    pc.player_id = player_id

    self.load_all_prefs_flag(pc)
    self.load_all_prefs_numeric(pc)
    self.load_all_prefs_text(pc)

  def check_password(self, name, password):
    rs = self.table_by_name(database.PLAYER_TABLE).search(name=name)
    record = rs[0]
    return record['password'] == password

  def player_id_by_name(self, name):
    rs = self.table_by_name(database.PLAYER_TABLE).search(name=name)

    if rs.num_results == 0:
      return None

    record = rs[0]
    player_id = record['id']

    if rs.num_results > 1:
      mudlog.error(f"found two players named {name} when looking up player_id.  Returning {player_id}")

    return player_id

  def save_zone(self, zone):
    if self.has_zone(zone.id):
      self.delete_zone(zone.id)

    self.table_by_name(database.ZONE_TABLE).insert(id=zone.id, name=zone.name, author=zone.author)

    for id in zone.list_room_ids():
      self.save_room(zone.room_by_id(id))

    for id in zone.list_npc_ids():
      self.save_npc_proto(zone.npc_by_id(id))

    for id in zone.list_obj_ids():
      self.save_obj_proto(zone.obj_by_id(id))

  def has_zone(self, id):
    z_table = self.table_by_name(database.ZONE_TABLE)
    return z_table.get_by_pk(id=id) is not None

  def delete_zone(self, id):
    if not self.has_zone(id):
      mudlog.error(f"Trying to delete non-existent zone with id {zone.id}.")
      return

    self.table_by_name(database.ZONE_TABLE).delete(id=id)
    self.table_by_name(database.WORLD_TABLE).delete(zone_id=id)
    self.table_by_name(database.OBJ_PROTO_TABLE).delete(zone_id=id)
    self.table_by_name(database.NPC_PROTO_TABLE).delete(zone_id=id)
    self.table_by_name(database.EXIT_TABLE).delete(o_zone_id=id)

  def num_zones(self):
    return self.table_by_name(database.ZONE_TABLE).num_records()

  def save_alias(self, zone_id, id, type, alias):
    if self.has_alias(zone_id, id, type, alias):
      self.delete_alias(zone_id, id, type, alias)

    self.table_by_name(database.ALIAS_TABLE).insert(zone_id=zone_id, id=id, type=type, alias=alias)

  def has_alias(self, zone_id, id, type, alias):
    alias_table = self.table_by_name(database.ALIAS_TABLE)
    return alias_table.get_by_pk(zone_id=zone_id, id=id, type=type, alias=alias) is not None

  def delete_alias(self, zone_id, id, type, alias):
    if not self.has_alias(zone_id, id, type, alias):
      mudlog.error(f"Trying to delete non-existant alias {alias} from {type} {id}@{zone_id}.")
      return

    alias_table = self.table_by_name(database.ALIAS_TABLE)
    alias_table.delete(zone_id=zone_id, id=id, type=type, alias=alias)

  def num_aliases(self):
    return self.table_by_name(database.ALIAS_TABLE).num_records()

  def show_table(self, name):
    return self.table_by_name(name).search()

  def create_tables(self):

    exit_table = db_table.db_table(self._handler, database.EXIT_TABLE)
    pref_numeric_table = db_table.db_table(self._handler, database.PREF_NUMERIC_TABLE)
    pref_text_table = db_table.db_table(self._handler, database.PREF_TEXT_TABLE)
    pref_flag_table = db_table.db_table(self._handler, database.PREF_FLAG_TABLE)
    npc_proto_table = db_table.db_table(self._handler, database.NPC_PROTO_TABLE)
    obj_proto_table = db_table.db_table(self._handler, database.OBJ_PROTO_TABLE)
    npc_proto_table = db_table.db_table(self._handler, database.NPC_PROTO_TABLE)
    wld_table = db_table.db_table(self._handler, database.WORLD_TABLE)
    p_table = db_table.db_table(self._handler, database.PLAYER_TABLE)
    z_table = db_table.db_table(self._handler, database.ZONE_TABLE)
    alias_table = db_table.db_table(self._handler, database.ALIAS_TABLE)

    exit_table.create(
      ("direction", int, True),
      ("o_zone_id", str, True),
      ("o_id", str, True),
      ("d_zone_id", str, False),
      ("d_id", str, False)
    )

    pref_numeric_table.create(
      ("id", int, True),
      ("field", str, True),
      ("value", int, False)
    )

    pref_text_table.create(
      ("id", int, True),
      ("field", str, True),
      ("value", str, False)
    )

    pref_flag_table.create(
      ("id", int, True),
      ("field", str, True),
      ("value", int, False)
    )

    obj_proto_table.create(
      ("zone_id", str, True),
      ("id", str, True),
      ("name", str, False),
      ("ldesc", str, False),
      ("desc", str, False)
    )

    npc_proto_table.create(
      ("zone_id", str, True),
      ("id", str, True),
      ("name", str, False),
      ("ldesc", str, False),
      ("desc", str, False)
    )

    wld_table.create(
      ("zone_id", str, True),
      ("id", str, True),
      ("name", str, False),
      ("desc", str, False)
    )

    p_table.create(
      ("id", int, True),
      ("name", str, False),
      ("password", str, False)
    )

    z_table.create(
      ("id", str, True),
      ("name", str, False),
      ("author", str, False)
    )

    alias_table.create(
      ("zone_id", str, True),
      ("id", str, True),
      ("type", str, True),
      ("alias", str, True)
    )

  def zone_table(self):
    z_table = self.table_by_name(database.ZONE_TABLE)
    return z_table.search()
    
  def world_table(self):
    wld_table = self.table_by_name(database.WORLD_TABLE)
    return wld_table.search()
    
  def exit_table(self):
    ex_table = self.table_by_name(database.EXIT_TABLE)
    return ex_table.search()
    
  def npc_table(self):
    npc_proto_table = self.table_by_name(database.NPC_PROTO_TABLE)
    return npc_proto_table.search()
    
  def obj_table(self):
    obj_proto_table = self.table_by_name(database.OBJ_PROTO_TABLE)
    return obj_proto_table.search()
    
  def alias_table(self):
    alias_table = self.table_by_name(database.ALIAS_TABLE)
    return alias_table.search()
    
  def load_stock(self):
    stockville = zone_data.zone_data()
    stockville.name = "the city of stockville"
    stockville.id = "stockville"
    stockville.author = "kyle"

    rm = room_data.room_data()
    rm.name = "The Void"
    rm.zone_id = "stockville"
    rm.id = "void"
    rm.desc = text_data.text_data("<p>This is a nice, calm, relaxing space. Anything in this room probably wound up here because its last known location no longer exists. Head down to return to recall.</p>")

    rm.connect(exit_data.direction.DOWN, 'stockville', 'recall')
    stockville._world[rm.id] = rm

    rm = room_data.room_data()
    rm.name = "Stockville Casino"
    rm.zone_id = "stockville"
    rm.id = "casino"
    rm.desc = text_data.text_data("<p>The heavy weight of bad decisions hangs thick in the air.</p>")
    rm.connect(exit_data.direction.WEST, 'stockville', 'recall')
    stockville._world[rm.id] = rm

    rm = room_data.room_data()
    rm.name = "Stockville Recall"
    rm.zone_id = "stockville"
    rm.id = "recall"
    rm.desc = text_data.text_data("<p>This is the recall point of Stockville City.  You should be able to get here by typing <c11>RECALL<c0> at <c6>a<c2>n<c5>y<c0> time.</p>")
    rm.connect(exit_data.direction.EAST, 'stockville', 'casino')
    rm.connect(exit_data.direction.WEST, 'stockville', 'reading')
    stockville._world[rm.id] = rm

    rm = room_data.room_data()
    rm.name = "Reading Room"
    rm.zone_id = "stockville"
    rm.id = "reading"
    rm.desc = text_data.text_data("""<p>This would a great place to catch up on news from the non-existent message board that should be here!  To the north is the entrance to a different zone.</p>

  <c9>HINT HINT<c0>:  Time to make a message board!
  ---------
       But you can see here that this text
       is not formatted along with the
       paragraph above.  I can even use the
       format command while editing this
       room and this mini pargraph will not
       be harmed!  <(^_^)7   6(*-*)^

<p>But now I've entered paragraph mode again. So all of this text will be formatted according to my user-set preference of how wide I want my screen to be.</p>""")
    rm.connect(exit_data.direction.EAST, 'stockville', 'recall')
    rm.connect(exit_data.direction.NORTH, 'newbie_zone', 'hallway1')
    stockville.add_room(rm)

    npcp = npc_proto_data.npc_proto_data()
    npcp.reset_aliases('baccarat', 'dealer')
    npcp.name = 'the baccarat card dealer'
    npcp.desc = "<p>He looks like he's straight out of a bluegrass music video.</p>"
    npcp.ldesc = 'A dealer stands here ready to hand out cards.'
    npcp.zone_id = 'stockville'
    npcp.id = 'baccarat_dealer'
    stockville.add_npc(npcp)

    npcp = npc_proto_data.npc_proto_data()
    npcp.reset_aliases('baker', 'fat')
    npcp.name = 'the baker'
    npcp.desc = "<p>Hes a nice looking person, but you can see that he has seen battle by the many scars on his body.</p>"
    npcp.ldesc = "A baker is here, but dont give him a bottle."
    npcp.zone_id = 'stockville'
    npcp.id = 'baker'
    stockville.add_npc(npcp)

    op = obj_proto_data.obj_proto_data()
    op.reset_aliases('baccarat', 'gaming', 'table')
    op.name = 'a baccarat table'
    op.desc = "<p>It's rude to look over player's shoulders.  If you want to watch the game, sit down and play.</p>"
    op.ldesc = "A gaming table has been set up here."
    op.zone_id = 'stockville'
    op.id = 'baccarat_table'
    stockville.add_obj(op)

    op = obj_proto_data.obj_proto_data()
    op.reset_aliases('red', 'chip')
    op.name = 'a red chip'
    op.desc = "<p>It's a <c1>red<c0> coin with a Stockville Casino logo imprinted upon it.</p>"
    op.ldesc = "A red casino chip has been left on the ground."
    op.zone_id = 'stockville'
    op.id = 'red_chip'
    stockville.add_obj(op)

    op = obj_proto_data.obj_proto_data()
    op.reset_aliases('green', 'chip')
    op.name = 'a green chip'
    op.desc = "<p>It's a <c2>green<c0> coin with a Stockville Casino logo imprinted upon it.</p>"
    op.ldesc = "A green casino chip has been left on the ground."
    op.zone_id = 'stockville'
    op.id = 'green_chip'
    stockville.add_obj(op)

    op = obj_proto_data.obj_proto_data()
    op.reset_aliases('black', 'chip')
    op.name = 'a black chip'
    op.desc = "<p>It's a <c6>black<c0> coin with a Stockville Casino logo imprinted upon it.</p>"
    op.ldesc = "A black casino chip has been left on the ground."
    op.zone_id = 'stockville'
    op.id = 'black_chip'
    stockville.add_obj(op)

    op = obj_proto_data.obj_proto_data()
    op.reset_aliases('purple', 'chip')
    op.name = 'a purple chip'
    op.desc = "<p>It's a <c5>purple<c0> coin with a Stockville Casino logo imprinted upon it.</p>"
    op.ldesc = "A purple casino chip has been left on the ground."
    op.zone_id = 'stockville'
    op.id = 'purple_chip'
    stockville.add_obj(op)

    op = obj_proto_data.obj_proto_data()
    op.reset_aliases('bottle')
    op.name = 'a bottle'
    op.desc = "<p>It's brown, sticky, and smells like stale beer inside.</p>"
    op.ldesc = 'An empty bottle has been dropped here.'
    op.zone_id = 'stockville'
    op.id = 'bottle'
    stockville.add_obj(op)
    self.save_zone(stockville)

    # now do the same for the newbie zone
    newbie_zone = zone_data.zone_data()
    newbie_zone.name = "the newbie zone"
    newbie_zone.id = "newbie_zone"
    newbie_zone.author = "kyle"

    rm = room_data.room_data()
    rm.name = "The Beginning of a Damp Hallway"
    rm.zone_id = "newbie_zone"
    rm.id = "hallway1"
    rm.desc = text_data.text_data("<p>This hallway leads onward into the darkness.  The floors are made of hard, compact gravel and dirt.  The walls consist of red bricks with white grout.  This place gives off a real, negative vibe.  To the south is Stockville City.</p>")
    rm.connect(exit_data.direction.NORTH, 'newbie_zone', 'hallway2')
    rm.connect(exit_data.direction.SOUTH, 'stockville', 'reading')
    newbie_zone.add_room(rm)

    rm = room_data.room_data()
    rm.name = "A Dark Corner in the Hallway"
    rm.zone_id = "newbie_zone"
    rm.id = "hallway2"
    rm.desc = text_data.text_data("""<p>Ill start off with a paragraph tag. Then I will add some more lines haphazardly, as I think of
them. Then I can close the tag whenever I want to, and I will!</p>

<p>The proofread <c5>option is made for situations like <c1>this where you could have <c9>really
<c0>awkard spaces between words and tags. Just simply due to the way you enter words through the
editor, they may come through one at a time. And you may put a period after some spaces and forget to
capitalize a word.</p>""")
    rm.connect(exit_data.direction.SOUTH, 'newbie_zone', 'hallway1')
    newbie_zone.add_room(rm)

    npcp = npc_proto_data.npc_proto_data()
    npcp.reset_aliases('newbie', 'monster')
    npcp.name = 'the newbie monster'
    npcp.desc = "<p>He has googly eyes and drools all over the place as he growls.</p>"
    npcp.ldesc = 'A newbie monster snarls furiously here.'
    npcp.zone_id = 'newbie_zone'
    npcp.id = 'newbie_monster'
    newbie_zone.add_npc(npcp)

    op = obj_proto_data.obj_proto_data()
    op.reset_aliases('newbie', 'dagger')
    op.name = 'a newbie dagger'
    op.desc = "<p>It's so bright and shiny, even you can't lose it.</p>"
    op.ldesk = 'Some idiot left a newbie dagger here.'
    op.zone_id = 'newbie_zone'
    op.id = 'newbie_dagger'
    newbie_zone.add_obj(op)

    self.save_zone(newbie_zone)

  def load_world(self, mud):

    for zone in self.zone_table():
      new_zone = zone_data.zone_data()
      new_zone.id = zone['id']
      new_zone.name = zone['name']
      zone_author = zone['author']
      mud.add_zone(new_zone)

    for room in self.world_table():
      new_room = room_data.room_data()
      new_room.zone_id = room['zone_id']
      new_room.id = room['id']
      new_room.name = room['name']
      new_room.desc.text = room['desc']
      zone = mud.zone_by_id(new_room.zone_id)

      if zone is None:
        mudlog.warning(f"suppressing room {new_room.id} from zone {new_room.zone_id} which does not exist.")
        continue

      zone.add_room(new_room)

    for exit in self.exit_table():
      dir = exit_data.direction(exit['direction'])
      o_zone_id = exit['o_zone_id']
      o_id = exit['o_id']
      d_zone_id = exit['d_zone_id']
      d_id = exit['d_id']

      origin_room = mud.room_by_uid(o_zone_id, o_id)

      if origin_room is None:
        mudlog.warning(f"suppressing exit {o_id}@{o_zone_id} -> {d_id}@{d_zone_id} since origin room does not exist.")
        continue

      origin_room.connect(dir, d_zone_id, d_id)

    for npcp in self.npc_table():
      new_npcp = npc_proto_data.npc_proto_data()
      new_npcp.zone_id = npcp['zone_id']
      new_npcp.id = npcp['id']
      new_npcp.name = npcp['name']
      new_npcp.ldesc = npcp['ldesc']
      new_npcp.desc = npcp['desc']
      zone = mud.zone_by_id(new_npcp.zone_id)

      if zone is None:
        mudlog.warning(f"suppressing npc {new_npcp.id} from zone {new_npcp.zone_id} which does not exist.")
        continue

      zone.add_npc(new_npcp)

    for objp in self.obj_table():
      nobjp = obj_proto_data.obj_proto_data()
      nobjp.zone_id = objp['zone_id']
      nobjp.id = objp['id']
      nobjp.name = objp['name']
      nobjp.ldesc = objp['ldesc']
      nobjp.desc = objp['desc']
      zone = mud.zone_by_id(nobjp.zone_id)

      if zone is None:
        mudlog.warning(f"suppressing npc {new_objp.id} from zone {new_objp.zone_id} which does not exist.")
        continue

      zone.add_obj(nobjp)

    for alias in self.alias_table():
      if alias['type'] == "npc":
        npc = mud.npc_by_uid(alias['zone_id'], alias['id'])
        if npc is None:
          mudlog.warning(f"suppressing alias {alias['alias']} for npc proto {alias['id']}@{alias['zone_id']} which does not exist")
          continue
        npc.add_alias(alias['alias'])
      elif alias['type'] == "obj":
        obj = mud.obj_by_uid(alias['zone_id'], alias['id'])
        if npc is None:
          mudlog.warning(f"suppressing alias {alias['alias']} for obj proto {alias['id']}@{alias['zone_id']} which does not exist")
          continue
        obj.add_alias(alias['alias'])