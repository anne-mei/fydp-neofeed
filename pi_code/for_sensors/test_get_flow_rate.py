import csv
import numpy as np
import os



def process_csv(csv_path):
    file = open(csv_path)
    csvreader = csv.reader(file)
    csv_data = np.asarray(list(csvreader))
    csv_data = np.asfarray(csv_data,float).flatten()
    return csv_data

# Path to folder containing sensor data (csv file format)
csv_data_folder = r'C:\Users\anne\Projects\FYDP\fydp-neofeed\sensor_data\2022-03-04 Load sensor trials'


#Read sensor data

# csv_name_15_light4 = r'light_15ml_4.csv'
csv_name = r'load_medianfilter_3_50_10medavg_10avg_1.csv'
# csv_name = r'load_medianfilter_3_50_10medavg_10avg_2.csv'  --> process with [80:]
# csv_name = r'load_medianfilter_3_50_10medavg_10avg_3.csv'  --> process with [160:]

csv_path = os.path.join(csv_data_folder, csv_name)
csv_data = process_csv(csv_path)[60:] #120]

# =========================================================
# CODE TO PASS IN SENSOR DATA AND GET FLOW RATE VALUES
# =========================================================
from get_flow_rate import get_flow_rate, WINDOW_WIDTH_RAW, FPS

sensor_data = []  # prev raw_data
flow_rate_sig = []
for i in range(len(csv_data)):  # as we get data from the sensor
    val = csv_data[i]
    sensor_data.append(val)

    # while signal is less than WINDOW_WIDTH_RAW * fps, only get flow rate
    if len(sensor_data) < WINDOW_WIDTH_RAW * FPS:
        single_flowrate = 0
        flow_rate_sig.append(single_flowrate)

    elif len(sensor_data) > WINDOW_WIDTH_RAW * FPS:
        latest_sensor_data = sensor_data[int(-WINDOW_WIDTH_RAW*FPS):]
        single_flowrate, flow_rate_sig = get_flow_rate(latest_sensor_data, flow_rate_sig)  # pass in last data and flow_rate segments
        
        # single_flowrate is the value to display
        print(i, single_flowrate)
        
