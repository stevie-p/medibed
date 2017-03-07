import time, datetime
import RPi.GPIO as GPIO

# Use board pin numbers
GPIO.setmode(GPIO.BCM)

# Set capacitance = 0.1uF
C = 0.0000001

def RCtime (PiPin):
    
    # Discharge capacitor
    GPIO.setup(PiPin, GPIO.OUT)
    GPIO.output(PiPin, GPIO.LOW)
    time.sleep(0.1)

    # Set pin as input, capacitor starts charging
    GPIO.setup(PiPin, GPIO.IN)
    start = time.time()

    # Measure time until pin goes HIGH
    wait = 0
    while (GPIO.input(PiPin) == GPIO.LOW):
        wait = time.time() - start
        if wait > 0.2:
            break
        
    finish = time.time()

    # print("RC time on pin", PiPin, "=", finish-start)
    return finish - start

def FSRforce (conductance):
    # Assuming FSR Conductance (G) is proportional to Force (F) (F = 0.004*G)
    force = 0.004 * conductance
    # print("Estimated force =", force)
    return round(force, 3) # rounded to 3 decimal places

def getForce (PiPin):
    conductance = 1000000 * C / RCtime(PiPin)
    force = FSRforce(conductance)
    # print(PiPin, str(datetime.datetime.now()), force)
    return force

if __name__ == '__main__':
    getForce(23)
    getForce(24)
