import character_data
import event_data
import npc_data
import unittest
import unique_id_data

class TestEventData(unittest.TestCase):
  def test_event_data(self):

    npc = npc_data.npc_data()
    npc.zone_id = "midgaard"
    npc.id = "baker"
    npc.name = "the baker"

    uid = unique_id_data.unique_id_data()
    uid.zone_id = "wef"
    uid.id = "weffer"

    target1 = character_data.character_data()
    target1.name = "bob"
    target2 = character_data.character_data()
    target2.name = "alice"

    def event_func(ch, mud, db):
      print("event function parameters")
      print(f"ch: {ch}\nmud: {mud}\ndb: {db}")

    event = event_data.event_data(npc, event_func, 3)
    event.add_target(target1)
    event.add_target(target2)

    self.assertEqual(event.countdown, 3)
    event.heartbeat()
    self.assertEqual(event.countdown, 2)
    event.heartbeat()
    self.assertEqual(event.countdown, 1)
    event.heartbeat()
    self.assertEqual(event.countdown, 0)
    self.assertTrue(event.pending())

    event.execute("uossmud", "sql")

    print(event.debug())

if __name__ == "__main__":
  unittest.main()