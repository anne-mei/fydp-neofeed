from runSensor_GPIO import runSensor_GPIO
import time
flow_sensor = runSensor_GPIO()
flow_sensor.initialize_sensor()
flow_sensor.return_flow_rate()
#flow_sensor.start_thread()
#for i in range(500):
#    print(flow_sensor.current_flow_rate)
#   print(flow_sensor.thread.is_alive())
#    time.sleep(1)
flow_sensor.save_data()
flow_sensor.cleanAndExit()