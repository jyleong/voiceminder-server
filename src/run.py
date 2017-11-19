import datetime
import os
import time

from flask import jsonify, request
from tornado.ioloop import IOLoop
from tornado.web import Application, FallbackHandler
from tornado.wsgi import WSGIContainer

import app_file
from sockets.websocket import WebSocket
from src import models
from src.app_file import db

app = app_file.create_app(app_file.config_name)


@app.route('/')
def index():
    return "Hello, World!"

@app.route('/sleep/<int:userId>/date', methods=['GET']) # need start and end time or jsut start
def get_sleep_date(userId):
    startTime = request.args.get('startTime', None)
    endTime = request.args.get('endTime', None)
    # now query within this range from database
    sleepRecordSet = []
    if endTime:
        startDateTime = datetime.datetime.strptime(startTime, "%Y-%m-%d")
        startDateTime = time.mktime(startDateTime.timetuple())
        endDateTime = datetime.datetime.strptime(endTime, "%Y-%m-%d")
        endDateTime = time.mktime(endDateTime.timetuple())
        RecordSet = models.SleepRecord.query.filter(models.SleepRecord.userId == userId).filter(models.SleepRecord.date >= startDateTime).filter(models.SleepRecord.date <= endDateTime)
        sleepRecordSet = list(map(lambda x: {"date": x.date,"startTime": x.startTime, "endTime": x.endTime,
                                             "userId": x.userId,"sleepState":x.sleepState,
                                             "fullTimeSlept": x.fullTimeSlept,
                                             "timeToSleep": x.timeToSleep, "timeWokenUp": x.timeWokenUp,
                                             "durationWokenUp": x.durationWokenUp}, RecordSet))
    else:
        startDateTime = datetime.datetime.strptime(startTime, "%Y-%m-%d")
        startDateTime = time.mktime(startDateTime.timetuple())
        RecordSet = models.SleepRecord.query.filter(models.SleepRecord.userId == userId).filter(models.SleepRecord.date >= startDateTime)
        sleepRecordSet = list(map(lambda x: {"date": x.date, "startTime": x.startTime, "endTime": x.endTime,
                                             "userId": x.userId, "sleepState": x.sleepState,
                                             "fullTimeSlept": x.fullTimeSlept,
                                             "timeToSleep": x.timeToSleep, "timeWokenUp": x.timeWokenUp,
                                             "durationWokenUp": x.durationWokenUp}, RecordSet))
    response = jsonify({'sleepData': sleepRecordSet})
    response.status_code = 200
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/sleep/<int:userId>', methods=['POST'])
def post_sleep_record(userId):
    content = request.get_json(silent=False)
    sleepRecord = models.SleepRecord(userId, sleepState=content['sleepState'],
                                      startTime=content['startTime'], endTime=content['endTime'], fullTimeSlept=content['fullTimeSlept'],
                                      date=content['date'], timeToSleep=content['timeToSleep'], timeWokenUp=content['timeWokenUp'],
                                      durationWokenUp=content['durationWokenUp'])
    db.session.add(sleepRecord)
    db.session.commit()
    db.session.refresh(sleepRecord)
    response = jsonify({'id': sleepRecord.id})
    response.status_code = 201
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/users/<int:userId>', methods=['GET'])
def get_user(userId):
    user = models.User.query.get(userId)
    response = jsonify({"id": user.id, "name": user.name})
    response.status_code = 200
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response



if __name__ == '__main__':
    print("PYTHONPATH: {}".format(os.environ['PYTHONPATH']))
    container = WSGIContainer(app)
    server = Application([
        (r'/websocket/', WebSocket),
        (r'.*', FallbackHandler, dict(fallback=container))
    ])

    print("Running server...")
    if 'PRODUCTION' in os.environ:
        # app.run(host="0.0.0.0", port=int(os.environ['PORT']))
        server.listen(port=int(os.environ['PORT']), address="0.0.0.0")
        IOLoop.instance().start()
    else:
        # app.run()
        server.listen(5000)
        IOLoop.instance().start()