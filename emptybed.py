# medibed

import time

print "Medibed"

tolerance = 40
emptybed = [20, 20, 20, 20]

bedloads = [40, 40, 40, 40]

while True:

    load = sum(bedloads) - sum(emptybed)

    if (load >= tolerance):
        str = "Someone is in bed"
    else:
        str = "Bed is empty"

    print time.strftime("%a, %d %b %Y %H:%M:%S", time.gmtime()) + ": " + str

    time.sleep(5)
