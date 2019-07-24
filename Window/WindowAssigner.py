# Author - Piyush Yadav
# Insight Centre for Data Analytics
# Package- VidWIN Project

import concurrent.futures
from GlobalVariables import Config
from Window.TimeWindow import  TimeWindow


class WindowAssigner:

    #default constructor
    def __init__(self, publisher_id, window_conf):
        self.publisher_id = publisher_id
        self.window_conf = window_conf


    def assign_window(self):
        print("test")
        # create a thread for time window
        with concurrent.futures.ThreadPoolExecutor(max_workers= 2) as executor:
            window = TimeWindow(self.publisher_id, self.window_conf)
            executor.submit(window.intialize_timewindow)






