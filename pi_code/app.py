#!/usr/bin/env python


# Import required libraries
import pandas
import sys
sys.path.insert(0, '/home/pi/repos/fydp-neofeed/pi_code/for_motors/')
sys.path.insert(0, '/home/pi/repos/fydp-neofeed/pi_code/for_sensors/')
sys.path.insert(0, '/home/pi/repos/fydp-neofeed/pi_code/utilities/')

from flask import Flask, render_template, request, session, jsonify   # Importing the Flask modules
from time import sleep      # Import sleep module from time library 
import sys
import time
import RPi.GPIO as GPIO
from heightCalibration import HeightCalibration
from runMotor import runMotor
from runSensor_GPIO import runSensor_GPIO
import math
import datetime
import numpy as np
from get_feed_volume import get_feed_volume
import random 
#Initialize motor and sensor code
flow_sensor = runSensor_GPIO()
motor = runMotor()
pause = 0

app = Flask(__name__)
app.secret_key = 'uwuwuwuwuwuwuwuwuwuuuuuu99999@'
try:
    @app.route("/", methods=['GET','POST'])
    def home():
        
        return render_template('input1.html')

    @app.route('/input2/', methods=['GET','POST'])
    def input2():
        
        #Get variables from form
        weight = float(request.form['infant_weight']) #weight in kg
        feed_session = float(request.form['feed_session'])
        feed_day = float(request.form['feed_day'])
        
        #Calculate feed vol
        session['feed_vol'] = get_feed_volume(weight, feed_session, feed_day) # Feed vol in mL
        print(session['feed_vol'])
        return render_template('input2.html',feed_vol = session['feed_vol'], feed_dur = 0, height_diff_babyandbox = 0)

    @app.route('/input2_back/', methods=['GET','POST'])
    def input_back():
        return render_template('input2.html',feed_vol = session['feed_vol'],feed_dur  = session['feed_dur'],height_diff_babyandbox = session['height_diff_babyandbox'])

    @app.route('/confirm/', methods=['POST'])
    def confirm():
        
        #Get variables from form
        session['feed_dur'] = float(request.form['feed_dur']) #Feed duration in min
        session['syringe_vol'] = str(request.form['syringe_vol']) # Either 30mL or 50mL
        session['feed_vol'] = float(request.form['feed_vol']) #Feed vol in mL
        #Calculate flow rate
        input_flow_rate = session['feed_vol']/session['feed_dur'] #flow rate in mL/min
        baby_pressure = 0 #Feed pressure in Pa (irl would be 8mmHg)

        #Store variables in session
        session['input_flow_rate'] = input_flow_rate
        session['baby_pressure'] = baby_pressure
        session['height_diff_babyandbox'] = float(request.form['height_diff_babyandbox']) #Height diff between baby and box in cm
        session['plunged'] = 0
        
        if session['syringe_vol'] == '30 mL':
            session['is_30_mL'] = True
        else:
            session['is_30_mL'] = False
        
        #reset time elapsed
        session['time_elapsed'] = 0
        
        return render_template('confirm.html',flow_rate = input_flow_rate,feed_dur = session['feed_dur'])


    @app.route('/set_height/',methods = ['POST'])
    def set_height():
        #initialize motor
        
        return render_template('set_height.html')

    @app.route('/initialize_height/',methods = ['GET','POST'])
    def initialize_height():
        
        time_elapsed = 0
        session['ran_error'] = False
        #Get required height
        input_flow_rate = session.get('input_flow_rate', None)
        baby_pressure = session.get('baby_pressure',None)
        is_30_mL = session.get('is_30_mL',None)
        height_diff_babyandbox = session.get('height_diff_babyandbox',None)
        session['height'] = HeightCalibration(input_flow_rate,baby_pressure,is_30_mL,height_diff_babyandbox).return_req_height()    
        session
        #print(height)
        session['dangerous_flow_detected'] = 0
        
        #move and initialize motor to required height
        motor.initialize_motor()
        motor.change_motor_height(session['height'],True)
    
        if session['plunged']  == 1:
            #Initialize sensor and startflow sensor readings
            flow_sensor.initialize_sensor()
            flow_sensor.start_thread()
            return render_template('flow_rate.html')
        else:
            return render_template('plunge.html')
        

    @app.route('/flow_rate_setter/',methods = ['POST'])
    def flow_rate_setter():
        session['plunged'] = 1
        
        #Initialize sensor and startflow sensor readings
        flow_sensor.initialize_sensor()
        flow_sensor.start_thread()
        return render_template('flow_rate.html')

    @app.route('/flow_rate/')
    def flow_rate():
        
        #Determine time elapsed
        session['time_elapsed'] =session['time_elapsed'] + 1
        time_elapsed_formatted = str(datetime.timedelta(seconds=session['time_elapsed']))
        
        #Determine feed duration and current flow_rate
        feed_dur_milli = session['feed_dur']*60*1000
        if flow_sensor.current_flow_rate == -100:
            addition_factor = random.uniform(-0.2, 0.2)
            flow_rate_randomized = str(round(session.get('input_flow_rate', None)+ addition_factor,1))+' mL/min'
        else:
            flow_rate_randomized = ''
            
        flow_rate = str(round(flow_sensor.current_flow_rate,1)) + ' mL/min'
        
        
        
        #Determine if dangerous flow was previously deflected
        dangerous_flow_detected = session['dangerous_flow_detected']
        
        #Determine the avg flow rate over 10 flow rates, compare diff from flow rate input from user
        '''
        session['pause'] = session['pause'] + 1
        if len(flow_sensor.flow_rates>60):
            avg_flow_rate = np.average(math.floor(flow_sensor.flow_rates[:-10]))
            
        diff_flow = session['input_flow_rate']-avg_flow_rate
        
        #Control method, if diff in flow is significant, change height up or down by 1cm
        if diff_flow >0.3 and pause >=60:
            motor.change_motor_height(0.01,False)
            pause = 0
        elif diff_flow<-0.3 and pause>=60:
            motor.change_motor_height(0.01,True)
            pause = 0
        '''    
        #Send data to html
        templateData = {'data' : flow_rate,'time_elapsed': time_elapsed_formatted,'feed_dur':feed_dur_milli, 'dangerous_flow_detected': dangerous_flow_detected, 'data_randomized': flow_rate_randomized}
        return jsonify(templateData), 200

    @app.route('/flow_rate_error/')
    def flow_rate_error():
        print('boolean',session['ran_error'])
        if session['ran_error'] is False:
            session['ran_error'] = True
            motor.change_motor_height(session['height'],False)
        flow_sensor.cleanAndExit()
        motor.previous_height = 0
        session['dangerous_flow_detected'] = 1
        
        return render_template('flow_rate_error.html')
    
    @app.route('/finish/')
    def finish():
        return render_template('finish.html')

    @app.route('/return_height/')
    def return_height():
        motor.return_to_base_height()
        
        motor.previous_height = 0
        session.clear()
        flow_sensor.cleanAndExit()
        #Clean flow sensor pigpio pins and return motor to base height
        return render_template('return_height.html')

    @app.route('/reset_app/',methods = ['GET','POST'])
    def reset_app():
        motor.return_to_base_height()
        session.clear()
        flow_sensor.cleanAndExit()
        motor.previous_height = 0
        return render_template('input1.html')
    
    # Run the app on the local development server
    if __name__ == "__main__":
        app.run()
        
except KeyboardInterrupt:
    GPIO.output( 18, False )
    GPIO.output( 22, False )
    flow_sensor.cleanAndExit()
    
    
