#!/usr/bin/env python
# A tool to graph energy usage, as reported by the Loop energy monitoring
# system, on a Pimoroni Unicorn HAT connected to a Raspberry Pi.
# Requires node-loop.js to be running in the background, called using the
# following command:
# node node-loop.js | gawk -F '[,:]' '{print $11;fflush();}' | xargs -n 1 -I'{}' sh -c 'echo $1 > /tmp/electricityreading.txt' -- {} &
# node-loop.js download and instructions:
# https://github.com/marcosscriven/loop
# Requires gawk: sudo apt-get install gawk
# Requires unicornhat: 
# v1.0
# Gareth Halfacree <gareth@halfacree.co.uk>

import time
import unicornhat as UH

gradients = 200 # Each LED equals a 200W measurement
readinglist = [0,0,0,0,0,0,0,0] # Initialises the list of readings for graphing.

while True:
    readingfile=open('/tmp/electricityreading.txt', 'r')
    rawreading=readingfile.readline() # Get the latest reading
    readingfile.close()
    reading=int(rawreading) # Convert string into integer.
    readinglist.insert(0,reading) # Insert reading at the start of the list.
    del readinglist[8:] # With an 8x8 matrix, we only want eight list entries.
    for x in range(8): # Run through all eight X axis positions.
        for y in range(8): # Graph each Y axis entry based on gradient size.
            readingcomparison = (y+1) * gradients
            if (readinglist[x] >= readingcomparison):
                if (y < 2):
                    UH.set_pixel(x,y,0,255,0) # Green for bottom two LEDs.
                elif (y >= 2) and (y < 4): 
                    UH.set_pixel(x,y,255,255,0) # Yellow for next two LEDs.
                else:
                    UH.set_pixel(x,y,220,20,60) # Red for top four LEDs.
            else:
                UH.set_pixel(x,y,0,0,0) # Turn LEDs above our reading off.
    UH.show() # Update the display
    time.sleep(10) # node-loop.js updates every 10 seconds, so wait a while.
