# python modules
import socket
import unittest

# local modules
import character_data
import config
import database
import descriptor_data
import event_data
import game_data
import npc_proto_data
import obj_proto_data
import pc_data
import room_data
import select
import test_utilities
import unique_id_data
import zone_data

class TestGameData(unittest.TestCase):
  def test_event_management(self):
    mud = game_data.game_data()

    event1 = event_data.event_data(None, None, 1)
    event2 = event_data.event_data(None, None, 1)

    mud.add_event(event1)

    self.assertIn(event1, mud.list_events())
    self.assertEqual(mud.num_events(), 1)

    mud.add_event(event2)

    self.assertIn(event1, mud.list_events())
    self.assertIn(event2, mud.list_events())
    self.assertEqual(mud.num_events(), 2)

    mud.cancel_event(event1)

    self.assertNotIn(event1, mud.list_events())
    self.assertIn(event2, mud.list_events())
    self.assertEqual(mud.num_events(), 1)

    mud.cancel_event(event2)

    self.assertNotIn(event1, mud.list_events())
    self.assertNotIn(event2, mud.list_events())
    self.assertEqual(mud.num_events(), 0)

  def test_zone_management(self):
    mud = game_data.game_data()

    zone1 = zone_data.zone_data()
    zone1.name = "the newbie zone"
    zone1.id = "newbie_zone"
    zone1.author = "bob"

    zone2 = zone_data.zone_data()
    zone2.name = "the veteran zone"
    zone2.id = "veteran_zone"
    zone2.author = "alice"

    zone3 = zone_data.zone_data()
    zone3.name = "the problem zone"
    zone3.id = "veteran_zone"
    zone3.author = "greg"

    mud.add_zone(zone1)
    mud.add_zone(zone2)

    # should fire an error and take no action
    mud.add_zone(zone3)

    # only zones 1 and 2 were added
    self.assertIn(zone1, mud.list_zones())
    self.assertIn(zone2, mud.list_zones())
    self.assertNotIn(zone3, mud.list_zones())
    self.assertEqual(mud.num_zones(), 2)

    # retrieve zones by their ID's
    self.assertEqual(mud.zone_by_id("newbie_zone"), zone1)
    self.assertEqual(mud.zone_by_id("veteran_zone"), zone2)

    # typed the ID wrong
    self.assertIsNone(mud.zone_by_id("veretan_zone"))

    # delete zone 1
    mud.delete_zone(zone1)

    # should fire error
    mud.delete_zone(zone1)

    # only zone 2 remains
    self.assertNotIn(zone1, mud.list_zones())
    self.assertIn(zone2, mud.list_zones())
    self.assertEqual(mud.num_zones(), 1)

    # delete zone 2 by looking it up by ID instead
    mud.delete_zone(mud.zone_by_id("veteran_zone"))

    # no zones remain
    self.assertNotIn(zone2, mud.list_zones())
    self.assertEqual(mud.num_zones(), 0)

  def test_object_management(self):
    # build some test zones
    zone1 = zone_data.zone_data()
    zone1.name = "the newbie zone"
    zone1.id = "newbie_zone"
    zone1.author = "bob"

    zone2 = zone_data.zone_data()
    zone2.name = "the veteran zone"
    zone2.id = "veteran_zone"
    zone2.author = "alice"

    # build some test objects for zone 1
    obj1 = obj_proto_data.obj_proto_data()
    obj1.name = "a sharp knife"
    obj1.remove_all_aliases()
    obj1.add_alias("sharp")
    obj1.add_alias("knife")
    obj1.ldesc = "A sharp knife has been stuck into the ground here."
    obj1.desc = "This knife looks extra sharp -- be careful!"
    obj1.id = "sharp_knife"
    obj1.zone_id = "newbie_zone"

    obj2 = obj_proto_data.obj_proto_data()
    obj2.name = "a dull knife"
    obj2.remove_all_aliases()
    obj2.add_alias("dull")
    obj2.add_alias("knife")
    obj2.ldesc = "A dull knife has been stuck into the ground here."
    obj2.desc = "This knife looks extra dull -- relax!"
    obj2.id = "dull_knife"
    obj2.zone_id = "newbie_zone"

    # build some test objects for zone 2
    obj3 = obj_proto_data.obj_proto_data()
    obj3.name = "a bouncy ball"
    obj3.remove_all_aliases()
    obj3.add_alias("bouncy")
    obj3.add_alias("ball")
    obj3.ldesc = "A ball bounces on the ground here."
    obj3.desc = "This knife looks extra bouncy!"
    obj3.id = "bouncy_ball"
    obj3.zone_id = "veteran_zone"

    obj4 = obj_proto_data.obj_proto_data()
    obj4.name = "a cannon ball"
    obj4.remove_all_aliases()
    obj4.add_alias("cannon")
    obj4.add_alias("ball")
    obj4.ldesc = "A cannon ball rests on the ground here."
    obj4.desc = "This ball looks very heavy!"
    obj4.id = "cannon_ball"
    obj4.zone_id = "veteran_zone"

    # add the objects to the zones
    zone1.add_obj(obj1)
    zone1.add_obj(obj2)
    zone2.add_obj(obj3)
    zone2.add_obj(obj4)

    # now put all of this into a game object
    mud = game_data.game_data()
    mud.add_zone(zone1)
    mud.add_zone(zone2)

    # look up objects by their IDs
    self.assertEqual(mud.obj_by_uid("newbie_zone", "sharp_knife"), obj1)
    self.assertEqual(mud.obj_by_uid("newbie_zone", "dull_knife"), obj2)
    self.assertEqual(mud.obj_by_uid("veteran_zone", "bouncy_ball"), obj3)
    self.assertEqual(mud.obj_by_uid("veteran_zone", "cannon_ball"), obj4)

    # look for object in the wrong zone
    self.assertIsNone(mud.obj_by_uid("veteran_zone", "sharp_knife"))

  def test_npc_management(self):
    # build some test zones
    zone1 = zone_data.zone_data()
    zone1.name = "the newbie zone"
    zone1.id = "newbie_zone"

    zone2 = zone_data.zone_data()
    zone2.name = "the veteran zone"
    zone2.id = "veteran_zone"

    # build some npcs for zone 1
    npc1 = npc_proto_data.npc_proto_data()
    npc1.zone_id = "newbie_zone"
    npc1.id = "wild_dog"

    npc2 = npc_proto_data.npc_proto_data()
    npc2.zone_id = "newbie_zone"
    npc2.id = "tame_dog"

    # build some npcs for zone 2
    npc3 = npc_proto_data.npc_proto_data()
    npc3.zone_id = "veteran_zone"
    npc3.id = "wild_man"

    npc4 = npc_proto_data.npc_proto_data()
    npc4.zone_id = "veteran_zone"
    npc4.id = "tame_man"

    # add npcs to zones
    zone1.add_npc(npc1)
    zone1.add_npc(npc2)
    zone2.add_npc(npc3)
    zone2.add_npc(npc4)

    # now put all of this into a game object
    mud = game_data.game_data()
    mud.add_zone(zone1)
    mud.add_zone(zone2)

    # look up npcs by their IDs
    self.assertEqual(mud.npc_by_uid("newbie_zone", "wild_dog"), npc1)
    self.assertEqual(mud.npc_by_uid("newbie_zone", "tame_dog"), npc2)
    self.assertEqual(mud.npc_by_uid("veteran_zone", "wild_man"), npc3)
    self.assertEqual(mud.npc_by_uid("veteran_zone", "tame_man"), npc4)

    # look for npcs in the wrong zone
    self.assertIsNone(mud.npc_by_uid("veteran_zone", "wild_dog"))

  def test_room_management(self):
    # build a test zone
    zone1 = zone_data.zone_data()
    zone2 = zone_data.zone_data()
    zone1.id = "zone1"
    zone2.id = "zone2"

    # build some rooms
    rm1 = room_data.room_data()
    rm1.id = "cold_hallway"
    rm1.zone_id = "zone1"
    rm2 = room_data.room_data()
    rm2.id = "warm_hallway"
    rm2.zone_id = "zone2"

    # add rooms to zones
    zone1.add_room(rm1)
    zone2.add_room(rm2)

    # put the zones in a game object
    mud = game_data.game_data()
    mud.add_zone(zone1)
    mud.add_zone(zone2)

    # look them up
    self.assertEqual(mud.room_by_uid("zone1", "cold_hallway"), rm1)
    self.assertEqual(mud.room_by_uid("zone2", "warm_hallway"), rm2)

    # should fire an error
    self.assertIsNone(mud.room_by_uid("zone2", "cold_hallway"))

  def test_character_management(self):
    mud, zone, room = test_utilities.create_single_room_test_world()
    char = character_data.character_data()

    # have game add character to specific room
    mud.add_character_to_room(char, room)

    # make sure they went into the game
    self.assertTrue(mud.has_character(char))

    # make sure they went into the room
    self.assertIn(char, room.people)

    uid = unique_id_data.unique_id_data(room.zone_id, room.id)
  
    # make sure their room field was set accordingly
    self.assertEqual(char.room, uid)

    # now remove the player from the mud
    mud.extract_character(char)

    # make sure it's been removed from the room
    self.assertNotIn(char, room.people)

    # make sure it's been removed from the game
    self.assertFalse(mud.has_character(char))


  def test_object_management(self):
    mud, zone, room = test_utilities.create_single_room_test_world()
    obj = test_utilities.create_test_object()

    # have game add object to specific room
    mud.add_obj_to_room(obj, room)

    # make sure it went into the room
    self.assertIn(obj, room.contents)

    # and the game
    self.assertIn(obj, mud.list_objects())

    # make sure its room field was set accordingly
    self.assertEqual(obj.room, unique_id_data.unique_id_data(room.zone_id, room.id))

    # now remove object from the mud
    mud.extract_obj(obj)

    # it should be nowhere
    self.assertIsNone(obj.room)

    # definitely not in the room
    self.assertNotIn(obj, room.contents)

    # or even the game
    self.assertNotIn(obj, mud.list_objects())

  def test_load_world(self):
    mud = game_data.game_data()
    db = database.database()

    db.load_stock()
    mud.load_world(db)
    mud.assign_spec_procs()

  def test_echo_around(self):
    clients, players, mud, zone, room = test_utilities.create_single_room_test_world_and_players(3)
    bob, alice, sam = players
    bob_socket, alice_socket, sam_socket = clients

    # they'll be in the same room
    mud.add_character_to_room(bob, room)
    mud.add_character_to_room(alice, room)
    mud.add_character_to_room(sam, room)

    # now test the echo_around
    mud.echo_around(sam, list(), "Hello world!")

    # flush the output
    alice.descriptor.flush_output()
    bob.descriptor.flush_output()

    # make sure it was received
    self.assertEqual(alice_socket.recv(1024).decode("utf-8"), "Hello world!")
    self.assertEqual(bob_socket.recv(1024).decode("utf-8"), "Hello world!")

    # sam should have no data pending
    rlist, wlist, xlist = select.select([sam_socket], [], [], 1)
    self.assertNotIn(sam_socket, rlist)

    for client in clients:
      client.close()
    for player in players:
      player.descriptor.close()

if __name__ == "__main__":
  unittest.main()