from flask import Flask, render_template
import datetime, time
import RPi.GPIO as GPIO

app = Flask(__name__)
GPIO.setmode(GPIO.BCM)

@app.route('/')
def index():
    now = datetime.datetime.now()
    timeStr = now.strftime("%Y-%m-%d %H:%M")
    templateData = {
        'title': "Hello!",
        'time': timeStr
        }
    return render_template('index.html', **templateData)

@app.route('/log')
def log():
    return render_template('log.html')

# pin = 21
# GPIO.setup(pin, GPIO.IN)

# while True:
#    time.sleep(0.001)
#    if GPIO.input(pin) == GPIO.HIGH:
#        start = time.time()
#        while GPIO.input(pin) == GPIO.HIGH:
#            time.sleep(0.001)
#        finish = time.time()
#        duration = finish - start
#        print "ALERT: Noise detected"
#        print "    Start: ", time.asctime(time.localtime(start))
#        print "    Finish:", time.asctime(time.localtime(finish))
#        print "    Duration (s):", duration


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
