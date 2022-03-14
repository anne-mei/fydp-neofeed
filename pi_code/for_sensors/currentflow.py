from runSensor_PIGPIO import runSensor_PIGPIO
import time
flow_sensor = runSensor_PIGPIO()
flow_sensor.initialize_sensor()
flow_sensor.start_thread()
for i in range(500):
    print(flow_sensor.current_flow_rate)
    time.sleep(1)
flow_sensor.save_data()
flow_sensor.cleanAndExit()
flow_sensor.save_data()