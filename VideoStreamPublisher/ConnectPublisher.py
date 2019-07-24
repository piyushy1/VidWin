# Author - Piyush Yadav
# Insight Centre for Data Analytics
# Package- VidWIN Project

# this class connects to the publisher and add frame value to the publisher queue
from GlobalVariables import Config
import queue
from VideoStreamPublisher.ReadVideoPublisher import VideoPublisher
import cv2
from Window.WindowAssigner import WindowAssigner
from QueryBuilder.QueryParser import read_query

class ConnectPublisher:

    def __init__(self, publisher_path, publisher_id):
        self.publisher_path = publisher_path
        self.publisher_id = publisher_id


    def test_publisher(self,a):
        print(a)

    #function to connect to the publisher
    def connect_publisher_source(self):
        #print("The publsisher path..........."+ self.publisher_path)
        # create publisher queue for each publisherl
        publisher_queue = queue.Queue(maxsize=0)
        # add the queue to the publisher queue map
        Config.publisher_queue_map.update({self.publisher_id: publisher_queue})

        #code for windowing
        #need to be handled here... presently not implemented
        # window_time = read_query()
        # window = WindowAssigner(self.publisher_id,window_time)
        # window.assign_window

        # start video publisher

        video_publisher = VideoPublisher(publisher_queue,self.publisher_id, self.publisher_path)
        video_publisher.load_video()



