#! /usr/bin/python2

import time
import sys
from RunningMedian import RunningMedian
from FilterWindow import FilterWindow
import csv

#Intialize load sensor
EMULATE_HX711=False

referenceUnit = -2390

if not EMULATE_HX711:
    import RPi.GPIO as GPIO
    from hx711 import HX711
else:
    from emulated_hx711 import HX711

def cleanAndExit():
    print("Cleaning...")

    if not EMULATE_HX711:
        GPIO.cleanup()
        
    print("Bye!")
    sys.exit()

#Initialize clases
hx = HX711(5, 6)
rn = RunningMedian(50)
filter_window = FilterWindow(40,900)
hx.set_reading_format("MSB", "MSB")
hx.set_reference_unit(referenceUnit)
hx.reset()
hx.tare()

#Save data
total_avg_weights = []
while True:
    try:
        
        avg_count = 10
        total_weight = 0
        for i in range(avg_count):
            
            #Find avg median
            weight = hx.get_weight(1)
            rn.add(weight)
            avg_med_val = rn.findAvgMedian(10)
            total_weight = total_weight+avg_med_val
            
        #Find overall average
        avg_weight = total_weight/avg_count
        print(avg_weight)


        #Get array of averages
        avg_weights = filter_window.get_filter_window(avg_weight)
        
        #PUT IN FLOW SENSOR READING CODE HERE
        
        #save_data
        #total_avg_weights.append(avg_weight)
        
        #hx.power_down()
        #hx.power_up()
        #time.sleep(0.001)'''
    except (KeyboardInterrupt, SystemExit):
        #save_data
        '''csv_name = '/result.csv'
        csv_path = '/home/pi/Documents'+csv_name
        with open(csv_path,'w',newline = "") as f:
            write = csv.writer(f)
            write.writerows([[x] for x in total_avg_weights])'''
        
        cleanAndExit()
