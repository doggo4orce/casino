class event_data:
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

class speech_event(event_data):
  """if target == None, then owner will use 'say', otherwise they will 'tell' the target?"""
  def __init__(self, owner, speech, target, count_down):
    def speech_function(ch, mud, db):
      commands.do_say(ch, None, speech, None, mud, db)

    super().__init__(owner, speech_function, target, count_down)

