import event_bucket_data
import event_data
import unittest

class TestEventBucketData(unittest.TestCase):
  def test_event_bucket(self):

    def event_func1(ch, mud, db):
      print("calling event1 with parameters")
      print(f"ch: {ch}\nmud: {mud}\ndb: {db}")

    def event_func2(ch, mud, db):
      print("calling event2 with parameters")
      print(f"ch: {ch}\nmud: {mud}\ndb: {db}")

    def event_func3(ch, mud, db):
      print("calling event3 with parameters")
      print(f"ch: {ch}\nmud: {mud}\ndb: {db}")

    event1 = event_data.event_data(None, event_func1, 3)
    event2 = event_data.event_data(None, event_func2, 2)
    event3 = event_data.event_data(None, event_func3, 1)

    bucket = event_bucket_data.event_bucket_data()

    bucket.add_event(event1)
    bucket.add_event(event2)
    bucket.add_event(event3)

    self.assertEqual(bucket.num_events(), 3)

    bucket.heartbeat("uoss", "sql")

    print(bucket.debug())

    bucket.heartbeat("uoss", "sql")

    print(bucket.debug())

    bucket.heartbeat("uoss", "sql")

    print(bucket.debug())

    bucket.heartbeat("uoss", "sql")

if __name__ == "__main__":
  unittest.main()