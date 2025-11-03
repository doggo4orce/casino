import unittest
import npc_proto_data
import obj_proto_data
import room_data
import zone_data

class TestZoneData(unittest.TestCase):
  def test_zone_data(self):
    zone = zone_data.zone_data()

    zone.name = "the newbie zone"
    zone.id = "newbie_zone"
    zone.author = "Smart Dude"

    self.assertTrue(zone.name, "the newbie zone")
    self.assertTrue(zone.id, "newbie_zone")
    self.assertTrue(zone.author, "Smart Dude")

    rm1 = room_data.room_data()
    rm2 = room_data.room_data()

    rm1.name = "A Long Dark Hallway"
    rm1.desc = "<p>It is cold, dark, and damp, and miserable.</p>"
    rm1.id = "cold_hallway"
    rm1.zone_id = "newbie_zone"

    rm2.name = "A Short Fat Hallway"
    rm2.desc = "<p>It is cold, dark, and damp, and miserable.</p>"
    rm2.id = "warm_hallway"
    rm2.zone_id = "newbie_zone"

    obj_p1 = obj_proto_data.obj_proto_data()
    obj_p2 = obj_proto_data.obj_proto_data()

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

    npc_p1 = npc_proto_data.npc_proto_data()
    npc_p2 = npc_proto_data.npc_proto_data()

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

    zone.add_obj(obj_p1)
    zone.add_obj(obj_p2)
    zone.add_npc(npc_p1)
    zone.add_npc(npc_p2)
    zone.add_room(rm1)
    zone.add_room(rm2)

    self.assertEqual(zone.num_rooms(), 2)
    self.assertEqual(zone.num_npcs(), 2)
    self.assertEqual(zone.num_objs(), 2)

    print(zone.debug())

    self.assertIs(zone.room_by_id('cold_hallway'), rm1)
    self.assertIs(zone.room_by_id('warm_hallway'), rm2)

    self.assertIs(zone.obj_by_id('new_object'), obj_p1)
    self.assertIs(zone.obj_by_id('old_object'), obj_p2)

    self.assertIs(zone.npc_by_id('happy_npc'), npc_p1)
    self.assertIs(zone.npc_by_id('sad_npc'), npc_p2)

    self.assertTrue(zone.has_room('cold_hallway'))
    self.assertTrue(zone.has_obj('new_object'))
    self.assertTrue(zone.has_npc('happy_npc'))

    zone.delete_obj('new_object')
    self.assertFalse(zone.has_obj('new_object'))
    self.assertEqual(zone.num_objs(), 1)

    zone.delete_room('cold_hallway')
    self.assertFalse(zone.has_room('cold_hallway'))
    self.assertEqual(zone.num_rooms(), 1)

    zone.delete_npc('happy_npc')
    self.assertFalse(zone.has_npc('happy_npc'))
    self.assertEqual(zone.num_npcs(), 1)

if __name__ == "__main__":
  unittest.main()