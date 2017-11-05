# manage.py

import os
import datetime
import time
from random import randint
from flask_script import Manager # class for handling a set of commands
from flask_migrate import Migrate, MigrateCommand
from src.app_file import db, create_app, config_name
from src import models

app = create_app(config_name)
migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

def findFullTimeSlept(endTime, startTime, timeToSleep, timeWokenUp, durationWokenUp):
    fullTimeSlept = (endTime - startTime) - timeToSleep - timeWokenUp * durationWokenUp
    return fullTimeSlept

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
    user1 = models.User(name="Rick")
    user2 = models.User(name="Talia")
    user3 = models.User(name="Christina")
    sleepStateList = ["GOOD", "OKAY", "BAD"]


    db.session.add_all([user1, user2, user3])
    db.session.flush()
    db.session.commit()
    print("Users created!")
    print("Seeding database for users sleep records")

    # per user per date, make random entry
    # random entry time to sleep in minutes, times woken up is int, duration woken up is minutes
    # starttime, endtime are timestamps, fulltimesleep is F = (E-D) -A - BC
    date1 = datetime.date(2017, 3, 1)
    date2 = datetime.date(2017, 8, 21)
    day = datetime.timedelta(days=1)
    dateTemp = date1
    while dateTemp <= date2:
        print(dateTemp.strftime('%Y.%m.%d'))
        randIndex1 = randint(0, 2)
        randIndex2 = randint(0, 2)
        randIndex3 = randint(0, 2)
        randTimeDuration1 = randint(4,10)
        randTimeDuration2 = randint(4,10)
        randTimeDuration3 = randint(4,10)

        currentDate = time.mktime(dateTemp.timetuple())

        startTime1 = currentDate + randint(17, 20) * 3600
        endTime1 = startTime1 + randTimeDuration1 * 3600

        startTime2 = currentDate + randint(17, 20) * 3600
        endTime2 = startTime2 + randTimeDuration2 * 3600

        startTime3 = currentDate + randint(17, 20) * 3600
        endTime3 = startTime3 + randTimeDuration3 * 3600


        timeToSleep1 = randint(0,2400)
        timeWokenUp1 = randint(0,4)
        durationWokenUp1 = randint(0,60)

        timeToSleep2 = randint(0, 2400)
        timeWokenUp2 = randint(0, 4)
        durationWokenUp2 = randint(0, 60)

        timeToSleep3 = randint(0, 2400)
        timeWokenUp3 = randint(0, 4)
        durationWokenUp3 = randint(0, 60)


        fullTimeSlept1 = findFullTimeSlept(endTime1, startTime1, timeToSleep1, timeWokenUp1, durationWokenUp1)
        fullTimeSlept2 = findFullTimeSlept(endTime2, startTime2, timeToSleep2, timeWokenUp2, durationWokenUp2)
        fullTimeSlept3 = findFullTimeSlept(endTime3, startTime3, timeToSleep3, timeWokenUp3, durationWokenUp3)
        sleepRecord1 = models.SleepRecord(user1.id, sleepState=sleepStateList[randIndex1],
                                          startTime=startTime1, endTime=endTime1, fullTimeSlept=fullTimeSlept1,
                                          date=currentDate, timeToSleep=timeToSleep1, timeWokenUp=timeWokenUp1,
                                          durationWokenUp=durationWokenUp1)
        sleepRecord2 = models.SleepRecord(user2.id, sleepState=sleepStateList[randIndex2],
                                          startTime=startTime2, endTime=endTime2, fullTimeSlept=fullTimeSlept2,
                                          date=currentDate, timeToSleep=timeToSleep2, timeWokenUp=timeWokenUp2,
                                          durationWokenUp=durationWokenUp2)
        sleepRecord3 = models.SleepRecord(user3.id, sleepState=sleepStateList[randIndex3],
                                          startTime=startTime3, endTime=endTime3, fullTimeSlept=fullTimeSlept3,
                                          date=currentDate, timeToSleep=timeToSleep3, timeWokenUp=timeWokenUp3,
                                          durationWokenUp=durationWokenUp3)
        db.session.add_all([sleepRecord1, sleepRecord2, sleepRecord3])
        db.session.flush()
        db.session.commit()
        dateTemp = dateTemp + day
    print("all sleep records added")
    return

if __name__ == '__main__':
    manager.run()