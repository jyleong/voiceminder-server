import unittest

from user.user_list import UserList
from user.User import User

class TestUserListMethods(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.userList = UserList()
        cls.setUpUser = User()
        cls.setUpUser.name = "June"
        cls.setUpUser.socket = "fake websocket"
        cls.userList.append(cls.setUpUser)

    @classmethod
    def tearDownClass(cls):
        cls.userList = None

    def testAddUser(cls):
        testUser = User()
        testUser.name = "tester1"
        testUser.socket = "fake websocket 1"
        cls.userList.append(testUser)
        assert(cls.userList.getSize() == 2)

        # test delete user
        cls.userList.deleteUserBySocket(testUser.socket)

        assert (cls.userList.getSize() == 1)

    def testSetNameForSocket(cls):
        testName = "Kevin"
        cls.userList.setNameforSocket(testName, "fake websocket")
        testUser = cls.userList.userFromName(testName)
        testUserSocket = cls.userList.userFromSocket("fake websocket")

        assert(testUser is not None)
        assert(testUserSocket is not None)

    def testContainsUser(cls):

        assert(cls.userList.containsUser(cls.setUpUser))

if __name__ == '__main__':
    unittest.main()