#!/usr/bin/env python


# Import required libraries
import pandas
import sys
from pygame import mixer
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

#Initialize music
mixer.init()
mixer.music.load('/home/pi/repos/fydp-neofeed/pi_code/nurse_alarm.mp3')

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
        
        
        
        #instantiate weight_errors
        weight_error = ''
        feed_session_error = ''
        feed_day_error = ''
        
        input1_error = False
        max_feed_session = 0
        max_feed_day = 0
        
        #Check if input is correct
        
        if weight>=0.4 and weight<0.6:
            max_feed_session = 12
            max_feed_day = 7
        elif weight>=0.6 and weight<1.25:
            max_feed_session = 12
            max_feed_day = 6
        elif weight>=1.25 and weight<=2.25:
            max_feed_session = 8
            max_feed_day = 5
        else:
            weight_error = ' Please enter a weight between 0.4kg and 2.25kg'
            input1_error = True
        
        if feed_session>max_feed_session or feed_session<1:
            feed_session_error = 'Please enter a feed session number between 1 and ' + str(max_feed_session)
            input1_error = True
        if feed_day>max_feed_day or feed_day<1:
            feed_day_error = 'Please enter a feed day number between 1 and ' + str(max_feed_day)
            input1_error = True
        
        if input1_error:
            return render_template('errors_input1.html',weight_error = weight_error, feed_session_error = feed_session_error, feed_day_error = feed_day_error)
        else:
            #Calculate feed vol
            session['feed_vol'] = get_feed_volume(weight, feed_session, feed_day) # Feed vol in mL
            print(session['feed_vol'])
            return render_template('input2.html',feed_vol = session['feed_vol'], feed_dur = 1, height_diff_babyandbox = 0)

    @app.route('/input2_back/', methods=['GET','POST'])
    def input2_back():
        mixer.music.stop()
        return render_template('input2.html',feed_vol = session['feed_vol'],feed_dur  = session['feed_dur'])#,height_diff_babyandbox = session['height_diff_babyandbox'])

    @app.route('/confirm/', methods=['POST'])
    def confirm():
        #Get variables from form
        session['feed_dur'] = float(request.form['feed_dur']) #Feed duration in min
        session['syringe_vol'] = str(request.form['syringe_vol']) # Either 30mL or 50mL
        session['feed_vol'] = float(request.form['feed_vol']) #Feed vol in mL
        
        #Calculate flow rate
        input_flow_rate = round(session['feed_vol']/session['feed_dur'],2) #flow rate in mL/min
        session['input_flow_rate'] = input_flow_rate
        baby_pressure = 0 #Feed pressure in Pa (irl would be 8mmHg)
        #session['height_diff_babyandbox']= float(request.form['height_diff_babyandbox']) #Height diff between baby and box in cm

        #Store variables in session
        #session['input_flow_rate'] = input_flow_rate
        #session['baby_pressure'] = baby_pressure
        session['height_diff_babyandbox'] = float(request.form['height_diff_babyandbox']) #Height diff between baby and box in cm
        session['plunged'] = 0
        session['dangerous_flow_detected'] = 0
        
        
            
        if session['syringe_vol'] == '30 mL':
            is_30_mL = True
        else:
            is_30_mL = False
        
        #Check for errors on page
        input_flow_rate_error = ''
        #height_diff_babyandbox_error = ''
        input_2_error = False
        
        if input_flow_rate>2 or input_flow_rate<0:
            input_2_error = True
            input_flow_rate_error = 'Please ensure flow rate is below 2mL/min'
            return render_template('errors_input2.html',input2_error_msg = input_flow_rate_error)
        
        session['height'] = HeightCalibration(input_flow_rate,baby_pressure,is_30_mL,session['height_diff_babyandbox']).return_req_height()
        
        
        if session['height']<0:
            input_2_error = True
            change_height_required = round(session['height_diff_babyandbox']+session['height']*(100))
            height_diff_babyandbox_error = 'Please adjust so the height between the baby and device is at most '+str(change_height_required) + ' cm'
            return render_template('errors_input2.html',input2_error_msg = height_diff_babyandbox_error)
        
        
        if input_2_error is False:
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
        #input_flow_rate = session.get('input_flow_rate', None)
        #baby_pressure = session.get('baby_pressure',None)
        #is_30_mL = session.get('is_30_mL',None)
        #height_diff_babyandbox = session.get('height_diff_babyandbox',None)
        #session['height'] = HeightCalibration(input_flow_rate,baby_pressure,is_30_mL,height_diff_babyandbox).return_req_height()    
        
        #stop music if playing
        mixer.music.stop()
        
        #move and initialize motor to required height
        motor.initialize_motor()
        motor.change_motor_height(session['height'],True)
        
        #restart flow rate var
        session['first_flow_rate']  = 1
    
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
        session['pause'] = 0
        session['changing_height'] = False
        session['time'] = 0
        session['large_diff_counter'] = 0
        #Initialize sensor and startflow sensor readings
        flow_sensor.initialize_sensor()
        flow_sensor.start_thread()
        return render_template('flow_rate.html')

    @app.route('/flow_rate/')
    def flow_rate():
        #Determine time elapsed
        session['time_elapsed'] =session['time_elapsed'] + 1
        time_elapsed_formatted = str(datetime.timedelta(seconds=session['time_elapsed']))
        changing_height = False
        time = 0
        #Determine feed duration and current flow_rate
        feed_dur_milli = session['feed_dur']*60*1000
        flow_rate = str(round(flow_sensor.current_flow_rate,1)) + ' mL/min'
        print('processed fl',flow_rate)
        if session['first_flow_rate'] == 1:
            flow_rate = '-100 mL/min'
            session['first_flow_rate'] = 0
        
        
        if flow_rate == '-100 mL/min':
            addition_factor = random.uniform(-0.2, 0.2)
            if session.get('input_flow_rate',None) is None:
                flow_rate_randomized = str(round(addition_factor,1))+' mL/min'
            else:
                flow_rate_randomized = str(round(session.get('input_flow_rate', None)+ addition_factor,1))+' mL/min'
        else:
            flow_rate_randomized = ''
        
        
        
        #Determine if dangerous flow was previously deflected
        dangerous_flow_detected = session['dangerous_flow_detected']
        
        #Determine the avg flow rate over 10 flow rates, compare diff from flow rate input from user
        
        diff = abs(flow_sensor.flow_rates_converted[-2] - flow_sensor.current_flow_rate)
        
        if session['large_diff_counter'] >0:
            session['large_diff_counter'] =  session['large_diff_counter'] + 1
            
        if diff> 0.3 and session['large_diff_counter'] == 0:
            session['large_diff_counter'] = session['large_diff_counter'] + 1
            session['pause'] = session['pause'] - 30
            
        if session['large_diff_counter'] >30:
            session['large_diff_counter'] = 0
            
        session['pause'] = session['pause'] + 1
        
        if len(flow_sensor.flow_rates_converted)>60:
            print (flow_sensor.flow_rates_converted[-20:-1])
            avg_flow_rate = round(np.average(flow_sensor.flow_rates_converted[-20:-1]),1)
            print('avg_flow_rate',avg_flow_rate)
            print('input_flow_rate',session['input_flow_rate'])
            diff_flow = session['input_flow_rate']-avg_flow_rate
            print('diff_flow',diff_flow)
            #Control method, if diff in flow is significant, change height up or down by 1cm
            if diff_flow >0.15 and session['pause'] >=90:
                session['pause'] = 0
                motor.change_motor_height(0.045,True)
                session['changing_height'] = True
            elif diff_flow<-0.15 and session['pause']>=90:
                session['pause'] = 0
                motor.change_motor_height(0.045,False)
                session['changing_height'] = True
                
        if session['changing_height'] is True and session['time'] < 5:
            session['time'] = session['time'] + 1
            templateData = {'data' : 'Height Changing','time_elapsed': time_elapsed_formatted,'feed_dur':feed_dur_milli, 'dangerous_flow_detected': dangerous_flow_detected, 'data_randomized': flow_rate_randomized}
        
        elif session['changing_height'] is True and session['time'] >= 5 and session['time'] < 20:
            session['time'] = session['time'] + 1
            templateData = {'data' : 'Processing...','time_elapsed': time_elapsed_formatted,'feed_dur':feed_dur_milli, 'dangerous_flow_detected': dangerous_flow_detected, 'data_randomized': flow_rate_randomized}
        else:
            session['changing_height'] = False
            session['time'] = 0
            #Send data to html
            templateData = {'data' : flow_rate,'time_elapsed': time_elapsed_formatted,'feed_dur':feed_dur_milli, 'dangerous_flow_detected': dangerous_flow_detected, 'data_randomized': flow_rate_randomized}
        return jsonify(templateData), 200
    
    @app.route('/return_to_base_error/')
    def return_to_base_error():
        return render_template('return_to_base_error.html')   

    @app.route('/flow_rate_error/')
    def flow_rate_error():
        if session['ran_error'] is False:
            mixer.music.play(-1)
            #time.sleep(5)
            session['ran_error'] = True
            motor.return_to_base_height()
            motor.previous_height = 0
            flow_sensor.cleanAndExit()
            session['dangerous_flow_detected'] = 1
            return render_template('flow_rate_error.html')
    
    
    @app.route('/finish/')
    def finish():
        return render_template('finish.html')

    @app.route('/return_height/')
    def return_height():
        
        #Clean flow sensor pins and return motor to base height
        motor.return_to_base_height()
        motor.previous_height = 0
        session.clear()
        flow_sensor.cleanAndExit()
        
        return render_template('return_height.html')
    
    @app.route('/return_to_base_reset/')
    def return_to_base_reset():
        return render_template('return_to_base_reset.html')
                               
    @app.route('/reset_app/',methods = ['GET','POST'])
    def reset_app():
        
        #Clean flow sensor pins and return motor to base height
        motor.return_to_base_height()
        motor.previous_height = 0
        session.clear()
        flow_sensor.cleanAndExit()
        
        return render_template('input1.html')
    
    # Run the app on the local development server
    if __name__ == "__main__":
        app.run(threaded = True)
        
except KeyboardInterrupt:
    GPIO.output( 18, False )
    GPIO.output( 22, False )
    flow_sensor.cleanAndExit()
    
    
