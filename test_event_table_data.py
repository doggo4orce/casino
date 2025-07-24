import event_data
import event_table_data
import unittest

class TestEventTableData(unittest.TestCase):
  def test_event_table(self):

    # simplify for testing
    event_table_data.event_table_data.NUM_BUCKETS = 3

    table = event_table_data.event_table_data()

    def event_func1(ch, mud, db):
      print("calling event1 with parameters")
      print(f"ch: {ch}\nmud: {mud}\ndb: {db}")

    def event_func2(ch, mud, db):
      print("calling event2 with parameters")
      print(f"ch: {ch}\nmud: {mud}\ndb: {db}")

    def event_func3(ch, mud, db):
      print("calling event3 with parameters")
      print(f"ch: {ch}\nmud: {mud}\ndb: {db}")

    event1 = event_data.event_data(None, event_func1, 4)
    event2 = event_data.event_data(None, event_func2, 5)
    event3 = event_data.event_data(None, event_func3, 6)

    table.add_event(event1)
    table.add_event(event2)
    table.add_event(event3)

    print(table.debug())

    table.heartbeat("grotto", "sql")
    table.heartbeat("grotto", "sql")
    table.heartbeat("grotto", "sql")
    table.heartbeat("grotto", "sql")
    table.heartbeat("grotto", "sql")
    table.heartbeat("grotto", "sql")

if __name__ == "__main__":
  unittest.main()