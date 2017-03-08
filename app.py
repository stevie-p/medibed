from flask import Flask, render_template
from flask_socketio import SocketIO, send, emit
from threading import Thread, Event
import eventlet
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
thresholdSound = 1 # number of cylces to trigger a sound alert

thread = Thread()
thread_stop_event = Event()

class MeasureThread(Thread):
    def __init__(self):
        self.delay = 1
        super(MeasureThread, self).__init__()

    def reading(self):
        
        previous = {
            'time': str(datetime.datetime.now()),
            'forceLeg1': 0,
            'forceLeg2': 0,
            'forceTotal': 0,
            'status': "Unknown"
        }
        
				soundStart = 0
				
        while not thread_stop_event.isSet():
						data = {
                'time': str(datetime.datetime.now()),
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

            if (data['status'] != previous['status']):
                socketio.emit('change', data, namespace='/medibed')
            
						if (data['sound']==1 && previous['sound']==0):
							  soundStart = data['time']
						elif (data['sound']==0 && previous['sound']==1):
							  soundFinish = data['time']
								soundDuration = round(soundFinish - soundStart, 2)
								alert = {
									'type': 'sound',
									'time': soundStart,
									'duration': soundDuration,
								}
						    socketio.emit('alert', alert, namespace='/medibed')
						
            previous = data

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

@socketio.on('connect', namespace='/medibed')
def handle_connected():
    # Make thread global
    global thread
    print('Client connected')

    # Start the measurement thread
    if not thread.isAlive():
        print('Starting Thread')
        thread = MeasureThread()
        thread.start()

@socketio.on('disconnect', namespace='/medibed')
def handle_disconnect():
    thread.stop()
    print('Client disconnected')

    
if __name__ == '__main__':
    socketio.run(app, port=80, debug=True)
