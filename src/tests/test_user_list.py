import unittest

from user.user_list import UserList
from user.User import User
import uuid

class TestUserListMethods(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.userList = UserList()
        cls.setUpUser = User()
        cls.setUpUser.name = "June"
        cls.setUpUser.socket = "fake websocket"
        cls.setUpUser.setUUID(str(uuid.uuid4()))
        cls.userList.append(cls.setUpUser)

    @classmethod
    def tearDownClass(cls):
        cls.userList = None

    def testAddUser(cls):
        testUser = User()
        testUser.name = "tester1"
        testUser.socket = "fake websocket 1"
        testUser.setUUID(str(uuid.uuid4()))
        cls.userList.append(testUser)
        assert(cls.userList.getSize() == 2)

        # test delete user
        cls.userList.deleteUserByUUID(testUser.uuid)

        assert (cls.userList.getSize() == 1)

    def testSetNameForSocket(cls):
        testName = "Kevin"
        cls.userList.setNameforSocket(testName, "fake websocket")
        testUser = cls.userList.userFromName(testName)
        testUserByUUID = cls.userList.userByUUID(testUser.uuid)

        assert(testUser is not None)
        assert(testUserByUUID is not None)

    def testContainsUser(cls):

        assert(cls.userList.containsUser(cls.setUpUser))

if __name__ == '__main__':
    unittest.main()