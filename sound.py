import time
import RPi.GPIO as GPIO

# Use board pin numbers
GPIO.setmode(GPIO.BCM)

def getSound(pin):
	GPIO.setup(pin, GPIO.IN)
	if GPIO.input(pin) == GPIO.HIGH:
		return 1
	else
		return 0
	
#
#while True:
#    time.sleep(0.001)
#    if GPIO.input(pin) == GPIO.HIGH:
#        start = time.time()
#        while GPIO.input(pin) == GPIO.HIGH:
#            time.sleep(0.001)
#        finish = time.time()
#        duration = finish - start
#        print ("ALERT: Noise detected")
#        print ("    Start: ", time.asctime(time.localtime(start)))
#        print ("    Finish:", time.asctime(time.localtime(finish)))
#        print ("    Duration (s):", duration)
