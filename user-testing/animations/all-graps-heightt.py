#Importing required libraries
#%matplotlib notebook
import matplotlib.pyplot as plt
import numpy as np
from celluloid import Camera
import ffmpeg
from matplotlib.animation import FuncAnimation, PillowWriter 

 
 
#Creating Data
y_5fr = np.linspace(34.28, 41.28, 100)
y_6fr = np.linspace(27.89, 34.89, 100)
fluid_lvl = np.linspace(0,7,100)
x = np.ones(150)*5


fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(10, 5))
#plt.xlim(4,6)
#plt.ylim(0,2)
camera = Camera(fig)
x_fluid = []
#Looping the data and capturing frame at each iteration
for i in range(len(y_5fr)):
    ax[0].bar(['Fluid Level'], [7-fluid_lvl[i]], 0.5, label='Men',color =  [(226/256,220/256,205/256)])
    ax[0].bar(['Fluid Level'], [fluid_lvl[i]], 0.5, bottom=[7-fluid_lvl[i]],label='Women',color = [(169/256,169/256,169/256)])
    # ax[0].set_ylabel('Syringe Fluid Level (cm)')

    a = ax[1].scatter([5],[34.28],color = 'red',s = 25)
    b = ax[1].scatter([5],[41.28],color = 'red',s = 25)
    c = ax[1].scatter(x[i], y_5fr[i] , color = 'green' ,marker = "s", s = 200)
    ax[1].plot([5,5],[0,45] , color = 'grey' , lw = 3)
    ax[1].set_ylim(25,45)
    ax[1].set_xlabel('5 Fr')
    ax[1].get_xaxis().set_ticks([])
    ax[1].get_yaxis().set_visible(False)

    # a = ax[2].scatter([5],[27.89],color = 'red',s = 25)
    # b = ax[2].scatter([5],[34.89],color = 'red',s = 25)
    # c = ax[2].scatter(x[i], y_6fr[i] , color = 'blue' ,marker = "s", s = 200)
    # ax[2].plot([5,5],[0,45] , color = 'grey' , lw = 3)
    # ax[2].set_ylim(25,45)
    # ax[2].set_xlabel('6 Fr')
    # ax[2].get_xaxis().set_ticks([])
    # ax[2].get_yaxis().set_visible(False)

    # x_fluid.append(7-fluid_lvl[i]) 
    # ax[3].plot(x_fluid,y_5fr[0:(i+1)],color = 'green')
    # ax[3].plot(x_fluid,y_6fr[0:(i+1)], color = 'blue')
    # ax[3].set_ylim(25,45)
    # ax[3].set_xlim(7,0)
    # ax[3].yaxis.tick_right()
    # ax[3].yaxis.set_label_position("right")
    # ax[3].set_xlabel('Syringe Fluid Level (cm)')
    # ax[3].set_ylabel('Height Above Baby (cm)')
    # ax[3].grid(linestyle="--")
    #ax[0].title('tracing a sin function')

    
    #plt.show()

    camera.snap()



 
#Creating the animation from captured frames
animation = camera.animate(interval = 200, repeat = True,
                           repeat_delay = 500)
animation.save(r'C:\Users\rachj\Documents\GitHub\fydp-neofeed\user-testing\coil.gif',writer='imagemagick') 
# fig, ax = plt.subplots()
# ax.scatter
# def animate_height(i):
#     line
# x = [7,3.75,0]
# Fr_5 = [0.3428,0.3778,0.4128]
# Fr_6 = [0.2789,0.3139,0.3489]
# plt.plot(x,Fr_5)
# plt.plot(x,Fr_6)
# plt.show()
# v =21.355/1000
# d = 1.37/1000
# #d = 1.11/1000

# flow = ((d**2)/4)*math.pi*v
# flow = flow*60/(10**(-6))
# print(flow)