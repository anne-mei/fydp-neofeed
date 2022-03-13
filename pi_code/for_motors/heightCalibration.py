import math
class HeightCalibration:
    def __init__(self,flow_rate,baby_pressure,is_30_mL,height_diff_babyandbox):
        '''Initialize fluid variables'''
        self.is_30_mL = is_30_mL
        self.rho = 1035           # density of milk (kg/m^3)
        self.g = 9.81             #acceleration due to gravity (m/s^2)
        self.l_total = 0.875       # total length of tube (m)
        self.mu = 0.00584     # viscosity of milk (Pa*s)
        self.h_full = 0.084        #height of fluid in syringe (m)
        self.p0 = 0                # atmospheric gauge pressure  (Pa)
        self.p1 = self.p0 + self.rho*self.g*self.h_full  #gauge pressure due to liquid in syringe (Pa)

        if self.is_30_mL:
            self.h_full = 0.084        #height of fluid in syringe (m)
            self.k_bends = 0.0001      #degree of bends
        else:
            self.h_full = 0.084        
            self.k_bends = 8000

        self.d = 0.0011    # internal tube diameter for 5 French (m)
        self.flow_rate_conversion = 1/60000000 #Conversion factor from mL/min->m^3/s
        self.flow_rate = flow_rate*self.flow_rate_conversion
        self.baby_pressure = baby_pressure
        self.height_diff_babyandbox = height_diff_babyandbox*(1/100) #height diff between baby and box in m
    def flowrate_to_velocity(self):
        '''
        Converts flow rate (ml/min) to velocity (m/s)
        OUTPUT:
            v2 (float): Velocity in m/s
        '''
        v2 = self.flow_rate / (math.pi * (self.d / 2) ** 2) 
        return v2    
    

    def get_headloss_friction(self,velocity):
        '''
        Calculates the headloss friction from both bend and tubing
        OUTPUT:
           hf (float): Headloss friction from bends and tubing 
        '''
        f = ((self.d*self.mu*16*math.pi)/(4*(self.flow_rate)*self.rho))
        k_tubing = 4*f*self.l_total/self.d
        kf = k_tubing + self.k_bends 
        hf = (kf/2) *(velocity)**2
        return hf

    def get_height(self,velocity,headloss_friction):
        '''
        Calculates the height required to achieve desired flow rate
        OUTPUT:
           h (float): Desired height (m)
        '''
        h = ((self.baby_pressure-self.p1)/self.rho + (velocity**2)/2 + headloss_friction)/self.g
        return h
    
    def return_req_height(self):
        '''Returns required height
        OUTPUT:
            height (float): Desired height that motor must be set to (mm)

        '''

        velocity = self.flowrate_to_velocity()
        headloss_friction = self.get_headloss_friction(velocity)
        height = self.get_height(velocity,headloss_friction)

        if self.is_30_mL:
            height_syringe = 0.107
            height_motor = height-self.height_diff_babyandbox-height_syringe
        else:
            height_syringe = 0.13
            height_motor = height-self.height_diff_babyandbox-height_syringe
        return height_motor
