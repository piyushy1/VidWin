# Author - Piyush Yadav
# Insight Centre for Data Analytics
# Package- VidWIN Project

from datetime import datetime
import queue
from GlobalVariables import Config

class TimeWindow:

    def __init__(self, publisher_id, time_stamp):
        self.publisher_id = publisher_id
        self.time_stamp = time_stamp


    # run time window
    def intialize_timewindow(self):
        intial_time = datetime.now()
        window_queue = queue.Queue(maxsize=0)
        temp_var =1
        #for frame in iter()
        while temp_var ==1:
            frame_val = Config.publisher_queue_map.get(self.publisher_id, "none")
            if frame_val:
                a = frame_val.get()
                window_queue.put(a)
                print(window_queue.qsize())

            # print("Time Window for Publisher: ", self.publisher_id," = ",window_queue.qsize())
            # if (datetime.now().total_seconds()-intial_time) >=self.time_stamp:
            #     print("Time Over to clear window")
            #     # CAUTION.... send all the value to your configurator and then only clear window
            #     # function to send value to configurator
            #     with window_queue.mutex:
            #         window_queue.queue.clear()
            #         print("Window Clear")



