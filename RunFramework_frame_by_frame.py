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
from multiprocessing import Pool, Process, Queue
import numpy as np
import sys
from Models.MobileNet import model, batch_prediction
import cv2
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



window_queue = None
blocks = []

def grouper(mwin_q, results_batch):
    # print("in here")
    temp_block = []
    # count = 0
    while True:
        sleep(1/59)
        # print("I'm checking.. ", count)
        # count += 1
        try:
            new_frame = mwin_q.get(block=False)
            new_frame_data = new_frame['frame_data']
            new_frame_time_id = new_frame['time_window_id']
            
            if new_frame_data == "poison":
                break
            elif temp_block == []:
                if new_frame_data[0] == 'I':
                    temp_block.append((new_frame_data[1], new_frame_time_id))
                else:
                    temp_block.append((new_frame_data[0], new_frame_time_id))
            else:
                if new_frame_data[0] == "I":
                    results_batch.put(temp_block)
                    print("New block found I frame - len ", len(temp_block))
                    temp_block.clear()
                    temp_block.append((new_frame_data[1], new_frame_time_id))
                else:
                    # print(new_frame_data[0].shape)
                    dist = get_frame_distance(new_frame_data[0], temp_block[0][0])
                    if dist < 0.8:
                        results_batch.put(temp_block)
                        print("New block found separate - len ", len(temp_block))
                        temp_block.clear()
                    temp_block.append((new_frame_data[0], new_frame_time_id))
                        # print(blocks)
        except queue.Empty:
            pass

        # print()
            # print("got queue empty")

def bufferer(buffer_queue, single_frame_queue):
    while True:
        get_frame = buffer_queue.get()
        if get_frame == "Done":
            single_frame_queue.put("Done")
            break
        single_frame_queue.put(get_frame)

def publisher_worker(publisher_queue, mwindow_queue, single_frame_queue, buffer_queue):
    # while True:
    #     try:
    #         new_batch = results_batch.get(block=True)
    #         processed_batch = []
    #         for i in new_batch:
    #             processed_batch.append(new_batch[0])
    #         # print(len(new_batch))
    #         print("Received new mini batch.. sending for processing")
    #         # with_batches(new_batch)
    #         # batch_prediction(processed_batch, model)
    #     except Exception as e:
    #         print(e)
    intial_time = datetime.now()

    try:
        # for frame in iter(publisher_queue.get, None):
        while True:
            get_frame = publisher_queue.get(block=True)
            if get_frame == "Done":
                print("inside this")
                mwindow_queue.close()
                buffer_queue.put("Done")
                raise queue.Empty
            # sleep(1/100)
            buffer_queue.put((get_frame, datetime.now()))
            # mwindow_queue.put( { "frame_data" : get_frame, "time_window_id" : int((datetime.now() - intial_time).total_seconds()/5) + 1 } )

    except Exception as e:
        # raise e from None
        print("No more frames to publish, exiting...")
        return
   
# run time window
def intialize_timewindow(publisher_id, time_duration):
    # global window_queue
    count = 1
    publisher_queue = get_publisher_queue(publisher_id) # here 1 is publisher id
    intial_time = datetime.now()
    # window_queue = queue.Queue(maxsize=0)
    mwindow_queue = Queue()
    results_batch = Queue()
    single_frame_queue = Queue()
    buffer_queue = Queue()
    latencies = []
    # flag = 1
    # p = Process(target=grouper, args=(mwindow_queue, results_batch,))
    # p.start()

    # s = Process(target=single_frame_processor, args=(single_frame_queue,))
    # s.start()

    r = Process(target=publisher_worker, args=(publisher_queue, mwindow_queue, single_frame_queue, buffer_queue, ))
    r.start()

    b = Process(target=bufferer, args=(buffer_queue, single_frame_queue,  ))
    b.start()

    start_time = datetime.now()
    while True:
        # For single frame processing
        try:
            get_data = single_frame_queue.get()
            if get_data == "Done":
                break
            new_frame, time_stayed = get_data
            if new_frame[0] == 'I':
                new_frame = new_frame[1]
            else:
                new_frame = new_frame[0]
            # batch_prediction(np.array([new_frame]), model)
            # rs_time = datetime.now()
            # new_dim = (300,300)
            # new_frame = cv2.resize(new_frame, new_dim)
            # print("resize time :- ", (datetime.now() - rs_time).total_seconds())
            # print(new_frame.shape)
            prdd = batch_prediction(np.array([new_frame]), model)
            latency = (datetime.now() - time_stayed).total_seconds()
            # print(latency)
            latencies.append(latency)

            # print(prdd)
            # if prdd[0][1][0] == 'car':
            #     print(prdd[0][1][0], "  more")
            #     cv2.imwrite("car_100/ccc"+str(count)+".jpg", new_frame)
            #     count += 1
            # else:
            #     print(prdd[0][1][0], "  more")
            #     cv2.imwrite("not_car_100/ccc"+str(count)+".jpg", new_frame)
            #     count += 1
            # if len(new_frame.shape) == 3:
            #     batch_prediction(np.array([new_frame]), model)
            # else:
            #     batch_prediction(np.array(new_frame), model)
        except Exception as e:
            raise e from None
    end_time = datetime.now()
    elasped_time = (end_time - start_time).total_seconds()
    print(elasped_time, "s for frame by frame processing")


    # print(np.array(latencies).mean())
    non_cum_latencies = [latencies[0]]
    for i in range(1,len(latencies)):
        non_cum_latencies.append(latencies[i] - latencies[i-1])
    print(np.array(non_cum_latencies).mean())
        # # for batch wise processing
        # try:
        #     new_batch = results_batch.get(block=True)
        #     processed_batch = []
        #     for i in new_batch:
        #         processed_batch.append(i[0])
        #     print(len(new_batch))
        #     print("Received new mini batch.. sending for processing")
        #     # with_batches(new_batch)
        #     # print(processed_batch[0].shape)
        #     # te = np.stack(processed_batch, axis=0)
        #     # print(te.shape)
        #     batch_prediction(np.stack(processed_batch, axis=0), model)
        # except Exception as e:
        #     raise e from None 
        #     print(e)


def single_frame_processor(single_frame_queue):
    while True:
        new_frame = single_frame_queue.get(block=True)
        if new_frame[0] == 'I':
            new_frame = new_frame[1]
        pred = mobile_net(new_frame)
        print(pred)

def with_batches(batch):
    preds = mobile_net(batch)
    print(preds)


def mobile_net(batch):
    return "10preds"
# if __name__== "__main__":

# create subscriber query map to read the VEQL query

if __name__ == '__main__':
# <----Configure and start Publisher---->
    publisher = ConfigurePublisher()
    publisher.configureandstartpublisher()

    # <----Start Window---->
    intialize_timewindow(0, 5)



    # code for light weight process for

    # queue_items = get_publisher_queue(0)

    # print(queue_items)
    pre_frame =[]
    frame_count =1
    batch_size =[]

# count = 0



         

# while not queue_items.empty():
#     # count += 1
#     a = queue_items.get()

#     if not pre_frame:
#         print("List frame empty")
#         if(len(a)==2):
#             pre_frame.append(a[1])
#             Config.frame_arr.append(frame_count)
#         else:
#             pre_frame.append(a[0])
#             Config.frame_arr.append(frame_count)

#     else:
#         if(len(a)==2):
#             dist_val = get_frame_distance(pre_frame[0],a[1])
#             Config.dist_arr.append(dist_val)
#             Config.frame_arr.append(frame_count)
#             #batch_size.append(1)
#             #print("I frame batch Size:", len(batch_size))
#             #batch_size.clear()
#             #print("List Clear")
#             pre_frame.clear()
#             pre_frame.append(a[1])
#         else:
#             dist_val = get_frame_distance(pre_frame[0],a[0])
#             Config.dist_arr.append(dist_val)
#             Config.frame_arr.append(frame_count)
#             batch_size.append(1)
#             #print("List Clear")
#             if(dist_val < 0.8):
#                 print("batch: ", len(batch_size) )
#                 #batch_size.clear()
#                 pre_frame.clear()
#                 pre_frame.append(a[0])
#                 #batch_size.append(1)

#     frame_count +=1


#     if(len(a)==2):
#         print("I......")
#         #cv2.imwrite('1.jpg',a)
#         #cv2.imshow('frame',a[1])
#         #cv2.waitKey(5000)

# live_graph()
