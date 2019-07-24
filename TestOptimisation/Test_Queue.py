# Author - Piyush Yadav
# Insight Centre for Data Analytics
# Package- VidWIN Project

import queue

q = queue.Queue()

for i in range(5):
    q.put(i,'X')

while not q.empty():
    print(q.get())

