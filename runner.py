from __future__ import division
from VideoStreamPublisher.ReadVideoPublisher import VideoPublisher
from GlobalVariables import Config
from VideoStreamPublisher.ConfigurePublisher import ConfigurePublisher
from VideoAnalysis.AnalyseVideo import get_frame_distance
from VideoAnalysis.LivePlot import live_graph
from datetime import datetime
import queue
from time import sleep

publisher = ConfigurePublisher()
publisher.configureandstartpublisher()

# <----Start Window---->
#intialize_timewindow(1, 5)



# code for light weight process for

list = get_publisher_queue(0)

print(list)
pre_frame =[]
frame_count =1
batch_size =[]


while not list.empty():
    a = list.get()

    if not pre_frame:
        print("List frame empty")
        if(len(a)==2):
            pre_frame.append(a[1])
            Config.frame_arr.append(frame_count)
        else:
            pre_frame.append(a[0])
            Config.frame_arr.append(frame_count)

    else:
        if(len(a)==2):
            dist_val = get_frame_distance(pre_frame[0],a[1])
            Config.dist_arr.append(dist_val)
            Config.frame_arr.append(frame_count)
            #batch_size.append(1)
            #print("I frame batch Size:", len(batch_size))
            #batch_size.clear()
            #print("List Clear")
            pre_frame.clear()
            pre_frame.append(a[1])
        else:
            dist_val = get_frame_distance(pre_frame[0],a[0])
            Config.dist_arr.append(dist_val)
            Config.frame_arr.append(frame_count)
            batch_size.append(1)
            #print("List Clear")
            if(dist_val < 0.8):
                print("batch: ", len(batch_size) )
                #batch_size.clear()
                pre_frame.clear()
                pre_frame.append(a[0])
                #batch_size.append(1)

    frame_count +=1



    if(len(a)==2):
        print("I......")
        #cv2.imwrite('1.jpg',a)
        #cv2.imshow('frame',a[1])
        #cv2.waitKey(5000)

live_graph()