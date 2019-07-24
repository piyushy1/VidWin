# Author - Piyush Yadav
# Insight Centre for Data Analytics
# Package- VidWIN Project

import os
from GlobalVariables import Config
import concurrent.futures
from VideoStreamPublisher.ConnectPublisher import ConnectPublisher

def test(a):
    print(a)

class ConfigurePublisher:

    def __init__(self):
        print("")


    def configureandstartpublisher(self):

        #how many video publishers

        publisher_entries = os.listdir(Config.PUBLISHER_FOLDER_PATH)
        print(publisher_entries)

        # start the different publisher thread

        with concurrent.futures.ThreadPoolExecutor(max_workers= Config.PUBLISHER_NUMBER) as executor:
            #print(len(publisher_entries))
            for publisher_id in range(0, Config.PUBLISHER_NUMBER):
                print(Config.PUBLISHER_FOLDER_PATH+publisher_entries[publisher_id])
                publisher = ConnectPublisher(Config.PUBLISHER_FOLDER_PATH+publisher_entries[publisher_id],publisher_id)
                #executor.submit(publisher.test_publisher, publisher_id)
                executor.submit(publisher.connect_publisher_source)





