import math
#assumtions:
    #assume laminar flow (Nre < 2000)
    #assume alpha = 1 (velocity profile at max)
    #assume v1 = 0 (very small flow at the start)
    #assume 1 bend for an empty bag

# variables:
g = 9.81              # gravity (m/s^2)
q1 = 0                # initial flow rate from bag (m^3/s)
q2 = 3.3333 * 10**-8  # flow rate going into baby(m^3/s)
d_5French = 0.0011    # internal tube diameter for 5 French (m)
d_6French = 0.00137   # internal tube diameter for 6 French (m)
rho = 1000            # density of milk (kg/m^3)
l_total = 0.875       # total length of tube (m)
mu = 0.003254           # viscosity of milk (Pa*s)
h_full = 0.084        #height of fluid in syringe (m)
h_half_full = 0.042   # height of half fluid in syringe (m)
p0 = 0                # atmospheric gauge pressure 
p1_full = p0 + rho*g*h_full
p1_half_full = p0 + rho*g*h_half_full
h_diff = 0.3          #Height between top of syringe and bottom of tube -----> CHANGE
p2 = rho*g*h_diff # pressure in baby's stomach (Pa)
k_ent = 0.4           # entering loss from syringe
k_bend_90deg = 0.15   # loss from the tube bend at 90 degree                     CHANGE TO 150 degrees!!!!
k_bend_45deg = 0.08   # loss from the tube bend at 45 degree

def get_velocity_into_baby(d):
    v2 = q2 / (math.pi * (d / 2) ** 2)  # velocity into baby's stomach (m/s)
    return v2

def get_headloss_friction(v2,k_bend,d):
    f = ((d*mu*16*math.pi)/(4*(q2/2)*rho))
    kpipe = 4*f*l_total/d
    kf = kpipe + k_bend + k_ent
    hf = (kf/2) *(v2/2)**2
    return hf

def get_height(hf,p1,d):
    h = ((p2-p1)/rho + (get_velocity_into_baby(d)**2)/2 + hf)/g
    return h

if __name__ == '__main__':
    #v2 = get_velocity_into_baby();

#SOLVE FOR 5 FRENCH:
    print('\nSolved Heights for 5 French Tubing:')
    #CASE 1: 1 Bend at mouth (90 degrees) (bag is empty)
    hf1 = get_headloss_friction(get_velocity_into_baby(d_5French), k_bend_90deg,d_5French)
    h_empty = get_height(hf1, 0,d_5French)
    print('The height for an empty bag of feed should be', round(h_empty, 4), 'm above the baby\'s stomach')

    #CASE 2: 2 Bends, one at mouth (90 degrees), one at 45 degree (bag is half empty)
    hf2 = get_headloss_friction(get_velocity_into_baby(d_5French), k_bend_90deg + k_bend_45deg,d_5French)
    h_semifull = get_height(hf2,p1_half_full,d_5French)
    print('The height for a semi-full bag of feed should be', round(h_semifull, 4),'m above the baby\'s stomach')

    #CASE 3: 2 Bends, one at mouth (90 degrees), one at 90 degree (bag is full)
    hf3 = get_headloss_friction(get_velocity_into_baby(d_5French), k_bend_90deg + k_bend_90deg,d_5French)
    h_fullbag = get_height(hf3, p1_full,d_5French)
    print('The height for a full bag of feed should be', round(h_fullbag, 4), 'm above the baby\'s stomach')

#SOLVE FOR 6.5 FRENCH:
    # print('\nSolved Heights for 6 French Tubing:')
    # # CASE 1: 1 Bend at mouth (90 degrees) (bag is empty)
    # hf1 = get_headloss_friction(get_velocity_into_baby(d_6French), k_bend_90deg, d_6French);
    # h_empty = get_height(hf1, 0, d_6French);
    # print('The height for an empty bag of feed should be', round(h_empty, 4), 'm above the baby\'s stomach')

    # #CASE 2: 2 Bends, one at mouth (90 degrees), one at 45 degree (bag is half empty)
    # hf2 = get_headloss_friction(get_velocity_into_baby(d_6French), k_bend_90deg + k_bend_45deg,d_6French);
    # h_semifull = get_height(hf2,p1_half_full,d_6French);
    # print('The height for a semi-full bag of feed should be', round(h_semifull, 4),'m above the baby\'s stomach')

    # #CASE 3: 2 Bends, one at mouth (90 degrees), one at 90 degree (bag is full)
    # hf3 = get_headloss_friction(get_velocity_into_baby(d_6French), k_bend_90deg + k_bend_90deg,d_6French);
    # h_fullbag = get_height(hf3, p1_full,d_6French);
    # print('The height for a full bag of feed should be', round(h_fullbag, 4), 'm above the baby\'s stomach')










