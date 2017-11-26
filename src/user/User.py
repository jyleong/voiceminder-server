from enum import Enum

class UserState(Enum):
  Nameless = 0
  NameStaging = 1
  Ready = 2
  Conversing = 3

class User(object):
  socket = None
  name = None
  state = UserState.Nameless
  """docstring for User"""
  def __init__(self):
    super(User, self).__init__()
    

