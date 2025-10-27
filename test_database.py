import database
import exit_data
import pc_data
import namelist_data
import npc_proto_data
import obj_proto_data
import pref_data
import room_data
import unittest
import zone_data

class TestDatabase(unittest.TestCase):
  def test_aliases(self):
    db = database.database(":memory:")
    db.connect()
    db.create_tables()

    db.save_alias("goblin_cave", "small_goblin", "npc", "goblin")
    db.save_alias("goblin_cave", "small_goblin", "npc", "small")

    # print("Namelists Table  -=-")
    # print(db.show_table(database.database.NAMELIST_TABLE))
    # print("-=-=-=-=-=-=-=-=-=-=")

    self.assertTrue(db.has_alias("goblin_cave", "small_goblin", "npc", "goblin"))
    self.assertTrue(db.has_alias("goblin_cave", "small_goblin", "npc", "small"))
    self.assertEqual(db.num_aliases(), 2)

    db.delete_alias("goblin_cave", "small_goblin", "npc", "small")

    self.assertTrue(db.has_alias("goblin_cave", "small_goblin", "npc", "goblin"))
    self.assertFalse(db.has_alias("goblin_cave", "small_goblin", "npc", "small"))
    self.assertEqual(db.num_aliases(), 1)

  def test_exits(self):
    db = database.database(":memory:")
    db.connect()
    db.create_tables()

    ex = exit_data.exit_data(exit_data.direction.NORTH, "cave", "hallway1")
    ex2 = exit_data.exit_data(exit_data.direction.EAST, "cave", "hallway2")
    ex3 = exit_data.exit_data(exit_data.direction.NORTH, "cave", "hallway3")
    db.save_exit("casino", "foyer", ex)
    db.save_exit("casino", "foyer", ex2)
    db.save_exit("casino", "foyer", ex3)

    self.assertTrue(db.has_exit("casino", "foyer", exit_data.direction.NORTH))
    self.assertTrue(db.has_exit("casino", "foyer", exit_data.direction.EAST))
    self.assertTrue(db._handler.num_records(database.database.EXIT_TABLE), 2)
    # print("Exit Table  -=-=-=-=")
    # print(db.show_table(database.database.EXIT_TABLE))
    # print("-=-=-=-=-=-=-=-=-=-=")
    self.assertEqual(db.num_exits(), 2)

    db.delete_exit("casino", "foyer", exit_data.direction.NORTH)
    
    self.assertEqual(db.num_exits(), 1)

    db.close()

  def test_numeric_preferences(self):
    db = database.database(":memory:")
    db.connect()
    db.create_tables()

    pdn = pref_data.pref_data_numeric()
    pdn.screen_width = 4
    pdn.screen_length = 12

    pc = pc_data.pc_data()
    pc.player_id = 11

    db.save_all_prefs_numeric(pc)

    self.assertTrue(db.has_pref_numeric(pc.player_id, 'screen_length'))
    self.assertTrue(db.has_pref_numeric(pc.player_id, 'screen_width'))
    self.assertEqual(db.num_prefs_numeric(), 2)

    db.delete_pref_numeric(pc.player_id, 'screen_length')
    self.assertFalse(db.has_pref_numeric(pc.player_id, 'screen_length'))
    self.assertTrue(db.has_pref_numeric(pc.player_id, 'screen_width'))
    self.assertEqual(db.num_prefs_numeric(), 1)

    db.save_pref_numeric(pc, 'screen_width', 19)

    # print("Pref Numeric -=-=-=-")
    # print(db.show_table(database.database.PREF_NUMERIC_TABLE))
    # print("-=-=-=-=-=-=-=-=-=-=")

    self.assertTrue(db.has_pref_numeric(pc.player_id, 'screen_width'))
    self.assertEqual(db.num_prefs_numeric(), 1)

    db.close()

  def test_text_preferences(self):
    db = database.database(":memory:")
    db.connect()
    db.create_tables()

    pc1 = pc_data.pc_data()
    pc1.player_id = 11

    pc2 = pc_data.pc_data()
    pc2.player_id = 44

    pc1.preferences.set('color_mode', 'full_color')
    pc1.preferences.set('title', 'has a fancy title')

    pdn2 = pc2.preferences
    pdn2.set('color_mode', 'completely_off')
    pdn2.set('title', 'has a silly title')

    db.save_all_prefs_text(pc1)
    db.save_all_prefs_text(pc2)

    self.assertTrue(db.has_pref_text(pc1.player_id, 'color_mode'))
    self.assertTrue(db.has_pref_text(pc1.player_id, 'title'))
    self.assertTrue(db.has_pref_text(pc2.player_id, 'color_mode'))
    self.assertTrue(db.has_pref_text(pc2.player_id, 'title'))

    # print("Pref Text    -=-=-=-")
    # print(db.show_table(database.database.PREF_TEXT_TABLE))
    # print("-=-=-=-=-=-=-=-=-=-=")

    db.delete_pref_text(pc1.player_id, 'color_mode')
    self.assertFalse(db.has_pref_text(pc1.player_id, 'color_mode'))
    self.assertTrue(db.has_pref_text(pc1.player_id, 'title'))
    self.assertTrue(db.has_pref_text(pc2.player_id, 'color_mode'))
    self.assertTrue(db.has_pref_text(pc2.player_id, 'title'))
    self.assertEqual(db.num_prefs_text(), 3)

    db.close()

  def test_flag_preferences(self):
    db = database.database(":memory:")
    db.connect()
    db.create_tables()

    pc1 = pc_data.pc_data()
    pc1.player_id = 11

    pc2 = pc_data.pc_data()
    pc2.player_id = 44

    pc1.preferences.set('active_idle', True)
    pc1.preferences.set('brief_mode', True)
    pc2.preferences.set('debug_mode', True)

    db.save_all_prefs_flag(pc1)
    db.save_all_prefs_flag(pc2)

    db.delete_pref_flag(pc1.player_id, 'active_idle')
    db.delete_pref_flag(pc2.player_id, 'brief_mode')

    self.assertFalse(db.has_pref_flag(pc1.player_id, 'active_idle'))
    self.assertTrue(db.has_pref_flag(pc1.player_id, 'brief_mode'))
    self.assertTrue(db.has_pref_flag(pc1.player_id, 'debug_mode'))
    self.assertTrue(db.has_pref_flag(pc2.player_id, 'active_idle'))
    self.assertFalse(db.has_pref_flag(pc2.player_id, 'brief_mode'))
    self.assertTrue(db.has_pref_flag(pc2.player_id, 'debug_mode'))

    # print("Pref Flags   -=-=-=-")
    # print(db.show_table(database.database.PREF_FLAG_TABLE))
    # print("-=-=-=-=-=-=-=-=-=-=")
    db.close()

  def test_npc_proto(self):
    db = database.database(":memory:")
    db.connect()
    db.create_tables()

    npc_p1 = npc_proto_data.npc_proto_data()
    npc_p1.id = 'happy_npc'
    npc_p1.zone_id = 'nice_zone'
    npc_p1.name = "a happy npc"
    npc_p1.reset_aliases("happy", "npc")
    npc_p1.ldesc = "a happy npc wanders here"
    npc_p1.desc = "it looks happy"

    npc_p2 = npc_proto_data.npc_proto_data()
    npc_p2.id = 'angry_npc'
    npc_p2.zone_id = 'bad_zone'
    npc_p2.name = "an angry npc"
    npc_p2.reset_aliases("angry", "npc")
    npc_p2.ldesc = "an angry npc wanders here"
    npc_p2.desc = "it looks angry"

    db.save_npc_proto(npc_p1)    
    db.save_npc_proto(npc_p2)

    # print("NPC -= Proto -=-=-=-")
    # print(db.show_table(database.database.NPC_PROTO_TABLE))
    # print(db.show_table(database.database.NAMELIST_TABLE))
    # print("-=-=-=-=-=-=-=-=-=-=")

    self.assertTrue(db.has_npc_proto("nice_zone", "happy_npc"))
    self.assertTrue(db.has_npc_proto("bad_zone", "angry_npc"))

    db.delete_npc_proto("nice_zone", "happy_npc")
    self.assertFalse(db.has_npc_proto("nice_zone", "happy_npc"))
    self.assertTrue(db.has_npc_proto("bad_zone", "angry_npc"))

    db.close()

  def test_obj_proto(self):
    db = database.database(":memory:")
    db.connect()
    db.create_tables()

    obj_p1 = obj_proto_data.obj_proto_data()
    obj_p1.id = 'nice_dagger'
    obj_p1.zone_id = 'nice_zone'
    obj_p1.name = "a nice dagger"
    obj_p1.reset_aliases("nice", "dagger")
    obj_p1.ldesc = "A nice dagger has been nicely left here."
    obj_p1.desc = "It looks nice."

    obj_p2 = obj_proto_data.obj_proto_data()
    obj_p2.id = 'ugly_rock'
    obj_p2.zone_id = 'bad_zone'
    obj_p2.name = "an ugly rock"
    obj_p2.reset_aliases("ugly", "rock")
    obj_p2.ldesc = "An ugly rock has been dropped here."
    obj_p2.desc = "It looks ugly."

    db.save_obj_proto(obj_p1)
    db.save_obj_proto(obj_p2)

    # print("Object Proto -=-=-=-")
    # print(db.show_table(database.database.OBJ_PROTO_TABLE))
    # print(db.show_table(database.database.NAMELIST_TABLE))
    # print("-=-=-=-=-=-=-=-=-=-=")

    db.close()

  def test_room(self):
    db = database.database(":memory:")
    db.connect()
    db.create_tables()

    rm1 = room_data.room_data()
    rm1.name = "A Long Dark Hallway"
    rm1.desc = "<p>It is cold, dark, and damp, and miserable.</p>"
    rm1.id = "cold_hallway"
    rm1.zone_id = "newbie_zone"
    rm1.connect(exit_data.direction.EAST, "newbie_zone", "warm_hallway")
    rm1.connect(exit_data.direction.WEST, "stockville", "casino")

    rm2 = room_data.room_data()
    rm2.name = "A Short Bright Hallway"
    rm2.desc = "<p>It is warm, bright, and cheerful.</p>"
    rm2.id = "warm_hallway"
    rm2.zone_id = "newbie_zone"
    rm2.connect(exit_data.direction.WEST, "newbie_zone", "cold_hallway")
    rm2.connect(exit_data.direction.NORTH, "stockville", "casino")
    
    db.save_room(rm1)
    db.save_room(rm2)

    # print("Room   -=-=-=-=-=-=-")
    # print(db.show_table(database.database.WORLD_TABLE))
    # print("-=-=-=--=-=-=-=-=-=-")
    # print("Exits  -=-=-=-=-=-=-")
    # print(db.show_table(database.database.EXIT_TABLE))
    # print("-=-=-=-=-=-=-=-=-=-=")

    self.assertTrue(db.has_room('newbie_zone', 'cold_hallway'))
    self.assertTrue(db.has_room('newbie_zone', 'warm_hallway'))
    self.assertFalse(db.has_exit(rm1.zone_id, rm1.id, exit_data.direction.SOUTH))
    self.assertTrue(db.has_exit(rm1.zone_id, rm1.id, exit_data.direction.EAST))
    self.assertTrue(db.has_exit(rm1.zone_id, rm1.id, exit_data.direction.WEST))
    self.assertFalse(db.has_exit(rm1.zone_id, rm1.id, exit_data.direction.SOUTH))
    self.assertTrue(db.has_exit(rm2.zone_id, rm2.id, exit_data.direction.WEST))
    self.assertTrue(db.has_exit(rm2.zone_id, rm2.id, exit_data.direction.NORTH))

    db.delete_room(rm2.zone_id, rm2.id)

    self.assertTrue(db.has_room('newbie_zone', 'cold_hallway'))
    self.assertFalse(db.has_room('newbie_zone', 'warm_hallway'))
    self.assertTrue(db.has_exit(rm1.zone_id, rm1.id, exit_data.direction.EAST))
    self.assertTrue(db.has_exit(rm1.zone_id, rm1.id, exit_data.direction.WEST))
    self.assertFalse(db.has_exit(rm2.zone_id, rm2.id, exit_data.direction.WEST))
    self.assertFalse(db.has_exit(rm2.zone_id, rm2.id, exit_data.direction.NORTH))

    db.close()

  def test_players(self):
    db = database.database(":memory:")
    db.connect()
    db.create_tables()

    pc1 = pc_data.pc_data()
    pc2 = pc_data.pc_data()

    pc1.player_id = 13
    pc1.name = "george"
    pc1.password = 'cur10us'

    pc2.player_id = 14
    pc2.name = "roobiki"
    pc2.password = 'abbey'

    db.save_player(pc1)
    db.save_player(pc2)

    self.assertEqual(db.num_players(), 2)

    self.assertTrue(db.has_player(13))
    self.assertTrue(db.has_player(14))
    self.assertFalse(db.has_player(15))


    # print("Players  -=-=-=-=-=-")
    # print(db.show_table(database.database.PLAYER_TABLE))
    # print("-=-=-=--=-=-=-=-=-=-")

    db.delete_player(13)
    self.assertEqual(db.num_players(), 1)
    self.assertFalse(db.has_player(13))

    db.close()  

  def test_zones(self):
    db = database.database(":memory:")
    db.connect()
    db.create_tables()

    # NEWBIE ZONE
    rm1 = room_data.room_data()
    rm2 = room_data.room_data()
    obj_p1 = obj_proto_data.obj_proto_data()
    obj_p2 = obj_proto_data.obj_proto_data()
    npc_p1 = npc_proto_data.npc_proto_data()
    npc_p2 = npc_proto_data.npc_proto_data()

    rm1.name = "A Long Dark Hallway"
    rm1.desc = "<p>It is cold, dark, and damp, and miserable.</p>"
    rm1.id = "cold_hallway"
    rm1.zone_id = "newbie_zone"

    rm2.name = "A Short Fat Hallway"
    rm2.desc = "<p>It is cold, dark, and damp, and miserable.</p>"
    rm2.id = "warm_hallway"
    rm2.zone_id = "newbie_zone"

    npc_p1.id = 'happy_npc'
    npc_p1.zone_id = 'newbie_zone'
    npc_p1.name = "a happy npc"
    npc_p1.remove_all_aliases()
    npc_p1.add_alias("happy")
    npc_p1.add_alias("npc")
    npc_p1.ldesc = "a happy npc wanders here"
    npc_p1.desc = "it looks happy"

    npc_p2.id = 'sad_npc'
    npc_p2.zone_id = 'newbie_zone'
    npc_p2.name = "a sad npc"
    npc_p2.remove_all_aliases()
    npc_p2.add_alias("sad")
    npc_p2.add_alias("npc")
    npc_p2.ldesc = "a sad npc wanders here"
    npc_p2.desc = "it looks sad"

    obj_p1.name = "a new object"
    obj_p1.remove_all_aliases()
    obj_p1.add_alias("new")
    obj_p1.add_alias("object")
    obj_p1.ldesc = "a new object sits here"
    obj_p1.desc = "it looks new"
    obj_p1.id = "new_object"
    obj_p1.zone_id = "newbie_zone"

    obj_p2.name = "an old object"
    obj_p2.remove_all_aliases()
    obj_p2.add_alias("old")
    obj_p2.add_alias("object")
    obj_p2.ldesc = "an old object sits here"
    obj_p2.desc = "it looks old"
    obj_p2.id = "old_object"
    obj_p2.zone_id = "newbie_zone"

    zone1 = zone_data.zone_data()
    zone1.name = "the newbie zone"
    zone1.id = "newbie_zone"
    zone1.author = "Smart Dude"
    zone1.add_room(rm1)
    zone1.add_room(rm2)
    zone1.add_npc(npc_p1)
    zone1.add_npc(npc_p2)
    zone1.add_obj(obj_p1)
    zone1.add_obj(obj_p2)

    self.assertEqual(zone1.num_rooms(), 2)
    self.assertEqual(zone1.num_npcs(), 2)
    self.assertEqual(zone1.num_objs(), 2)

    db.save_zone(zone1)

    # MIDGAR
    zone2 = zone_data.zone_data()
    zone2.name = "The City of Midgaard"
    zone2.author ="diku"
    zone2.id = 'midgaard'

    rm1.zone_id = "midgaard"
    rm2.zone_id = "midgaard"
    obj_p1.zone_id = "midgaard"
    obj_p2.zone_id = "midgaard"
    npc_p1.zone_id = "midgaard"
    npc_p2.zone_id = "midgaard"

    # recycle old rooms because we're just checking database entries anyway
    zone2.add_room(rm1)
    zone2.add_room(rm2)
    zone2.add_npc(npc_p1)
    zone2.add_npc(npc_p2)
    zone2.add_obj(obj_p1)
    zone2.add_obj(obj_p2)
    db.save_zone(zone2)

    self.assertEqual(db.num_zones(), 2)
    self.assertEqual(db.num_rooms(), 4)
    self.assertEqual(db.num_obj_protos(), 4)
    self.assertEqual(db.num_npc_protos(), 4)

    # print("Zone1  -=-=-=-=-=-=-")
    # print(db.show_table(database.database.ZONE_TABLE))
    # print(db.show_table(database.database.WORLD_TABLE))
    # print(db.show_table(database.database.OBJ_PROTO_TABLE))
    # print(db.show_table(database.database.NPC_PROTO_TABLE))
    # print("-= after deleting -=")
    db.delete_zone(zone1.id)
    # print(db.show_table(database.database.ZONE_TABLE))
    # print(db.show_table(database.database.WORLD_TABLE))
    # print(db.show_table(database.database.OBJ_PROTO_TABLE))
    # print(db.show_table(database.database.NPC_PROTO_TABLE))

    self.assertEqual(db.num_zones(), 1)
    self.assertEqual(db.num_rooms(), 2)
    self.assertEqual(db.num_obj_protos(), 2)
    self.assertEqual(db.num_npc_protos(), 2)

    db.delete_zone(zone2.id)

    self.assertEqual(db.show_table(database.database.ZONE_TABLE), "")
    self.assertEqual(db.show_table(database.database.WORLD_TABLE), "")
    self.assertEqual(db.show_table(database.database.OBJ_PROTO_TABLE), "")
    self.assertEqual(db.show_table(database.database.NPC_PROTO_TABLE), "")
    # print("-=-=-=-=-=-=-=-=-=-=")

    self.assertEqual(db.num_zones(), 0)
    self.assertEqual(db.num_obj_protos(), 0)
    self.assertEqual(db.num_npc_protos(), 0)

  def test_load_world(self):
    mud = game_data.game_data()
    db = database.database(":memory:")
    db.connect()
    db.create_tables()
    db.load_stock()
    db.load_world(mud)

  def test_load_stock(self):
    db = database.database(":memory:")
    db.connect()
    db.create_tables()
    db.load_stock()

#TODO can't store apostrophes in strings that get saved, this is an issue with db_handler.py im pretty sure
if __name__ == "__main__":
  unittest.main()