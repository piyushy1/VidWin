# Author - Piyush Yadav
# Insight Centre for Data Analytics
# Package- VidWIN Project

# This is the main class file to run the code
from __future__ import division
from VideoStreamPublisher.ReadVideoPublisher import VideoPublisher
from GlobalVariables import Config
from VideoStreamPublisher.ConfigurePublisher import ConfigurePublisher
from VideoAnalysis.AnalyseVideo import get_frame_distance
from VideoAnalysis.LivePlot import live_graph
from datetime import datetime
import queue
from time import sleep


# get all items from thread queue
def get_all_queue_result(queue):

    result_list = []
    while not queue.empty():
        result_list.append(queue.get())

    return result_list



# get the list of publisher queue
def get_publisher_queue(publisher_id):
    #create window
    print(Config.publisher_queue_map.items())
    publisher_queue = Config.publisher_queue_map.get(publisher_id, "none")
    return publisher_queue



# run time window
def intialize_timewindow(publisher_id, time_duration):
    publisher_queue = get_publisher_queue(publisher_id) # here 1 is publisher id
    intial_time = datetime.now()
    window_queue = queue.Queue(maxsize=0)
    for frame in iter(publisher_queue.get, None):
        sleep(1/29) # sleeping with respect to frame per second
        window_queue.put(frame)
        #print("Window Queueu Size",window_queue.qsize())
        time_diff = datetime.now()-intial_time
        print(time_diff.total_seconds())
        if (time_diff.total_seconds()) >= time_duration:
            intial_time = datetime.now()
            print("Time Over to clear window")
            print("Window Queueu Size",window_queue.qsize())
            # CAUTION.... send all the value to your configurator and then only clear window
            # function to send value to configurator
            with window_queue.mutex:
                window_queue.queue.clear()
                print("Window Clear")




if __name__== "__main__":

    # create subscriber query map to read the VEQL query

    # <----Configure and start Publisher---->
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




