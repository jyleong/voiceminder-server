# models.py
# created by James L 07/07/2017

# file for all our database related python objects, used for ORM

from user.User import User, UserState
from src.app_file import db
from sqlalchemy.types import DateTime
from datetime import datetime
import re
import uuid
import base64

def uuid_url64():
    rv = base64.b64encode(uuid.uuid4().bytes).decode('utf-8')
    return re.sub(r'[\=\+\/]', lambda m: {'+': '-', '/': '_', '=': ''}[m.group(0)], rv)


class User(db.Model):
    """The test case table in mera_db"""
    __tablename__ = "users"

    id = db.Column(db.String(60), unique=True, primary_key=True)
    userName = db.Column(db.String(60))
    nickName = db.Column(db.String(60))
    userState = db.Column(db.Enum(UserState))
    created_at = db.Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def __init__(self, userName="", userState=UserState.Nameless):
        self.id = str(uuid_url64())
        self.userName = userName
        self.nickName = ""
        self.userState = userState

    def setUserName(self, userName):
        self.userName = userName
        print("UserId {} name is set to {}!".format(self.id, self.name))

    def setState(self, newState):
        self.userState = newState
        print("UserId {} is now in state {}".format(self.id, self.state))

class Conversation(db.Model):
    __tablename__ = "conversations"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)

    userFirstId = db.Column(db.String(60), db.ForeignKey('users.id'), nullable=False)
    userSecondId = db.Column(db.String(60), db.ForeignKey('users.id'), nullable=False)
    userFirst = db.relationship('User', foreign_keys=[userFirstId])
    userSecond = db.relationship('User', foreign_keys=[userSecondId])
    created_at = db.Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def __init__(self, userFirstId, userSecondId):
        self.userFirstId = userFirstId
        self.userSecondId = userSecondId


class ConversationMessage(db.Model):
    __tablename__ = "conversationmessages"
    ## id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    conversationId = db.Column(db.Integer, db.ForeignKey('conversations.id'), primary_key=True, nullable=False)
    userId = db.Column(db.String(60), db.ForeignKey('users.id'), primary_key=True, nullable=False)
    conversation = db.relationship('Conversation', foreign_keys=[conversationId])
    user = db.relationship('User', foreign_keys=[userId])
    created_at = db.Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def __init__(self, userId, conversationId):
        self.conversationId = conversationId
        self.userId = userId






