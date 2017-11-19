## Socket Instance to hold global dictionary of all in current use sockets,
## should only have aone member variable dictionary of socket instances


class SocketInstances(object):
    __instance = None
    socket_storage = dict()
    def __new__(cls):
        if SocketInstances.__instance is None:
            SocketInstances.__instance = object.__new__(cls)

        return SocketInstances.__instance
    def count():
      return len(socket_storage)