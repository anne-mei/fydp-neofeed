#! /usr/bin/python2

import os
import time
from datetime import datetime
import sys
from RunningMedian import RunningMedian
from FilterWindow import FilterWindow
import csv
from get_flow_rate import get_flow_rate, WINDOW_WIDTH_RAW, FPS
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
flow_rates = []
filter_window = FilterWindow(WINDOW_WIDTH_RAW,FPS)
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
        if avg_weight>0:
            print("current weight",avg_weight)


            #Get array of averages
            avg_weights = filter_window.get_filter_window(avg_weight)
            
            current_flow_rate, flow_rates = get_flow_rate(avg_weights, flow_rates)
            print("current flow rate",current_flow_rate)
            #PUT IN FLOW SENSOR READING CODE HERE
            
            #save_data
            total_avg_weights.append(avg_weight)
            
        
        
        #hx.power_down()
        #hx.power_up()
        #time.sleep(0.001)'''
    except (KeyboardInterrupt, SystemExit):
        #save_data
        data_folder = '/home/pi/repos/fydp-neofeed/sensor_data/raspberrypi_data'
        
        curr_datetime = datetime.now()
        
        # save total_avg_weights
        with open(os.path.join(data_folder, 'total_avg_weights--' + str(curr_datetime) + '.csv'),'w',newline = "") as f:
            write = csv.writer(f)
            write.writerows([[x] for x in total_avg_weights])
            
        # save flow_rate values
        with open(os.path.join(data_folder, 'flow_rates--' + str(curr_datetime) + '.csv'),'w',newline = "") as f:
            write = csv.writer(f)
            write.writerows([[x] for x in flow_rates])
            
        
        cleanAndExit()
