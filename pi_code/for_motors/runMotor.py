#!/usr/bin/env python


# Import required libraries

from flask import Flask, render_template_string, request   # Importing the Flask modules
from time import sleep      # Import sleep module from time library 
import sys
import time
import RPi.GPIO as GPIO
'''
GPIO.setmode(GPIO.BCM)

#Define GPIO signals to use
# Set all pins as output
#GPIO.output( 18, GPIO.LOW )
#GPIO.output( 22, GPIO.LOW )
#GPIO.cleanup()
#p#rint("Setting up pins")

GPIO.setup(18,GPIO.OUT) # step control pin = 18
GPIO.output(18, False) 
GPIO.setup(22,GPIO.OUT) # direction control pin = 22
GPIO.output(22, False)'''

class runMotor():
    def __init__(self):
        self.previous_height = 0
        
    def initialize_motor(self):
      
        # Use BCM GPIO references instead of physical pin numbers
        GPIO.setmode(GPIO.BCM)

        # Define GPIO signals to use
        # Set all pins as output
        print("Setting up pins")
        GPIO.setup(18,GPIO.OUT) # step control pin = 18
        GPIO.output(18, False) 
        GPIO.setup(22,GPIO.OUT) # direction control pin = 22
        GPIO.output(22, False)

    def cleanup_motor(self):
        GPIO.output( 18, GPIO.LOW )
        GPIO.output( 22, GPIO.LOW )
        GPIO.cleanup()
    
    def return_to_base_height(self):
        
        #Return motor to base height
        if self.previous_height>=0:
            self.change_motor_height(self.previous_height,False)
        else:
            print ('Error - Motor no longer knows its position')
            
    def change_motor_height(self,height,moves_up):
        #reinitialize motor
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(18,GPIO.OUT) # step control pin = 18
        GPIO.setup(22,GPIO.OUT) # direction control pin = 22
        
        # Initialise variables
        WaitTime = 0.025 # changed to 500ms
        stepCounter = 0
        stepsToRotate = height*1000*(1/0.3) # convert meters to steps (1 step = 0.3mm)
        
                
        print("Steps to rotate received:",int(stepsToRotate))
        
  
        #Initialize if motor moves up or down and set GPIO
        if moves_up:
            GPIO.output( 22, GPIO.LOW) # high is clockwise and low is counterclockwise
            self.previous_height = self.previous_height+height
        else:
            GPIO.output(22,GPIO.HIGH)
            self.previous_height = self.previous_height-height
            
        #Move motor determined amount of steps
        for stepCounter in range(abs(int(stepsToRotate))):
            #for pin in range(0, 4):
            GPIO.output(18, GPIO.HIGH)
            time.sleep(WaitTime/2)
            GPIO.output(18, GPIO.LOW)
            time.sleep(WaitTime/2)
        
        #Clean GPIO output
        GPIO.output( 18, False )
        GPIO.output( 22, False )
        return height

motor = runMotor()
motor.initialize_motor()
motor.change_motor_height(0.16,True)

