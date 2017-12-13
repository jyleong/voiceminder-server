from enum import Enum

class UserState(Enum):
  Nameless = 0
  NameStaging = 1
  Ready = 2
  Conversing = 3
  Invalid = 99

class User(object):
  socket = None
  name = None
  state = UserState.Nameless
  conversant = None
  """docstring for User"""
  def __init__(self):
    super(User, self).__init__()

  def setState(self, newState):
    if newState == 0:
      self.state = UserState.Ready
    elif newState == 1:
      self.state = UserState.NameStaging
    elif newState == 2:
      self.newState = UserState.Ready
    elif newState == 3:
      self.newState = UserState.Conversing
    else:
      self.newState = UserState.Invalid
    print("setState has now set Userstate to ", self.state)
    

