class UserList(object):
  __instance = None
  users = []
  def __new__(cls):
    if UserList.__instance is None:
        UserList.__instance = object.__new__(cls)
    return UserList.__instance
  
  #happens on connection
  @classmethod
  def append(cls, user):
    cls.users.append(user)

  @classmethod
  def setNameforSocket(cls, name, socket):
    # TODO: make this search faster somehow???
    for u in cls.users:
      if u.socket == socket:
        u.name = name
        return True
    return False

  @classmethod
  def userFromSocket(cls, socket):
    for u in cls.users:
      if u.socket == socket:
        return u
    return None

  @classmethod
  def containsUser(cls, user):
    for u in cls.users:
      if u == user:
        return True
    return False