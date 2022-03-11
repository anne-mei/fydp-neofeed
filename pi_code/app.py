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
from Motors import runMotor
from runSensor import runSensor

#Initialize motor and sensor code
flow_sensor = runSensor()
flow_sensor.initialize_sensor()
#motor = runMotor()
#motor.initialize_motor()

app = Flask(__name__)
app.secret_key = 'uwuwuwuwuwuwuwuwuwuuuuuu99999@'

@app.route("/", methods=['GET','POST'])
def home():                                                                                                                                                         
    return render_template('landing.html')

@app.route('/confirm/', methods=['POST'])
def confirm():
    
    #Initialize variables
    feed_vol = float(request.form['feed_vol']) # Feed vol in mL
    feed_dur = float(request.form['feed_dur']) #Feed duration in min
    
    session['feed_vol'] = feed_vol
    session['feed_dur'] = feed_dur
    
    
    flow_rate = feed_vol/feed_dur #flow rate in mL/min
    baby_pressure = 0#Feed pressure in Pa
    
    
    session['flow_rate'] = flow_rate
    session['baby_pressure'] = baby_pressure
    
    return render_template('confirm.html',flow_rate = flow_rate,feed_dur = feed_dur)
    #return render_template_string(confirm,flow_rate = flow_rate)

@app.route('/set_height/',methods = ['POST'])
def set_height():
    return render_template('set_height.html')

@app.route('/initialize_height/')
def initialize_height():
    
    #Get required height
    #flow_rate = session.get('flow_rate', None)
    #baby_pressure = session.get('baby_pressure',None)
    #height = HeightCalibration(flow_rate,baby_pressure).return_req_height()
    
    #move motor to required height
    #height_changed = motor.change_motor_height(height,True)
    flow_sensor.start_thread()
    return render_template('flow_rate.html')


@app.route('/flow_rate/')
def flow_rate():
    flow_rate = flow_sensor.current_flow_rate
    templateData = {'data' : flow_rate}
    return jsonify(templateData), 200


#@app.route('/finish/')
#def finish():
#return render_template('finish.html')

@app.route('/return_height/')
def return_height():
    #motor.return_to_base_height()
    time.sleep(5)
    return render_template('return_height.html')
# Run the app on the local development server
if __name__ == "__main__":
    app.run()
    
    
    
