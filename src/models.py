# models.py
# created by James L 07/07/2017

# file for all our database related python objects, used for ORM

from user.User import User, UserState
from src.app_file import db
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
    name = db.Column(db.String(60))
    userState = db.Column(db.Enum(UserState))
    # conversation = db.relationship("Conversation", backref='user',
    #                lazy='dynamic')

    def __init__(self, name, userState):
        self.id = str(uuid_url64())
        self.name = name
        self.userState = userState

class Conversation(db.Model):
    __tablename__ = "conversations"

    id = db.Column(db.Integer, primary_key=True)

    userFirstId = db.Column(db.String(60), db.ForeignKey('users.id'), primary_key=True)
    userSecondId = db.Column(db.String(60), db.ForeignKey('users.id'), primary_key=True)
    userFirst = db.relationship('User', foreign_keys=[userFirstId])
    userSecond = db.relationship('User', foreign_keys=[userSecondId])

    def __init__(self, userFirstId, userSecondId):
        self.userFirstId = userFirstId
        self.userSecondId = userSecondId




