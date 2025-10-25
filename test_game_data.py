# python modules
import unittest

# local modules
import event_data
import game_data
import npc_proto_data
import obj_proto_data
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

  def test_entity_management(self):
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


if __name__ == "__main__":
  unittest.main()