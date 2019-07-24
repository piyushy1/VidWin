# Author - Piyush Yadav
# Insight Centre for Data Analytics
# Package- VidWIN Project

# function to read video...
from __future__ import division
import numpy as np
import cv2
import queue
from GlobalVariables import Config
from VideoAnalysis.AnalyseVideo import get_frame_types
from datetime import datetime
from Window.WindowAssigner import WindowAssigner
from QueryBuilder.QueryParser import  read_query
from time import sleep



class VideoPublisher:

    #intialise video publisher
    def __init__(self, publisher_queue,publisher_id,publisher_path):
        self.publisher_queue = publisher_queue
        self.publisher_id = publisher_id
        self.publisher_path =  publisher_path


    #load the video publisher
    def load_video(self):

        # read the video file
        cap = cv2.VideoCapture(self.publisher_path)

        # read the fps so that opencv read with same fps speed
        fps = cap.get(cv2.CAP_PROP_FPS)
        print("FPS for video: ",self.publisher_id, " : ", fps )
        # time to sleep the process
        sleep_time = 1/(fps+2) # 2 is added to make the reading frame time and video time equivalnet. this is an empirical value may change for others.
        print("Sleep Time : ", sleep_time )
        # to check the frame count
        frame_count_num = cap.get(cv2.CAP_PROP_FRAME_COUNT)
        print('Frame COUNT: ',frame_count_num)
        duration = frame_count_num/fps
        print("Duration of video ", self.publisher_id, " ", duration%60)


        print("Video Publisher initiated==" + str(self.publisher_id))

        # attach the frame probe:
        # to be correct this is not a relat streaming scenario. this is just a way around. need to create a pipe function from
        #ffmpeg to read frame by frame and attach each frame info

        frame_types = get_frame_types(self.publisher_path,self.publisher_id)
        i_frames = [x[0] for x in frame_types if x[1]=='I']
        print(i_frames)
        frame_count =0
        dt1 = datetime.now()

        #add the windowing concept here...
        # get the time from query : presently only one query

        # window_time = read_query()
        # window = WindowAssigner(self.publisher_id,window_time)
        # window.assign_window()

        # process video
        while(True):
            # Capture frame-by-frame

            frame_info_list = []
            ret, frame = cap.read()
            if not ret:
                break

            frame = cv2.resize(frame, (400, 600))
            # need to set the frame rate:
            if frame_count in i_frames:
                frame_info_list.append("I")
                frame_info_list.append(frame)
                self.publisher_queue.put(frame_info_list)
                print("i-frame : "+ str(frame_count))

            else:
                frame_info_list.append(frame)
                self.publisher_queue.put(frame_info_list)

            #sleep(sleep_time)
            frame_count += 1
            # Our operations on the frame come here
            #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            # Display the resulting frame
            #cv2.imshow(str(self.publisher_id), gray)

            #print queue size
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        self.publisher_queue.put("Done")
        print("PublisherID "+ str(self.publisher_id) +"  Queue SIZE...."+ str(Config.publisher_queue_map.get(self.publisher_id).qsize()))
        dt2 = datetime.now()
        print("Time take to read video: ", self.publisher_id, " : ", (dt2-dt1).total_seconds())



        # When everything done, release the capture
        cap.release()
        #cv2.destroyAllWindows()




