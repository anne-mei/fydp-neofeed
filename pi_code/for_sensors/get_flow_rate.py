from scipy import stats
import math


WINDOW_WIDTH_RAW = 10
WINDOW_WIDTH_FLOWRATE = 25
DATAPNT_DELAY = 899
FPS = 1000 / DATAPNT_DELAY

# def butter_filter(data, cutoff, order, fs):
#     nyq = 0.5 * fs
#     normal_cutoff = cutoff / nyq
#     b, a = butter(order, normal_cutoff)  # , btype='low', analog=False
# #     b, a = butter(3, 0.1)
#     y = filtfilt(b, a, data)
#     return y

# pass in a window of raw sensor data, and window of flow_rate
def get_flow_rate(sensor_data, flow_rate_sig):
    x =list(range(len(sensor_data)))
    curr_slope, _, _, _, _ = stats.linregress(x, sensor_data)
    
    # Convert sensor data to flow rate
    syringe_rad = 21.7/2  # Syringe radius in mm
    syringe_area = math.pi * (syringe_rad ** 2)
    density = 1 # in g/mL
    curr_flowrate = (1 / density) * curr_slope * 60 * FPS * (-1)  # convert from g/s to mL/min

    flow_rate_sig.append(curr_flowrate)


    if len(flow_rate_sig) > (WINDOW_WIDTH_RAW + WINDOW_WIDTH_FLOWRATE) * FPS:
        curr_start = int(-WINDOW_WIDTH_FLOWRATE * FPS)
        curr_window_flowrate_sig = flow_rate_sig[curr_start:]
        curr_flowrate_val = stats.trim_mean(curr_window_flowrate_sig, 0.3)
        
        # load sensor calibration
        calibration_factor = 1.2
        curr_flowrate_val = round(calibration_factor * curr_flowrate_val, 2)
        
    else:
        curr_flowrate_val = -100

    return curr_flowrate_val, flow_rate_sig
