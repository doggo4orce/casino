import commands
import enum

class event_table:
  NUM_BUCKETS = 128
  """Creates an event_table which manages a list of event_buckets
     current_bucket = index next bucket to get a heart beat
     buckets        = list of event_buckets to manage"""

  def __init__(self):
    self._current_bucket = 0
    self._buckets = [ None ] * event_table.NUM_BUCKETS

    for j in range(0, len(self._buckets)):
      self._buckets[j] = event_bucket()

  def heart_beat(self, mud, db):
    self._buckets[self._current_bucket].heart_beat(mud, db)
    self._current_bucket += 1
    self._current_bucket = self._current_bucket % event_table.NUM_BUCKETS

  def add_event(self, event):
    new_count_down = event.count_down // event_table.NUM_BUCKETS
    bucket = (event.count_down + self._current_bucket) % event_table.NUM_BUCKETS 
    event.count_down = new_count_down
    self._buckets[bucket].add_event(event)

  def delete_event(self, event):
    for bucket in self._buckets:
      if event in bucket:
        bucket.delete_event(event)

class event_bucket:
  """Creates an event_bucket which manages a list of scheduled events.
     events = a list of events that have been scheduled"""

  def __init__(self):
    self._events = list()

  """heart_beat(mud)     <- counts down each event and executes/deletes those pending
     add_event(event)    <- schedules new event
     delete_event(event) <- deletes scheduled event (which may have already executed)
     num_events()        <- counts the number of scheduled events"""

  def heart_beat(self, mud, db):
    for event in self._events:
      if event.pending():
        event.execute(mud, db)
        self.delete_event(event)
      else:
        event.heart_beat()

  def add_event(self, event):
    self._events.append(event)

  def delete_event(self, event):
    self._events.remove(event)

  def num_events(self):
    return len(self._events)

  def __contains__(self, event):
    return event in self._events

# just check type(event.owner) instead of bothering with this
# class event_owner_type(enum.IntEnum):
#   OWNER_UNOWNED = 0
#   OWNER_DESC    = 1
#   OWNER_SERVER  = 2
#   OWNER_GAME    = 3
#   OWNER_CHAR    = 4
#   OWNER_OBJECT  = 5
#   OWNER_ROOM    = 6

# just check type(event.target) instead of bothering with this
# class event_target_type(enum.IntEnum):
#   TARGET_NONE   = 0
#   TARGET_CHAR   = 1
#   TARGET_OBJECT = 2

class event:
  """Creates an event which can be scheduled to occur in the future.
     name      = description of the event
     owner     = what event is attached to (typically char, room, or object)
     func      = function to be called upon execution
     target    = a list of targets for the event
     countdown = number of heart_beat calls remaining until event is executed"""
  def __init__(self, owner, func, target, count_down):
    self._owner = owner
    self._func = func

    if type(target) == list:
      self._target = target
    else:
      self._target = [target]

    self._count_down = count_down
    self._id = id

  @property
  def owner(self):
    return self._owner
  @property
  def func(self):
    return self._func
  @property
  def what_type(self):
    return self._what_type
  @property
  def target(self):
    return self._target
  @property
  def count_down(self):
    return self._count_down
  @property
  def id(self):
    return self._id


  @owner.setter
  def owner(self, new_owner):
    self._owner = new_owner
  @func.setter
  def func(self, new_func):
    self._func = new_func
  @what_type.setter
  def type(self, new_type):
    self._type = new_type
  @target.setter
  def target(self, new_target):
    if type(new_target) == list:
      self._target = new_target
    else:
      self._target = [new_target]
  @count_down.setter
  def count_down(self, new_count_down):
    self._count_down = new_count_down

  """execute(mud) <- calls the func, mud passed so events can access owner surroundings
     heart_beat() <- decrements the countdown
     pending()    <- checks whether the countdown has reached zero"""
  def execute(self, mud, db):
    # put an try/catch in here?
    self._func(self._owner, mud, db)

  def heart_beat(self):
    self._count_down -= 1

  def pending(self):
    return self._count_down == 0

class speech_event(event):
  """if target == None, then owner will use 'say', otherwise they will 'tell' the target?"""
  def __init__(self, owner, speech, target, count_down):
    def speech_function(ch, mud, db):
      commands.do_say(ch, None, speech, None, mud, db)

    super().__init__(owner, speech_function, target, count_down)

if __name__ == '__main__':
  e_list = list()
  e = event(3, 3, None, None, None)
  print(type(e_list))
  e_list.append(3)
  e_list.append(e)
  f_list = [e]
  print(type(f_list))
  print(f_list[0].name)

