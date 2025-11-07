from color import *
import mudlog

class event_data:
  """Creates an event which can be scheduled to occur in the future.
     owner     = what event is attached to (typically char, room, or object)
     func      = function(mud,db) to be called upon execution
     target    = a list of targets for the event
     countdown = number of heart_beat calls remaining until event is executed"""
  def __init__(self, owner, function, countdown):
    self._owner = owner
    self._function = function

    if countdown <= 0:
      mudlog.error(f"Tried to create event with negative countdown.  Countdown set to 1.")
      self.countdown = 1
    else:
      self.countdown = countdown

    self._targets = list()

  @property
  def owner(self):
    return self._owner

  @property
  def function(self):
    return self._function

  """add_target(target)    <- add target to event
     remove_target(target) <- remove target from event
     execute(mud, db)      <- calls event function
     has_targets()         <- check if event has targets
     targets()             <- return copy of self._targets
     heartbeat()           <- decrements countdown
     pending()             <- check if countdown has reached zero"""

  def add_target(self, target):
    self._targets.append(target)

  def remove_target(self, target):
    self._targets.remove(target)

  def execute(self, mud, db):
    self.function(self.owner, mud, db)

  def has_targets(self):
    return len(self.targets()) != 0

  def targets(self):
    return [target for target in self._targets]

  def target_names(self):
    return [target.name for target in self._targets]

  def heartbeat(self):
    if self.pending():
      mudlog.warning(f"Aborting heartbeat called on pending event.")
      return
    self.countdown -= 1

  def pending(self):
    return self.countdown == 0

  def debug(self):
    ret_val = ""
    if self.owner != None:
      ret_val += f"Owner: {CYAN}{self.owner.uid}{NORMAL}\r\n"
    
    ret_val += f"Function: {CYAN}"
    if self.function == None:
      ret_val += "(None)"
    else:
      ret_val += f"{self.function.__name__}"
    ret_val += NORMAL + "\r\n"

    ret_val += f"Targets: {CYAN}"
    if not self.has_targets():
      ret_val += "(None)"
    else:
      ret_val += ', '.join(self.target_names())
    ret_val += NORMAL + "\r\n"

    ret_val += f"Countdown: {CYAN}{self.countdown}{NORMAL}"
    return ret_val