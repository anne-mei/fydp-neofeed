import csv
import numpy as np
import os


# put in pi_code/for_sensors folder to run

def process_csv(csv_path):
    file = open(csv_path)
    csvreader = csv.reader(file)
    csv_data = np.asarray(list(csvreader))
    csv_data = np.asfarray(csv_data,float).flatten()
    return csv_data

# Path to folder containing sensor data (csv file format)
csv_data_folder = r'C:\Users\anne\Projects\FYDP\fydp-neofeed\sensor_data\raspberrypi_data'


#Read sensor data

# csv_name = r'load_medianfilter_3_50_10medavg_10avg_1.csv'  --> process with [60:]
# csv_name = r'load_medianfilter_3_50_10medavg_10avg_2.csv'  --> process with [80:]
# csv_name = r'load_medianfilter_3_50_10medavg_10avg_3.csv'  --> process with [160:]
csv_name = r'2022-03-08-11.47pm-total_avg_weights.csv'

csv_path = os.path.join(csv_data_folder, csv_name)
csv_data = process_csv(csv_path)[600:] 

# =========================================================
# CODE TO PASS IN SENSOR DATA AND GET FLOW RATE VALUES
# =========================================================
from get_flow_rate import get_flow_rate, WINDOW_WIDTH_RAW, FPS

sensor_data = []  # prev raw_data
flow_rate_sig = []
for i in range(len(csv_data)):  # as we get data from the sensor
    val = csv_data[i]
    sensor_data.append(val)

    if i % 100 == 0:
        print('------------100------------')

    # while signal is less than WINDOW_WIDTH_RAW * fps, only get flow rate
    if len(sensor_data) < WINDOW_WIDTH_RAW * FPS:
        single_flowrate = 0
        flow_rate_sig.append(single_flowrate)

    elif len(sensor_data) > WINDOW_WIDTH_RAW * FPS:
        latest_sensor_data = sensor_data[int(-WINDOW_WIDTH_RAW*FPS):]
        single_flowrate, flow_rate_sig = get_flow_rate(latest_sensor_data, flow_rate_sig, i)  # pass in last data and flow_rate segments

        # single_flowrate is the value to display
        # print(i, single_flowrate)