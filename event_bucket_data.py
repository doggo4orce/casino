import enum

class event_bucket_data:
  """Creates an event bucket which manages a list of scheduled events.
     events = a list of events that have been scheduled"""

  def __init__(self):
    self._events = list()

  """heartbeat(mud)      <- counts down each event and executes/deletes those pending
     add_event(event)    <- schedules new event
     list_events()       <- returns copy of event list
     cancel_event(event) <- deletes scheduled event (which may have already executed)
     num_events()        <- counts the number of scheduled events"""

  def heartbeat(self, mud, db):
    for event in self._events:
      if event.pending():
        event.execute(mud, db)
        self.cancel_event(event)
      else:
        event.heartbeat()

  def add_event(self, event):
    self._events.append(event)

  def list_events(self):
    return [list for list in self._events]

  def cancel_event(self, event):
    self._events.remove(event)

  def num_events(self):
    return len(self._events)

  def debug(self):
    ret_val = ""
    for event in self._events:
      ret_val += f"{event.debug()}\r\n"
    return ret_val

  def __contains__(self, event):
    return event in self._events
