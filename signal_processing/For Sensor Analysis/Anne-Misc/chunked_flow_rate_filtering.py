# %matplotlib nbagg
#Import required libraries
# from serial import Serial
import csv
import time
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import os
# from drawnow import drawnow, figure
from scipy import stats
from scipy.signal import butter, lfilter, freqz, filtfilt, resample
from sklearn.metrics import mean_squared_error

import pandas as pd
import math
from matplotlib import rcParams
import copy
from tqdm import tqdm
# rcParams.update({'figure.autolayout': True})

from sklearn.metrics import mean_squared_error

def butter_filter(data, cutoff, order, fs):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff)  # , btype='low', analog=False
#     b, a = butter(3, 0.1)
    y = filtfilt(b, a, data)
    return y

def get_rolling_slope(csv_data, datapnt_delay=None, load_scaling_factor=1):
    window_width_raw = 20
    window_width_flowrate = 20
    cutoff_1 = 0.1 # 0.02
    order_1 = 6 # 12  # original: 3
    fps = 1000/datapnt_delay
 
    raw_data = []
    flow_rate = []
    flow_rate_filtered = []
    flow_rate_filtered_new1 = []
    flow_rate_filtered_new2 = []
    flow_rate_filtered_new3 = []
    flow_rate_filtered_new4 = []
    flow_rate_filtered_new5 = []

    flow_rate_filtered_seg1 = True

    for i in tqdm(range(len(csv_data))):
        val = csv_data[i]
        raw_data.append(val)
        if i>window_width_raw*fps:
            curr_window_raw = raw_data[int(-window_width_raw*fps):]
            curr_window_raw_filtered = butter_filter(curr_window_raw, cutoff_1, order_1, fps)
            x =list(range(len(curr_window_raw_filtered)))
            curr_slope, intercept, r, p, std_err = stats.linregress(x, curr_window_raw_filtered)
            #print('curr_slope:', curr_slope)
            
            # if i % 10 == 0:
            #     plt.plot(curr_window_raw, label='curr_window_raw')
            #     plt.plot(curr_window_raw_filtered, label='curr_window_raw_filtered')
            #     plt.plot([curr_slope*val + intercept for val in x], label='fitted line', color='black')
            #     plt.legend()
            #     plt.show(block=False)
            #     plt.close()
            
            # #Convert light results
            # syringe_rad = 21.7/2 #Syringe radius in mm
            # syringe_area = math.pi*(syringe_rad ** 2)
            # conversion_factor = 0.06*fps
            # curr_flowrate = curr_slope*syringe_area*conversion_factor
            # flow_rate.append(curr_flowrate)

            # convert to load sensor results
            density = 1 #1g/mL
            curr_flowrate = (1/density)*curr_slope*60*fps*(-1)  #convert from g/s to mL/min       
            flow_rate.append(curr_flowrate)     
        else:
            flow_rate.append(0)
                
        cutoff_2 = 0.1 # 0.6
        order_2 = 6
        if len(flow_rate) > (window_width_raw + window_width_flowrate)*fps and len(flow_rate) % int(-window_width_flowrate*fps) == 0:
            curr_start = int(-window_width_flowrate*fps)
            curr_window_flowrate = flow_rate[curr_start:]
            
#             curr_window_flowrate_filtered = butter_filter(curr_window_flowrate, cutoff_2, order_2, fps)[0]
            temp_filtered_sig1 = butter_filter(curr_window_flowrate, 0.4, 6, fps)
            # temp_filtered_sig2 = butter_filter(curr_window_flowrate, 0.01, 6, fps)
            # temp_filtered_sig3 = butter_filter(curr_window_flowrate, 0.1, 3, fps)
            # temp_filtered_sig4 = butter_filter(curr_window_flowrate, 0.2, 6, fps)
            # temp_filtered_sig5 = butter_filter(curr_window_flowrate, 0.05, 6, fps)


            # if flow_rate_filtered_seg1:
            #     flow_rate_filtered_new = temp_filtered_sig.tolist()
            #     flow_rate_filtered_seg1 = False
            # else:
            #     flow_rate_filtered_new.append(0)  # adding a placeholder value at the end
            #     flow_rate_filtered_new[curr_start:] = temp_filtered_sig

            flow_rate_filtered_new1 = flow_rate_filtered_new1 + list(temp_filtered_sig1)
            # flow_rate_filtered_new2 = flow_rate_filtered_new2 + list(temp_filtered_sig2)
            # flow_rate_filtered_new3 = flow_rate_filtered_new3 + list(temp_filtered_sig3)
            # flow_rate_filtered_new4 = flow_rate_filtered_new4 + list(temp_filtered_sig4)
            # flow_rate_filtered_new5 = flow_rate_filtered_new5 + list(temp_filtered_sig5)


            curr_window_flowrate_filtered = np.mean(curr_window_flowrate)

            # plt.plot(temp_filtered_sig1, label='sig1')
            # plt.plot(temp_filtered_sig2, label='sig2')
            # plt.plot(temp_filtered_sig3, label='sig3')
            # # plt.plot(temp_filtered_sig4, label='sig4')
            # plt.plot(temp_filtered_sig5, label='sig5')

            # plt.plot(curr_window_flowrate, label='curr_window_flowrate')
            # # plt.plot(temp_filtered_sig2, label='temp_filtered_sig2')
            # plt.legend()
            # # plt.ylim([0,3])
            # plt.show(block=False)
            # plt.close()

            flow_rate_filtered.append(curr_window_flowrate_filtered)

        else:
            flow_rate_filtered.append(0)
    # return flow_rate_filtered

    # # plt.plot(flow_rate_filtered_new1, label='sig1')
    # plt.plot(flow_rate_filtered_new2, label='sig2')
    # # plt.plot(flow_rate_filtered_new3, label='sig3')
    # # plt.plot(flow_rate_filtered_new4, label='sig4')
    # # plt.plot(flow_rate_filtered_new5, label='sig5')
    # plt.ylim([0,3])
    # plt.legend()
    # plt.show()

    # if resample_bool:
    #     flow_rate_filtered_new1 = resample(flow_rate_filtered_new1, 10000)

    scaled_flow_rate = [val*load_scaling_factor for val in flow_rate_filtered_new1]
    return scaled_flow_rate
#     return flow_rate

def get_rolling_slope_measured(csv_data,time):
    #Sampled every 5 seconds - real data
    fps = 1
    window_width = 3
    slope = []
    raw_data = []
    for i in range(len(csv_data)):
        val = csv_data[i]
        raw_data.append(val)
        if i>window_width*fps:
            curr_window = raw_data[int(-window_width*fps):]
            x =list(range(len(curr_window)))
            curr_slope, intercept, r, p, std_err = stats.linregress(x, curr_window)
            slope.append(curr_slope)
        else:
            slope.append(0)
         
    #Calculate flow rate depending on sensor data type
    density_milk = 1 
    conversion_factor = 60
    time_interval = 5 #5s between data recordings
    flow_rate = np.multiply(slope,(1/time_interval*(1/density_milk)*conversion_factor))
    
    data_mean, data_std = np.mean(flow_rate), np.std(flow_rate)
    # identify outliers
    cut_off = data_std * 0.2 # 0.6
    lower, upper = data_mean - cut_off, data_mean + cut_off
    indexes_to_remove = np.where((flow_rate< lower) | (flow_rate > upper))[0]
  
    flow_rate_filtered = np.delete(flow_rate, indexes_to_remove)#indexes_to_remove[0])
    time_filtered = np.delete(np.array(time),indexes_to_remove)
    
    # if resample_bool:
    #     flow_rate_filtered = resample(flow_rate_filtered, 10000)
    return flow_rate_filtered,time_filtered

    
def get_time(csv_data, datapnt_delay):

    # datapnt_delay = 10 #163
    fps = 1000/datapnt_delay
    time = np.multiply(range(0,len(csv_data)),(1/fps))
    return time


def process_csv(csv_path):
    file = open(csv_path)
    # file = open(csv_path, newline='', encoding='utf-8-sig')
    csvreader = csv.reader(file)
    csv_data = np.asarray(list(csvreader))
    csv_data = np.asfarray(csv_data,float).flatten()
    return csv_data

# =====================
# LOAD DATA FROM CSV
# =====================
# Path to folder containing sensor data (csv file format)
# csv_data_folder = r'C:\Users\anne\Projects\FYDP\fydp-neofeed\sensor_data\2022-02-26 Height Cali and Light Sensor'
# csv_data_folder = r'C:\Users\anne\Projects\FYDP\fydp-neofeed\sensor_data\2022-03-01 Averaging Light Sensor'
# csv_data_folder = r'C:\Users\anne\Projects\FYDP\fydp-neofeed\sensor_data\2022-03-04 Load sensor trials'
csv_data_folder = r'C:\Users\anne\Projects\FYDP\fydp-neofeed\sensor_data\raspberrypi_data'


#Read sensor data
csv_name_30_light1 = r'total_avg_weights--2022-03-10 22_41_05.359004.csv'
# csv_name_30_light2 = r'total_avg_weights--2022-03-10 23_24_11.330455.csv'
csv_name_30_light3 = r'total_avg_weights--2022-03-11 00_21_52.936960.csv'
datapoint_delay = 100


csv_path_30_light1 = os.path.join(csv_data_folder, csv_name_30_light1)
# csv_path_30_light2 = os.path.join(csv_data_folder, csv_name_30_light2)
csv_path_30_light3 = os.path.join(csv_data_folder, csv_name_30_light3)

csv_data_30_light1 = process_csv(csv_path_30_light1)
# csv_data_30_light2 = process_csv(csv_path_30_light2)
csv_data_30_light3 = process_csv(csv_path_30_light3)[:20000]

time_30_light1 = get_time(csv_data_30_light1, datapoint_delay)
# time_30_light2 = get_time(csv_data_30_light2, datapoint_delay)
time_30_light3 = get_time(csv_data_30_light3, datapoint_delay)



csv_name_30_light_measured = r'Scale_data/2022-03-10-Load Sensor Trials with Pi.csv'
csv_path_30_light_measured = os.path.join(csv_data_folder, csv_name_30_light_measured)
csv_data_30_light_measured = pd.read_csv(csv_path_30_light_measured)

time_30_light_measured1 = csv_data_30_light_measured['Time'][csv_data_30_light_measured['Trial 1'].notna()]
# time_30_light_measured2 = csv_data_30_light_measured['Time'][csv_data_30_light_measured['Trial 2'].notna()]
time_30_light_measured3 = csv_data_30_light_measured['Time'][csv_data_30_light_measured['Trial 3'].notna()]

csv_data_30_light_measured1 = csv_data_30_light_measured['Trial 1'].dropna()
# csv_data_30_light_measured2 = csv_data_30_light_measured['Trial 2'].dropna()
csv_data_30_light_measured3 = csv_data_30_light_measured['Trial 3'].dropna()


# # =====================
# # PLOT RAW SENSOR DATA
# # =====================
# #Read sensor data
# fig, axs = plt.subplots(3,2)

# axs[0,0].plot(time_30_light_measured1,csv_data_30_light_measured1)
# axs[0,1].plot(time_30_light1,csv_data_30_light1)

# axs[1,0].plot(time_30_light_measured2,csv_data_30_light_measured2)
# axs[1,0].set_ylabel('Mass (g)')
# axs[1,1].plot(time_30_light2,csv_data_30_light2)
# axs[1,1].set_ylabel('Light Reading (mm)')

# axs[2,0].plot(time_30_light_measured3,csv_data_30_light_measured3)
# axs[2,1].plot(time_30_light3,csv_data_30_light3)
# axs[2,0].set_xlabel('Time (s)')
# axs[2,1].set_xlabel('Time (s)')

# load_scaling_factor = 0.54
load_scaling_factor = 1  #1.2
# PLOT FLOW RATE SIGNAL
flow_rate_light1 = get_rolling_slope(csv_data_30_light1, datapoint_delay, load_scaling_factor=load_scaling_factor)[2550:]
# flow_rate_light2 = get_rolling_slope(csv_data_30_light2, datapoint_delay, load_scaling_factor=load_scaling_factor)
flow_rate_light3 = get_rolling_slope(csv_data_30_light3, datapoint_delay, load_scaling_factor=load_scaling_factor)[3150:-851]


flow_rate_light_measured1, time_light_measured1_filt = get_rolling_slope_measured(csv_data_30_light_measured1,time_30_light_measured1) #, resample_bool=resample_bool)
# flow_rate_light_measured2, time_light_measured2_filt = get_rolling_slope_measured(csv_data_30_light_measured2,time_30_light_measured2) #, resample_bool=resample_bool)
flow_rate_light_measured3, time_light_measured3_filt = get_rolling_slope_measured(csv_data_30_light_measured3,time_30_light_measured3) #, resample_bool=resample_bool)



# ========================
# GET MSE
# ========================
for load_scaling_factor in range(60, 150, 5):
    load_scaling_factor = load_scaling_factor/100
    print(load_scaling_factor)
    flow_rate_light_measured1 = flow_rate_light_measured1[:-11]
    final_measured_1 = resample(flow_rate_light_measured1, len(flow_rate_light1))
    # final_measured_2 = resample(flow_rate_light_measured2, len(flow_rate_light2))
    final_measured_3 = resample(flow_rate_light_measured3, len(flow_rate_light3))
    final_measured_1 = np.around(final_measured_1, decimals=2)
    # final_measured_2 = np.around(final_measured_2, decimals=2)
    final_measured_3 = np.around(final_measured_3, decimals=2)

    final_sensor_1 = [val*load_scaling_factor for val in flow_rate_light1]
    # final_sensor_2 = [val*load_scaling_factor for val in flow_rate_light2][225:]
    final_sensor_3 = [val*load_scaling_factor for val in flow_rate_light3]
    # final_sensor_1 = flow_rate_light1
    # # final_sensor_2 = flow_rate_light2
    # final_sensor_3 = flow_rate_light3

    final_sensor_1 = np.around(final_sensor_1, decimals=2)
    # final_sensor_2 = np.around(final_sensor_2, decimals=2)
    final_sensor_3 = np.around(final_sensor_3, decimals=2)

    mse_ls = []
    mse_ls.append(mean_squared_error(final_measured_1, final_sensor_1))
    # mse_ls.append(mean_squared_error(final_measured_2, final_sensor_2))
    mse_ls.append(mean_squared_error(final_measured_3, final_sensor_3))


    print(f'MSE values: {mse_ls}')
    print(f'Average MSE: {np.mean(mse_ls)}')

    max_diff_ls = []
    max_diff_ls.append(max(abs(final_measured_1-final_sensor_1)))
    # max_diff_ls.append(max(abs(final_measured_2-final_sensor_2)))
    max_diff_ls.append(max(abs(final_measured_3-final_sensor_3)))

    print(f'Max diff: {max_diff_ls}')


# # ========================
# # PLOTTING
# # ========================

# fig, axs_2 = plt.subplots(3)
y_lim = [0,2]

plt.figure(figsize=(8, 5))
plt.subplot(211)
plt.plot(final_measured_1, label='measured (scale)')
plt.plot(final_sensor_1, label='load sensor')
plt.ylim(y_lim)
plt.legend()
plt.title(csv_name_30_light1)

# plt.subplot(312)
# plt.plot(final_measured_2, label='measured (scale)')
# plt.plot(final_sensor_2, label='load sensor')
# plt.ylim(y_lim)
# plt.legend()
# plt.title(csv_name_30_light2)

plt.subplot(212)
plt.plot(final_measured_3, label='measured (scale)')
plt.plot(final_sensor_3, label='load sensor')
plt.ylim(y_lim)
# plt.xlabel('Time (s)')
plt.legend()
plt.title(csv_name_30_light3)

plt.tight_layout()
plt.show(block=False)

print('---')