import database
import event_bucket_data
import event_data
import game_data
import npc_data
import unittest

class TestEventBucketData(unittest.TestCase):
  def test_event_bucket(self):

    db = database.database()
    mud = game_data.game_data()

    npc = npc_data.npc_data()
    npc.zone_id = "midgaard"
    npc.id = "baker"
    npc.name = "the baker"

    def event_func1(ch, mud, db, targets):
      ch.name = "first name"

    def event_func2(ch, mud, db, targets):
      ch.name = "second name"

    def event_func3(ch, mud, db, targets):
      ch.name = "third name"

    event1 = event_data.event_data(npc, event_func1, 3)
    event2 = event_data.event_data(npc, event_func2, 2)
    event3 = event_data.event_data(npc, event_func3, 1)

    bucket = event_bucket_data.event_bucket_data()

    bucket.add_event(event1)
    bucket.add_event(event2)
    bucket.add_event(event3)

    self.assertEqual(bucket.num_events(), 3)

    bucket.heartbeat(mud, db)

    print(bucket.list_events())

    #self.assertEqual(npc.name, "third name")

    bucket.heartbeat(mud, db)


    self.assertEqual(npc.name, "second name")

    bucket.heartbeat(mud, db)

    self.assertEqual(npc.name, "first name")

    bucket.heartbeat(mud, db)

if __name__ == "__main__":
  unittest.main()