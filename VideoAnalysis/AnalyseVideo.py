# Author - Piyush Yadav
# Insight Centre for Data Analytics
# Package- VidWIN Project


import os
import cv2
import subprocess
from datetime import datetime

filename = '/home/piyush/Desktop/VIDWIN_Demo/DataSets/Publisher/0.mp4'

# function to get IPB frames

def get_frame_types(video_fn, publisher_id):
    command = 'ffprobe -v error -show_entries frame=pict_type -of default=noprint_wrappers=1'.split()
    dt1 = datetime.now()
    out = subprocess.check_output(command + [video_fn]).decode()
    dt2 = datetime.now()
    time_diff = dt2-dt1
    print("Video " + str(publisher_id)+" Probe Time(ms) == " + str(time_diff.total_seconds()*1000))
    frame_types = out.replace('pict_type=','').split()
    return zip(range(len(frame_types)), frame_types)

# function to get distance between histograms of two frames.
def get_frame_distance(frame1, frame2):
    hsv_frame1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2HSV)
    hsv_frame2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2HSV)
    h_bins = 50
    s_bins = 60
    histSize = [h_bins, s_bins]
    # hue varies from 0 to 179, saturation from 0 to 255
    h_ranges = [0, 180]
    s_ranges = [0, 256]
    ranges = h_ranges + s_ranges # concat lists
    # Use the 0-th and 1-st channels
    channels = [0, 1]
    hist_frame1 = cv2.calcHist([hsv_frame1], channels, None, histSize, ranges, accumulate=False)
    cv2.normalize(hist_frame1, hist_frame1, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX)
    hist_frame2 = cv2.calcHist([hsv_frame2], channels, None, histSize, ranges, accumulate=False)
    cv2.normalize(hist_frame2, hist_frame2, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX)

    # only one compare memthod
    dist_value = cv2.compareHist(hist_frame1, hist_frame2, 0)
    return dist_value
    # print('Method:', 0, ' Distance:',\
    #       base_base, '/')

    # for compare_method in range(4):
    #     base_base = cv2.compareHist(hist_frame1, hist_frame2, compare_method)
    #     print('Method:', compare_method, 'Perfect, Base-Half, Base-Test(1), Base-Test(2) :',\
    #       base_base, '/')

def save_i_keyframes(video_fn):
    frame_types = get_frame_types(video_fn)
    i_frames = [x[0] for x in frame_types if x[1]=='I']
    print(i_frames)
    if i_frames:
        basename = os.path.splitext(os.path.basename(video_fn))[0]
        cap = cv2.VideoCapture(video_fn)
        for frame_no in i_frames:
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_no)
            ret, frame = cap.read()
            outname = basename+'_p_frame_'+str(frame_no)+'.jpg'
            #cv2.imwrite(outname, frame)
            print ('Saved: '+outname)
        cap.release()
    else:
        print ('No I-frames in '+video_fn)

if __name__ == '__main__':
    save_i_keyframes(filename)