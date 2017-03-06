import time, datetime
import RPi.GPIO as GPIO

# Use board pin numbers
GPIO.setmode(GPIO.BCM)

# Set input pin as #21
pin = 23

# Set capacitance = 0.1nF
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
    while (GPIO.input(PiPin) == GPIO.LOW):
        pass
    
    finish = time.time()
    
    return finish - start

def FSRforce (conductance):
    # Assuming FSR Conductance (G) is proportional to Force (F) (F = 0.004*G)
    force = 0.004 * conductance
    return round(force, 3) # rounded to 2 decimal places

while True:
    R = RCtime(pin) / C
    if R > 1000000:
        conductance = 0
    elif R>0:
        conductance = 1000000/R
    else:
        conductance = 0
    
    weight = FSRforce(conductance)
    print (weight, "N") # in Newtons

