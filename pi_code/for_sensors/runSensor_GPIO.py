#! /usr/bin/python2

import os
import time
from datetime import datetime
import sys
from RunningMedian import RunningMedian
from FilterWindow import FilterWindow
import csv
from get_flow_rate import get_flow_rate, WINDOW_WIDTH_RAW, FPS
import threading
EMULATE_HX711=False
if not EMULATE_HX711:
    import RPi.GPIO as GPIO
    from hx711 import HX711
else:
    from emulated_hx711 import HX711

class runSensor_GPIO:
    def __init__(self):
        self.hx = HX711(5, 6)
        self.rn = RunningMedian(50)
        self.flow_rates = []
        self.filter_window = FilterWindow(WINDOW_WIDTH_RAW,FPS)
        self.total_avg_weights = []
        self.current_flow_rate = 0
        self.stop = False
    def initialize_sensor(self):
        referenceUnit = -2390

        #Set reference unit and tare scale
        self.hx.set_reading_format("MSB", "MSB")
        self.hx.set_reference_unit(referenceUnit)
        self.hx.reset()
        self.hx.tare()
        
    def cleanAndExit(self):
        self.stop = True
        #self.thread.join()
        #Cleanup GPIO
        print("Cleaning...")

        if not EMULATE_HX711:
            GPIO.cleanup()
            
        print("Bye!")
        sys.exit()
        
    def save_data(self):
        #save_data
        data_folder = '/home/pi/repos/fydp-neofeed/sensor_data/raspberrypi_data'
        
        curr_datetime = datetime.now()
        
        # save total_avg_weights
        with open(os.path.join(data_folder, 'total_avg_weights--' + str(curr_datetime) + '.csv'),'w',newline = "") as f:
            write = csv.writer(f)
            write.writerows([[x] for x in self.total_avg_weights])
            
        # save flow_rate values
        with open(os.path.join(data_folder, 'flow_rates--' + str(curr_datetime) + '.csv'),'w',newline = "") as f:
            write = csv.writer(f)
            write.writerows([[x] for x in self.flow_rates])
                    
    def return_flow_rate(self):
        while True:
            avg_count = 10
            total_weight = 0
            for i in range(avg_count):
                
                #Find avg median
                weight = self.hx.get_weight(1)
                self.rn.add(weight)
                avg_med_val = self.rn.findAvgMedian(10)
                total_weight = total_weight+avg_med_val
                
            #Find overall average
            avg_weight = total_weight/avg_count
            print("current weight",avg_weight)
            #print("current weight",avg_weight)


            #Get array of averages
            avg_weights = self.filter_window.get_filter_window(avg_weight)
            
            #Get flow rate
            self.current_flow_rate, self.flow_rates = get_flow_rate(avg_weights, self.flow_rates)
            print("current flow rate",self.current_flow_rate)
            
            #save_data
            self.total_avg_weights.append(avg_weight)
            if self.stop:
                break
    def start_thread(self):
        self.thread = threading.Thread(target=self.return_flow_rate)
        self.thread.start()
'''
for testing
flow_sensor = runSensor_GPIO()
flow_sensor.initialize_sensor()
try:
    flow_sensor.return_flow_rate()
except KeyboardInterrupt:
    flow_sensor.save_data()
    flow_sensor.cleanAndExit()
'''