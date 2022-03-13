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
import pigpio
from sensor import sensor

class runSensor_PIGPIO:
    def __init__(self):
        def cbf(count, mode, reading):
            print(count, mode, reading)
        self.pi = pigpio.pi()
        if not self.pi.connected:
            exit(0)
        self.CH_A_GAIN_64  = 0 # Channel A gain 64
        self.CH_B_GAIN_32 = 1 # Channel A gain 128
        self.s = sensor(self.pi, DATA=5, CLOCK=6, mode=self.CH_B_GAIN_32, callback=cbf)
        self.rn = RunningMedian(50)
        self.flow_rates = []
        self.filter_window = FilterWindow(WINDOW_WIDTH_RAW,FPS)
        self.total_avg_weights = []
        self.current_flow_rate = 0
        self.stop = False

    def initialize_sensor(self):
        time.sleep(2)
        self.s.set_callback(None)
        self.s.set_mode(self.CH_A_GAIN_64)
        self.c, mode, reading = self.s.get_reading()
        
    def cleanAndExit(self):
        self.stop = True
        self.thread.join()
        #Cleanup pig
        print("Cleaning...")

        self.s.pause()
        self.s.cancel()
        self.pi.stop()
            
        print("Bye!")

    def save_data(self):
        #save_data
        data_folder = '/home/pi/repos/fydp-neofeed/sensor_data/raspberrypi_data'
        
        curr_datetime = datetime.now()
        
        # save total_avg_weights
        with open(os.path.join(data_folder, 'total_avg_weights--' + str(curr_datetime).replace(":","-") + '.csv'),'w',newline = "") as f:
            write = csv.writer(f)
            write.writerows([[x] for x in self.total_avg_weights])
            
        # save flow_rate values
        with open(os.path.join(data_folder, 'flow_rates--' + str(curr_datetime).replace(":","-") + '.csv'),'w',newline = "") as f:
            write = csv.writer(f)
            write.writerows([[x] for x in self.flow_rates])
                    
    def return_flow_rate(self):
        while True:
            avg_count = 10
            total_weight = 0
            for i in range(avg_count):
                #Find avg median
                count, mode, reading = self.s.get_reading()
                reading = reading/2390*-1
                if count != self.c:
                    self.c = count
                    weight = reading
                    self.rn.add(weight)
                    avg_med_val = self.rn.findAvgMedian(10)
                    total_weight = total_weight+avg_med_val
                
            #Find overall average
            avg_weight = total_weight/avg_count
            #print("current weight",avg_weight)


            #Get array of averages
            avg_weights = self.filter_window.get_filter_window(avg_weight)
            
            #Get flow rate
            self.current_flow_rate, self.flow_rates = get_flow_rate(avg_weights, self.flow_rates)
            #print("current flow rate",self.current_flow_rate)
            
            #save_data
            self.total_avg_weights.append(avg_weight)
            if self.stop:
                break
            
    def start_thread(self):
        self.thread = threading.Thread(target=self.return_flow_rate)
        self.thread.start()
'''
flow_sensor = runSensor()
flow_sensor.initialize_sensor()
try:
    while True:
        flow_rate = flow_sensor.return_flow_rate()
        print(flow_rate)
except KeyboardInterrupt:
    flow_sensor.save_data()
    flow_sensor.cleanAndExit()
'''
