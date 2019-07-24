# Author - Piyush Yadav
# Insight Centre for Data Analytics
# Package- VidWIN Project

import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time
from GlobalVariables import Config

xs =[]
ys =[]
fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)

def animate(i,xs,ys):
    # pullData = open("sampleText.txt","r").read()
    # dataArray = pullData.split('\n')
    print(len(Config.frame_arr))
    xs = Config.frame_arr[:]
    #print("Farema array size",len(xs), len(frame_arr))
    ys = Config.dist_arr[:]
    # for eachLine in dataArray:
    #     if len(eachLine)>1:
    #         x,y = eachLine.split(',')
    #         xar.append(int(x))
    #         yar.append(int(y))
    ax1.clear()
    ax1.plot(xs,ys)


def live_graph():
    ani = animation.FuncAnimation(fig, animate,fargs=(xs, ys), interval=1000)
    plt.show()