'''
Team Members:
    Yassine Jaoudi
    Akpan, Samuel Cyril  
    Samantha Clark
'''
from queue import Queue
import threading
import time

class MyThread (threading.Thread):
    sharedCount = [1]
    sharedLock = threading.Lock()
    sharedQ = Queue()

    def __init__(self, ID, name, count, urlqueue):
        threading.Thread.__init__(self)
        #define instance variables
        #initialize class variables
        self.threadID = ID #ID is an int
        self.name = name # name is a string
        self.counter = count # integer
        self.sharedCount[0] = urlqueue.qsize()
        self.sharedQ = urlqueue

    def run(self): #override the run() method
        #define job for each thread
        print(self.name + " thread starting ")
        url = [""] #list contains one string for a url
        while(True):
            self.sharedLock.acquire() #one thread modifies items at a time
            if (self.sharedCount [0] < 1):
                self.sharedLock.release()
                break
            url[0] = self.sharedQ.get() #remove and return an item from the queue
            print("thread%d %d %s" % (self.threadID, self.sharedCount[0], url[0]))
            self.sharedCount[0] -= 1
            self.sharedLock.release() #end of critical section
            #parallel by multiple threads
            print(self.name + " crawling " + url[0])
            time.sleep(1) #given url, parse it, get ip address, check if ip is unique, ...
        print("thread %d thread existing " % (self.threadID))
def main():
    startT = time.time()
    Q = Queue()
    try:
        with open("URL-input-100.txt") as file:
            for line in file:
                Q.put(line)
    except IOError:
        print('No such file')
        exit(1)
    print("Queue size:", Q.qsize()) 
    listOfThreads = [] # empty list
    numThreads = 100 #Can change for single-threaded
    for i in range(0, numThreads, 1):
        t = MyThread(i, "hi", 10, Q)
        t.start()
        listOfThreads.append(t)
    for t in listOfThreads:
        t.join()
    runTime = time.time() - startT
    print("Running time is ", runTime)

if __name__ == '__main__':
    main()
