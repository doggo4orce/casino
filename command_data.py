class command_data:
  """Creates a command object to be recorded by the command interpreter.
     command = actual input from player that activated the reponse
     function = function that determines the response to input
     subcmd = specification sent to function to fine tune behaviour"""
  def __init__(self, command, function, subcmd):
    self.command = command
    self.function = function
    self.subcmd = subcmd