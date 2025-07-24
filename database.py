import db_handler
import mudlog

class database:
  NAMELIST_TABLE     = "namelist_table"
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

     save_exit(zone_id, id, exit)        <- save exit
     has_exit(zone_id, id, direction)    <- check if exit already saved
     delete_exit(zone_id, id, direction) <- delete exit
     num_exits()                         <- count exits

     save_preferences(pc)                <- save all numeric/text/flag prefs
     
     save_pref_numeric(pc, field, value) <- save numeric preference
     save_all_prefs_numeric(pc)          <- save all numeric preferences
     has_pref_numeric(id, field)         <- check if preference already saved
     delete_pref_numeric(id, field)      <- delete preference from database
     delete_all_prefs_numeric(id)        <- delete all numeric preferences by id
     num_prefs_numeric()                 <- count text preferences in database

     save_pref_text(pc, field, value)    <- save text preference
     save_all_prefs_text(pc)             <- save all text preferences
     has_pref_text(id, field)            <- check if preference already saved
     delete_pref_text(id, field)         <- delete preference from database
     delete_all_prefs_text(id)           <- delete all text preferences by id
     num_prefs_text()                    <- count text preferences in database

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

     create_tables()                     <- creates all world data tables
     show_table(name)                    <- displays contents of table"""

  def connect(self):
    if self._db_file == None:
      mudlog.error("Trying to connect to non-existent database file.")
      return

    self._handler.connect(self._db_file)

  def close(self):
    self._handler.close()

  def save_exit(self, zone_id, id, exit):
    if self.has_exit(zone_id, id, exit.direction):
      self.delete_exit(zone_id, id, exit.direction)
  
    self._handler.insert_record(database.EXIT_TABLE,
      direction=int(exit.direction),
      o_zone_id=zone_id,
      o_id=id,
      d_zone_id=exit.zone_id,
      d_id=exit.id
    )

  def has_exit(self, zone_id, id, direction):
    return self._handler.get_record(database.EXIT_TABLE,
      direction=int(direction),
      o_zone_id=zone_id,
      o_id=id
    ) != None

  def delete_exit(self, zone_id, id, direction):
    if not self.has_exit(zone_id, id, direction):
      mudlog.error(f"Trying to delete non-existent exit from room {id}@{zone_id} to the {direction.name}.")
      return

    self._handler.delete_records(database.EXIT_TABLE,
      direction=int(direction),
      o_zone_id=zone_id,
      o_id=id
    )

  def num_exits(self):
    return self._handler.num_records(database.EXIT_TABLE)

  def save_preferences(self, pc):
    self.save_all_pref_numeric(pc)
    self.save_all_pref_text(pc)
    self.save_all_pref_flag(pc)

  def save_pref_numeric(self, pc, field, value):
    if self.has_pref_numeric(pc.player_id, field):
      self.delete_pref_numeric(pc.player_id, field)

    self._handler.insert_record(database.PREF_NUMERIC_TABLE,
      id=pc.player_id,
      field=field,
      value=value
    )

  def save_all_prefs_numeric(self, pc):
    for field in pc.numeric_prefs.fields():
      self.save_pref_numeric(pc, field, getattr(pc.numeric_prefs, field))

  def has_pref_numeric(self, id, field):
    return self._handler.get_record(database.PREF_NUMERIC_TABLE,
      id=id,
      field=field
    ) != None

  def delete_pref_numeric(self, id, field):
    if not self.has_pref_numeric(id, field):
      mudlog.error(f"Trying to delete non-existent numeric preference {field} for {name}.")
      return

    self._handler.delete_records(database.PREF_NUMERIC_TABLE,
      id=id,
      field=field
    )

  def delete_all_prefs_numeric(self, id):
    self._handler.delete_records(database.PREF_NUMERIC_TABLE,
      id=id
    )

  def num_prefs_numeric(self):
    return self._handler.num_records(database.PREF_NUMERIC_TABLE)

  def save_pref_text(self, pc, field, value):
    if self.has_pref_text(pc.player_id, field):
      self.delete_pref_text(pc.player_id, field)

    self._handler.insert_record(database.PREF_TEXT_TABLE,
      id=pc.player_id,
      field=field,
      value=value
    )

  def save_all_prefs_text(self, pc):
    for field in pc.text_prefs.fields():
      self.save_pref_text(pc, field, getattr(pc.text_prefs, field))

  def has_pref_text(self, id, field):
    return self._handler.get_record(database.PREF_TEXT_TABLE,
      id=id,
      field=field
    ) != None

  def delete_pref_text(self, id, field):
    if not self.has_pref_text(id, field):
      mudlog.error(f"Trying to delete non-existant text preference {field} for {name}.")
      return

    self._handler.delete_records(database.PREF_TEXT_TABLE,
      id=id,
      field=field
    )

  def delete_all_prefs_text(self, id):
    self._handler.delete_records(database.PREF_TEXT_TABLE,
      id=id
    )

  def num_prefs_text(self):
    return self._handler.num_records(database.PREF_TEXT_TABLE)

  def save_pref_flag(self, pc, field, value):
    if self.has_pref_flag(pc.player_id, field):
      self.delete_pref_flag(pc.player_id, field)

    self._handler.insert_record(database.PREF_FLAG_TABLE,
      id=pc.player_id,
      field=field,
      value=int(value)
    )

  def save_all_prefs_flag(self, pc):
    for field in pc.flag_prefs.fields():
      self.save_pref_flag(pc, field, getattr(pc.flag_prefs, field))

  def has_pref_flag(self, id, field):
    return self._handler.get_record(database.PREF_FLAG_TABLE,
      id=id,
      field=field
    ) != None

  def delete_pref_flag(self, id, field):
    if not self.has_pref_flag(id, field):
      mudlog.error(f"Trying to delete non-existent preference flag {field} for player {id}.")

    self._handler.delete_records(database.PREF_FLAG_TABLE,
      id=id,
      field=field
    )

  def delete_all_prefs_flags(self, id):
    self._handler.delete_records(database.PREF_FLAG_TABLE,
      id=id
    )

  def num_prefs_flag(self):
    return self._handler.num_records(database.PREF_FLAG_TABLE)

  def save_npc_proto(self, proto):
    if self.has_npc_proto(proto.zone_id, proto.id):
      self.delete_npc_proto(proto.zone_id. proto.id)

    self._handler.insert_record(database.NPC_PROTO_TABLE,
      zone_id=proto.zone_id,
      id=proto.id,
      name=proto.name,
      ldesc=proto.ldesc,
      desc=proto.ldesc
    )

    for alias in proto.aliases():
      self.save_alias(proto.zone_id, proto.id, 'npc', alias)

  def has_npc_proto(self, zone_id, id):
    return self._handler.get_record(database.NPC_PROTO_TABLE,
      zone_id=zone_id,
      id=id
    ) != None

  def delete_npc_proto(self, zone_id, id):
    if not self.has_npc_proto(zone_id, id):
      mudlog.error(f"Trying to delete non-existent npc proto {id}@{zone_id}.")
      return

    self._handler.delete_records(database.NPC_PROTO_TABLE,
      zone_id=zone_id,
      id=id
    )

    self._handler.delete_records(database.NAMELIST_TABLE,
      zone_id=zone_id,
      id=id,
      type='npc'
    )

  def num_npc_protos(self):
    return self._handler.num_records(database.NPC_PROTO_TABLE)

  def save_obj_proto(self, proto):
    if self.has_obj_proto(proto.zone_id, proto.id):
      self.delete_obj_proto(proto.zone_id, proto.id)

    self._handler.insert_record(database.OBJ_PROTO_TABLE,
      zone_id=proto.zone_id,
      id=proto.id,
      name=proto.name,
      ldesc=proto.ldesc,
      desc=proto.ldesc
    )

    for alias in proto.aliases():
      self.save_alias(proto.zone_id, proto.id, 'obj', alias)

  def has_obj_proto(self, zone_id, id):
    return self._handler.get_record(database.OBJ_PROTO_TABLE,
      zone_id=zone_id,
      id=id
    ) != None

  def delete_obj_proto(self, zone_id, id):
    if not self.has_obj_proto(zone_id, id):
      mudlog.error(f"Trying to delete non-existent object proto {id}@{zone_id}.")
      return

    self._handler.delete_records(database.OBJ_PROTO_TABLE,
      zone_id=zone_id,
      id=id
    )

    self._handler.delete_records(database.NAMELIST_TABLE,
      zone_id=zone_id,
      id=id,
      type='obj'
    )

  def num_obj_protos(self):
    return self._handler.num_records(database.OBJ_PROTO_TABLE)

  def save_room(self, room):
    if self.has_room(room.zone_id, room.id):
      self.delete_room(room.zone_id, room.id)

    self._handler.insert_record(database.WORLD_TABLE,
      zone_id=room.zone_id,
      id=room.id,
      name=room.name,
      desc=room.desc,
    )

    for ex in room.exits:
      self.save_exit(room.zone_id, room.id, ex)

  def has_room(self, zone_id, id):
    return self._handler.get_record(database.WORLD_TABLE,
      zone_id=zone_id,
      id=id
    ) != None

  def delete_room(self, zone_id, id):
    if not self.has_room(zone_id, id):
      mudlog.error(f"Trying to delete non-existent room {id}@{zone_id}.")
      return

    self._handler.delete_records(database.WORLD_TABLE,
      zone_id=zone_id,
      id=id
    )

    self._handler.delete_records(database.EXIT_TABLE,
      o_zone_id=zone_id,
      o_id=id
    )

  def num_rooms(self):
    return self._handler.num_records(database.WORLD_TABLE)

  def save_player(self, pc):
    if self.has_player(pc.player_id):
      self.delete_player(pc.player_id)

    self._handler.insert_record(database.PLAYER_TABLE,
      id=pc.player_id,
      name=pc.name,
      password=pc.password
    )

  def has_player(self, id):
    return self._handler.get_record(database.PLAYER_TABLE,
      id=id
    ) != None

  def delete_player(self, id):
    if not self.has_player(id):
      mudlog.error(f"Trying to delete non-existent player with id {pc.player_id}.")
      return

    self._handler.delete_records(database.PLAYER_TABLE,
      id=id
    )

  def num_players(self):
    return self._handler.num_records(database.PLAYER_TABLE)

  def save_zone(self, zone):
    if self.has_zone(zone.id):
      self.delete_zone(zone.id)

    self._handler.insert_record(database.ZONE_TABLE,
      id=zone.id,
      name=zone.name,
      author=zone.author
    )

    for id in zone.list_room_ids():
      self.save_room(zone.room_by_id(id))

    for id in zone.list_npc_ids():
      self.save_npc_proto(zone.npc_by_id(id))

    for id in zone.list_obj_ids():
      self.save_obj_proto(zone.obj_by_id(id))

  def has_zone(self, id):
    return self._handler.get_record(database.ZONE_TABLE,
      id=id) != None

  def delete_zone(self, id):
    if not self.has_zone(id):
      mudlog.error(f"Trying to delete non-existent zone with id {zone.id}.")
      return

    self._handler.delete_records(database.ZONE_TABLE,
      id=id
    )

    self._handler.delete_records(database.WORLD_TABLE,
      zone_id=id
    )

    self._handler.delete_records(database.OBJ_PROTO_TABLE,
      zone_id=id
    )

    self._handler.delete_records(database.NPC_PROTO_TABLE,
      zone_id=id
    )

  def num_zones(self):
    return self._handler.num_records(database.ZONE_TABLE)

  def save_alias(self, zone_id, id, type, alias):
    if self.has_alias(zone_id, id, type, alias):
      self.delete_alias(zone_id, id, type, alias)

    self._handler.insert_record(database.NAMELIST_TABLE,
      zone_id=zone_id,
      id=id,
      type=type,
      alias=alias
    )

  def has_alias(self, zone_id, id, type, alias):
    return self._handler.get_record(database.NAMELIST_TABLE,
      zone_id=zone_id,
      id=id,
      type=type,
      alias=alias
    ) != None

  def delete_alias(self, zone_id, id, type, alias):
    if not self.has_alias(zone_id, id, type, alias):
      mudlog.error(f"Trying to delete non-existant alias {alias} from {type} {id}@{zone_id}.")
      return

    self._handler.delete_records(database.NAMELIST_TABLE,
      zone_id=zone_id,
      id=id,
      type=type,
      alias=alias
    )

  def num_aliases(self):
    return self._handler.num_records(database.NAMELIST_TABLE)

  def show_table(self, name):
    return self._handler.show_table(name)

  def create_tables(self):
    # TODO: for maintainability, add default values, for example
    # when mana gets added, none of the currently saved characters
    # will have any mana.  I could give them all 50 mana by default
    #
    #            ("max_mp",    int,     50),

    self._handler.verify_columns(database.EXIT_TABLE,
      ("direction", int),
      ("o_zone_id", str),
      ("o_id", str),
      ("d_zone_id", str),
      ("d_id", str)
    )

    # also, could add support for primary key indicators here
    #
    #                ("id",    int),
    #                ("field", str),
    #                ("value", int),
    #                primary=("id", "field")

    self._handler.verify_columns(database.PREF_NUMERIC_TABLE,
      ("id", int),
      ("field", str),
      ("value", int)
    )

    self._handler.verify_columns(database.PREF_TEXT_TABLE,
      ("id", int),
      ("field", str),
      ("value", str)
    )

    self._handler.verify_columns(database.PREF_FLAG_TABLE,
      ("id", int),
      ("field", str),
      ("value", int)
    )

    self._handler.verify_columns(database.NPC_PROTO_TABLE,
      ("zone_id", str),
      ("id", str),
      ("name", str),
      ("ldesc", str),
      ("desc", str)
    )

    self._handler.verify_columns(database.OBJ_PROTO_TABLE,
      ("zone_id", str),
      ("id", str),
      ("name", str),
      ("ldesc", str),
      ("desc", str)
    )

    self._handler.verify_columns(database.WORLD_TABLE,
      ("zone_id", str),
      ("id", str),
      ("name", str),
      ("desc", str)
    )

    self._handler.verify_columns(database.PLAYER_TABLE,
      ("id", int),
      ("name", str),
      ("password", str)
    )

    self._handler.verify_columns(database.ZONE_TABLE,
      ("id", str),
      ("name", str),
      ("author", str)
    )

    self._handler.verify_columns(database.NAMELIST_TABLE,
      ("zone_id", str),
      ("id", str),
      ("type", str),
      ("alias", str)
    )

    # copyover_table