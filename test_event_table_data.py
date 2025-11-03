import event_data
import event_table_data
import database
import game_data
import npc_data
import unittest

class TestEventTableData(unittest.TestCase):
  def test_short_events(self):
    table = event_table_data.event_table_data()

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

    event1 = event_data.event_data(npc, event_func1, 4)
    event2 = event_data.event_data(npc, event_func2, 5)
    event3 = event_data.event_data(npc, event_func3, 6)

    table.add_event(event1)
    table.add_event(event2)
    table.add_event(event3)

    print(table.debug())

    table.heartbeat(mud, db)
    table.heartbeat(mud, db)
    table.heartbeat(mud, db)
    table.heartbeat(mud, db)

    self.assertEqual(npc.name, "first name")

    table.heartbeat(mud, db)

    self.assertEqual(npc.name, "second name")

    table.heartbeat(mud, db)

    self.assertEqual(npc.name, "third name")

  def test_long_event(self):
    table = event_table_data.event_table_data()

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

    event1 = event_data.event_data(npc, event_func1, 1353)
    event2 = event_data.event_data(npc, event_func2, 1354)
    event3 = event_data.event_data(npc, event_func3, 1355)

    table.add_event(event1)
    table.add_event(event2)
    table.add_event(event3)

    self.assertEqual(table.num_events(), 3)

    for j in range(0,1352):
      table.heartbeat(mud, db)

    self.assertEqual(npc.name, "the baker")


    # event 1 fires
    table.heartbeat(mud, db)

    self.assertEqual(npc.name, "first name")
    self.assertEqual(table.num_events(), 2)

    table.cancel_event(event3)

    self.assertEqual(table.num_events(), 1)

    # event 2 fires
    table.heartbeat(mud, db)

    self.assertEqual(table.num_events(), 0)

    self.assertEqual(npc.name, "second name")

    # had we not cancelled event 3, it would fire
    table.heartbeat(mud, db)

    self.assertEqual(npc.name, "second name")

if __name__ == "__main__":
  unittest.main()