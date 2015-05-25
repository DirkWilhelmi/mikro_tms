#!/usr/bin/python

from r515.projector import Connection, BasicFunctions
import wiringpi2 as wiringpi
from time import sleep

wiringpi.wiringPiSetup()

wiringpi.pinMode(0, 0)
wiringpi.pullUpDnControl(0, 2)
wiringpi.pinMode(2, 1)      # sets GPIO 2 to output  
wiringpi.digitalWrite(2, 0) # sets port 24 to 0 (0V, off)  
  
try:  
    while True:  
        if not wiringpi.digitalRead(0):     # If button on GPIO25 pressed   
            wiringpi.digitalWrite(2, 1) # switch on LED. Sets port 24 to 1 (3V3, on)  
        else:  
            wiringpi.digitalWrite(2, 0) # switch off LED. Sets port 24 to 0 (0V, off)  
        sleep(0.05)                      # delay 0.05s  
  
finally:  # when you CTRL+C exit, we clean up  
    wiringpi.digitalWrite(2, 0) # sets port 24 to 0 (0V, off)  
    wiringpi.pinMode(2, 0)      # sets GPIO 24 back to input Mode  
    # GPIO 25 is already an input, so no need to change anything  
