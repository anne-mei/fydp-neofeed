#!/usr/bin/env python


# Import required libraries
import sys
sys.path.insert(0, '/home/pi/repos/fydp-neofeed/pi_code/for_motors/')
sys.path.insert(0, '/home/pi/repos/fydp-neofeed/pi_code/for_sensors/')
from flask import Flask, render_template, request, session, jsonify   # Importing the Flask modules
from time import sleep      # Import sleep module from time library 
import sys
import time
import RPi.GPIO as GPIO
from heightCalibration import HeightCalibration
from runMotor import runMotor
from runSensor_PIGPIO import runSensor_PIGPIO
import datetime

#Initialize motor and sensor code
flow_sensor = runSensor()
flow_sensor.initialize_sensor()
motor = runMotor()
motor.initialize_motor()
pause = 0

app = Flask(__name__)
app.secret_key = 'uwuwuwuwuwuwuwuwuwuuuuuu99999@'

@app.route("/", methods=['GET','POST'])
def home():                                                                                                                                                         
    return render_template('landing.html')

@app.route('/confirm/', methods=['POST'])
def confirm():
    #Initialize variables and store them in session
    feed_vol = float(request.form['feed_vol']) # Feed vol in mL
    feed_dur = float(request.form['feed_dur']) #Feed duration in min
    session['feed_vol'] = feed_vol
    session['feed_dur'] = feed_dur
    
    #Get flow rate and baby pressure and store them in session
    flow_rate = feed_vol/feed_dur #flow rate in mL/min
    baby_pressure = 0#Feed pressure in Pa
    session['input_flow_rate'] = flow_rate
    session['baby_pressure'] = baby_pressure
    session['time_elapsed'] = 0
    
    return render_template('confirm.html',flow_rate = flow_rate,feed_dur = feed_dur)

@app.route('/set_height/',methods = ['POST'])
def set_height():
    return render_template('set_height.html')

@app.route('/initialize_height/')
def initialize_height():
    
    #start flow sensor readings
    flow_sensor.start_thread()
    time_elapsed = 0
    
    #Get required height
    flow_rate = session.get('input_flow_rate', None)
    baby_pressure = session.get('baby_pressure',None)
    height = HeightCalibration(flow_rate,baby_pressure).return_req_height()
    
    #move motor to required height
    motor.change_motor_height(height,True)

    return render_template('flow_rate.html')


@app.route('/flow_rate/')
def flow_rate():
    #Determine time elapsed
    time = session['time_elapsed']
    session['time_elapsed'] =time + 1
    time_elapsed_formatted = str(datetime.timedelta(seconds=session['time_elapsed']))
    
    #Determine feed duration and current flow_rate
    feed_dur_milli = session['feed_dur']*60*1000
    flow_rate = flow_sensor.current_flow_rate
    
    #Determine the avg flow rate over 10 flow rates, compare diff from flow rate input from user
    pause = pause + 1
    if len(flow_sensor.flow_rates>60):
        avg_flow_rate = np.average(floor(flow_sensor.flow_rates[:-10]))
        
    diff_flow = session['input_flow_rate']-avg_flow_rate
    
    #Control method, if diff in flow is significant, change height up or down by 1cm
    if diff_flow >0.3 and pause >=60:
        motor.change_motor_height(0.01,False)
        pause = 0
    else if diff_flow<-0.3 and pause>=60:
        motor.change_motor_height(0.01,True)
        pause = 0
        
    #Send data to html
    templateData = {'data' : flow_rate,'time_elapsed': time_elapsed_formatted,'feed_dur':feed_dur_milli}
    print(flow_sensor.thread.is_alive())
    return jsonify(templateData), 200

@app.route('/finish/')
def finish():
    pause = 0
    return render_template('finish.html')

@app.route('/return_height/')
def return_height():
    
    #Clean flow sensor pigpio pins and return motor to base height
    flow_sensor.cleanAndExit()
    motor.return_to_base_height()
    return render_template('return_height.html')

# Run the app on the local development server
if __name__ == "__main__":
    app.run()
    
    
    
