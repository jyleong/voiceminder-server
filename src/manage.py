# manage.py

from user.User import UserState
from flask_script import Manager # class for handling a set of commands
from flask_migrate import Migrate, MigrateCommand
from src.app_file import db, create_app, config_name
from src import models

app = create_app(config_name)
migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)


@manager.command
def seed():
    '''
    Assumes you have already have sleeportant database
    db init, and upgrade the databases
    method to create some initial users locally and insert to database
    make sleep records for each user for a large date range ~100-200 days
    :return:
    '''
    print("Seeding database with initial users")
    user1 = models.User(userName="Rick", userState=UserState.Ready)
    user2 = models.User(userName="Talia", userState=UserState.Nameless)
    user3 = models.User(userName="Christina", userState=UserState.Conversing)


    db.session.add_all([user1, user2, user3])
    db.session.flush()
    db.session.commit()
    print("Users created!")
    print("Seeding database for their converstations")
    convo1 = models.Conversation(user1.id, user2.id)
    db.session.add(convo1)
    db.session.commit()

    print("Add conversation message")
    msg1 = models.ConversationMessage(user1.id, convo1.id)
    db.session.add(msg1)
    db.session.commit()
    return

if __name__ == '__main__':
    manager.run()