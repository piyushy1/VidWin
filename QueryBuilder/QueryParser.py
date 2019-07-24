# Author - Piyush Yadav
# Insight Centre for Data Analytics
# Package- VidWIN Projectd

from GlobalVariables import Config
import re

def parse_query(query):
    query_predicates = re.split('\*', query)
    #presently focussing only on tumble time window..
    matching = [s for s in query_predicates if "WITHIN" in s]
    for i in matching:
        time = re.split('\=',i)
        return time[1]


def read_query():
    #open the query file
    query_file = open(Config.SUBSCRIBER_FOLDER_PATH, "r")
    window_value =[]
    for query in query_file:
        window_value.append(parse_query(query))

    return window_value[0]





