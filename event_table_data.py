import event_bucket_data

class event_table_data:
  NUM_BUCKETS = 64
  """Creates an event table which manages a list of event buckets
     current_bucket = index next bucket to get a heart beat
     buckets        = list of event_buckets to manage"""

  def __init__(self):
    self._current_bucket = 0
    self._buckets = list()

    for j in range(0, event_table_data.NUM_BUCKETS):
      self._buckets.append(event_bucket_data.event_bucket_data())

  """heartbeat(mud, db)  <- call heartbeat() for all events in current bucket++
     add_event(event)    <- add new event to table
     list_events()       <- returns list of scheduled events
     num_events()        <- counts the number of events in table
     cancel_event(event) <- remove event from table
     num_buckets()       <- number of buckets table is divided into"""

  def heartbeat(self, mud, db):
    self._buckets[self._current_bucket].heartbeat(mud, db)
    self._current_bucket += 1
    self._current_bucket = self._current_bucket % event_table_data.NUM_BUCKETS

  def add_event(self, event):
    # 1 is subtracted from countdown to account for the fact that events will
    # wait for one more heartbeat once they are pending
    new_countdown = (event.countdown - 1)// event_table_data.NUM_BUCKETS
    bucket = (event.countdown - 1 + self._current_bucket) % event_table_data.NUM_BUCKETS 
    event.countdown = new_countdown
    self._buckets[bucket].add_event(event)

  def list_events(self):
    ret_val = list()
    for bucket in self._buckets:
      ret_val.extend(bucket.list_events())
    return ret_val

  def num_events(self):
    return len(self.list_events())

  def cancel_event(self, event):
    for bucket in self._buckets:
      if event in bucket:
        bucket.cancel_event(event)

  def num_buckets(self):
    return len(self._buckets)

  def debug(self):
    ret_val = ""

    for j in range(0, self.num_buckets()):
      if self._buckets[j].num_events() == 0:
        continue
      ret_val += f"Bucket {j}:\r\n"
      ret_val += f"-----------\r\n"
      ret_val += self._buckets[j].debug() + "\r\n"

    return ret_val