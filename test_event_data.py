import character_data
import database
import event_data
import game_data
import npc_data
import pc_data
import unittest
import unique_id_data

class TestEventData(unittest.TestCase):
  def test_targets1(self):
    npc = npc_data.npc_data()
    npc.zone_id = "midgaard"
    npc.id = "baker"
    npc.name = "the baker"

    pc = pc_data.pc_data()
    pc.name = "Bob"
    pc.reset_aliases("bob", "man")
    pc.ldesc = "Bob is standing here."
    pc.desc = "He looks handsome as usual."
    pc.password = "p@ssw0rd"
    pc.player_id = 1
    pc.title = "the great guy"

    char = character_data.character_data()
    char.name = "alice"
    char.desc = "<p>This is Alice.</p>"
    char.ldesc = "Alice is standing around."
    char.room = unique_id_data.unique_id_data("stockville", "casino")
    char.reset_aliases("alice", "woman")

    event = event_data.event_data(npc, None, 0)

    self.assertFalse(event.has_targets())

    event.add_target(npc)

    self.assertTrue(event.has_targets())

    event.add_target(pc)
    event.add_target(char)

    print(event.debug())

    self.assertIn(npc, event.targets())
    self.assertIn(pc, event.targets())
    self.assertIn(char, event.targets())

    self.assertEqual(event.target_names(), ["the baker", "Bob", "alice"])

    event.remove_target(npc)

    self.assertNotIn(npc, event.targets())
    self.assertIn(pc, event.targets())
    self.assertIn(char, event.targets())

    event.remove_target(pc)

    self.assertNotIn(npc, event.targets())
    self.assertNotIn(pc, event.targets())
    self.assertIn(char, event.targets())

    event.remove_target(char)

    self.assertNotIn(npc, event.targets())
    self.assertNotIn(pc, event.targets())
    self.assertNotIn(char, event.targets())

    self.assertFalse(event.has_targets())

  def test_event_heartbeat_pending(self):

    event = event_data.event_data(None, None, 3)

    self.assertEqual(event.countdown, 3)
    event.heartbeat()
    self.assertEqual(event.countdown, 2)
    event.heartbeat()
    self.assertEqual(event.countdown, 1)
    event.heartbeat()
    self.assertEqual(event.countdown, 0)

    self.assertTrue(event.pending())


  def test_execute(self):
    npc = npc_data.npc_data()
    npc.zone_id = "midgaard"
    npc.id = "baker"
    npc.name = "the baker"

    mud = game_data.game_data()
    db = database.database()
    
    def event_func(ch, mud, db, targets):
      ch.name = "the brewer"

    event = event_data.event_data(npc, event_func, 1)

    event.execute(mud, db)

    self.assertEqual(npc.name, "the brewer")


if __name__ == "__main__":
  unittest.main()