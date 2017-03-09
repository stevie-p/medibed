from flask import Flask, render_template
from flask_socketio import SocketIO, send, emit
from threading import Thread, Event
import eventlet, atexit
import datetime, time
import RPi.GPIO as GPIO
import fsr, sound

eventlet.monkey_patch()
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode='eventlet')

GPIO.setmode(GPIO.BCM)

pin1 = 23
pin2 = 24
pinSound = 21

thresholdOccupied = 0.3 # readings over this will have status = occupied
thresholdMovement = 0.2 # If weight shifts more than this over a period, count this as a movement

thread = Thread()
thread_stop_event = Event()

class MeasureThread(Thread):
    def __init__(self):
        self.delay = 1
        self.readings = []
        super(MeasureThread, self).__init__()

    def addReading(self, data):
        self.readings.append(data)
        if (len(self.readings)>10):
            self.readings.pop(0)

    def getAverages(self):
        averages = {
            'leg1': 0,
            'leg2': 0
            }
        for reading in self.readings:
            averages['leg1'] += reading['forceLeg1']
            averages['leg2'] += reading['forceLeg2']
        averages['leg1'] = averages['leg1'] / len(self.readings)
        averages['leg2'] = averages['leg2'] / len(self.readings)
        return averages

    def reading(self):
        
        previous = {
            'time': str(datetime.datetime.now()),
            'forceLeg1': 0,
            'forceLeg2': 0,
            'forceTotal': 0,
            'status': "Unknown",
            'sound': 0
            }
        
        soundStart = 0
				
        while not thread_stop_event.isSet():
            now = datetime.datetime.now()
            data = {
                'time': now.isoformat(),
                'forceLeg1': fsr.getForce(pin1),
                'forceLeg2': fsr.getForce(pin2),
                'sound': sound.getSound(pinSound)
                }
            data['forceTotal'] = round(data['forceLeg1'] + data['forceLeg2'], 3)
            if (data['forceTotal'] >= thresholdOccupied):
                data['status'] = "Occupied"
            else:
                data['status'] = "Empty"

            print(data)

            socketio.emit('reading', data, namespace='/medibed')

            # Detect sound
            if (data['sound']==1 and previous['sound']==0):
                soundStart = now
            elif (data['sound']==0 and previous['sound']==1):
                soundFinish = now
                soundDuration = soundFinish - soundStart
                event = {
                    'type': 'sound',
                    'time': data['time'],
                    'duration': str(soundDuration),
                    'message': 'ALERT! Loud noise detected.',
                    'class': 'danger'
                    }
                socketio.emit('logEvent', event, namespace='/medibed')

            self.addReading(data)
            averages = self.getAverages()

            # Detect status change
            if (data['status'] != previous['status']):
                event = {
                    'type': 'statusChange',
                    'time': data['time'],
                    'message': 'Bed status changed to '+data['status'],
                    'class': 'warning'
                    }
                socketio.emit('logEvent', event, namespace='/medibed')

            # Detect movement
            elif (data['forceLeg1'] > (averages['leg1'] + thresholdMovement) or 
                data['forceLeg1'] < (averages['leg1'] - thresholdMovement) or
                data['forceLeg2'] > (averages['leg2'] + thresholdMovement) or
                data['forceLeg2'] < (averages['leg2'] - thresholdMovement)):
                # Reset readings array
                del self.readings[:]
                event = {
                    'type': 'movement',
                    'time': data['time'],
                    'message': 'Movement detected'
                }
                socketio.emit('logEvent', event, namespace='/medibed')
	    				
            previous = data
            
            time.sleep(self.delay)

    def run(self):
        self.reading()

    def stop(self):
        thread_stop_event.set()


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/log')
def log():
    return render_template('log.html')

# Start the measurement thread
if not thread.isAlive():
    print('Starting Thread')
    thread_stop_event.clear()
    thread = MeasureThread()
    thread.start()

def interrupt():
    thread.stop()

atexit.register(interrupt)

#@socketio.on('connect', namespace='/medibed')
#def handle_connected():
    # Make thread global
#    global thread
#    print('Client connected')

    

#@socketio.on('disconnect', namespace='/medibed')
#def handle_disconnect():
#    thread.stop()
#    print('Client disconnected')

    
if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=80, debug=True)
