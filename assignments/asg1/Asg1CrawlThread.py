'''
Team Members:
    Yassine Jaoudi
    Akpan, Samuel Cyril  
    Samantha Clark
'''

import sys, time, os, threading
from Asg1Socket import TCPsocket
from Asg1Request import Request
from Asg1Urlparser import URLparser
from queue import Queue

class MyThread (threading.Thread):
    sharedCount = [1]
    sharedLock = threading.Lock()
    sharedQ = Queue()
    sharedHost = set()
    sharedIP = set()
    sharedDns = [0]

    def __init__(self, ID, name, urlqueue, uniqueIPs, uniqueHost, count, extUrls, DnsLooks, transRate):
        threading.Thread.__init__(self)
        #define instance variables
        #initialize class variables
        self.threadID = ID #ID is an int
        self.name = name # name is a string
        self.counter = count # integer
        self.sharedCount[0] = urlqueue.qsize()
        self.sharedQ = urlqueue
        self.sharedHost = uniqueHost
        self.sharedIP = uniqueIPs
        self.sharedExtUrl = extUrls
        self.sharedDns =  DnsLooks
        self.sharedRate = transRate
    
    def run(self): #override the run() method
        #define job for each thread
        # print(self.name + " thread starting ")
        mysocket = TCPsocket() # create an object of TCP socket
        myrequest = Request()
        myparser  = URLparser()
        url = [""] #list contains one string for a url
        pHostSize = 0 # previous Host Size
        cHostSize = 0 # current  Host Size
        pIpSize = 0 # previous Ip Size
        cIpSize = 0 # current  Ip Size
        #robochecks count
        robochecks = 0 #will need updated
        #links count
        links = 0 #should update after pages are parsed--will fix if not
        ctr = 1
        # extUrls = []

        while not self.sharedQ.empty():
            if(self.threadID == 0):
                time.sleep(2)
                self.sharedLock.acquire()
                tm = 2 * ctr
                print("[", tm, "]     ", self.sharedCount[0], " Q       ", len(self.sharedExtUrl), " E      ", len(self.sharedHost), " H      ", len(self.sharedIP) - self.sharedDns[0], " D        ", len(self.sharedIP), " I       ", robochecks, " R      ", len(url), " C        ", links, " L       ") #Add XK - count?
                print("       *** crawling {} pps @ {} Mbps".format(0.1, 20))
                ctr += 1
                if (self.sharedCount[0] < 1):  # if empty Q, let thread 0 exit
                    self.sharedLock.release()
                    break   
                self.sharedLock.release()
            else:
                self.sharedLock.acquire() #one thread modifies items at a time
                if (self.sharedCount [0] < 1):
                    self.sharedLock.release()
                    break
                url[0] = self.sharedQ.get() #remove and return an item from the queue
                self.sharedExtUrl.add(url[0])
                # print("thread%d %d %s" % (self.threadID, self.sharedCount[0], url[0]))
                self.sharedCount[0] -= 1
                self.sharedLock.release() #end of critical section

                self.counter += 1
                host, port, path, query  = myparser.parse(url[0])
                # print('URL: {}'.format(url[0]))
                # print('         Parsing URL... host {}, port {}, path {}, request {}'.format(host, port, path, query))

                #parallel by multiple threads
                self.sharedLock.acquire()
                pHostSize = len(self.sharedHost)
                self.sharedHost.add(host)
                # sys.stdout.write("         Checking host uniqueness... ")
                cHostSize = len(self.sharedHost)
                self.sharedLock.release()

                if (cHostSize > pHostSize):
                    # sys.stdout.write('passed' + '\n')
                    self.sharedLock.acquire()
                    myIp = mysocket.getIP(host)
                    if myIp == None:
                        self.sharedDns[0] += 1
                        print('SharedDNs: ',self.sharedDns[0])  
                        self.sharedLock.release()
                        break
                    # self.sharedLock.acquire()
                    pIpSize = len(self.sharedIP)
                    self.sharedIP.add(myIp)
                    # sys.stdout.write("         Checking IP uniqueness... ")
                    cIpSize = len(self.sharedIP)
                    self.sharedLock.release()

                    if (cIpSize > pIpSize):
                        # sys.stdout.write('passed' + '\n')
                        msg = myrequest.headRequest(host) # build our request
                        self.sharedLock.acquire()
                        if query.find('download') == -1:
                            mysocket.checkrobots(host)
                            currentURL = url[0]
                            myparser.parsePage(currentURL, links) #might need to update links)
                            self.sharedLock.release()

                            self.sharedLock.acquire()
                            data = mysocket.crawl(port, msg, host, myIp)
                            # self.sharedRate += len(data)
                            idx = data.find('HTTP/')
                            if idx != -1:
                                statusCode = data[idx+8:idx+13]
                                if (statusCode != '200 OK'):
                                    # sys.stdout.write("status code {}\n".format(statusCode))
                                    # myparser.responseParser(data)
                                    mysocket.close()
                                else:
                                    mysocket.close()
                        else:
                            mysocket.close()
                            # break

                        self.sharedLock.release()

                    # else:
                        # sys.stdout.write(' NOT unique' + '\n')
                # else:
                    # sys.stdout.write(' NOT unique' + '\n')
                # time.sleep(1) #given url, parse it, get ip address, check if ip is unique, ...
                # print('\nQueue length: ',len(self.sharedQ.queue))
                continue
            # print("thread %d thread existing " % (self.threadID))

def main():
    
    if len(sys.argv) < 3:
        print("Error: insufficient arguments \nCorrect Usage: <interpreter> <Program Name> <No. of threads> <URL>")
        sys.exit()

    startT = time.time()
    Q = Queue()

    # Args
    numThreads = int(sys.argv[1])
    filename = sys.argv[2]
    print("\nOpened {} with size {} bytes".format(filename, os.stat(filename).st_size))

    # Opening designated file
    try:
        with open(filename) as file:
            for line in file:
                Q.put(line)
    except IOError:
        print('No such file')
        exit(1)
    
    # print("Queue size:", Q.qsize()) 
    listOfThreads = [] # empty list
    uniqueIPs = set()
    uniqueHost = set()
    extUrls = set()
    DnsLooks = [0]
    transRate = set()

    count = 0
    
    for i in range(0, numThreads, 1):
        t = MyThread(i, "Hi, ", Q, uniqueIPs, uniqueHost, count, extUrls, DnsLooks, transRate)
        t.start()
        listOfThreads.append(t)
    for t in listOfThreads:
        t.join()
    runTime = time.time() - startT
    print("Running time is ", runTime)

    print('Extracted {} URLs @ {}/s'.format(len(t.sharedExtUrl), round(len(t.sharedExtUrl)/runTime,2)))
    #TODO: Fix the DNS number by incrementing the overall DNS for all threads
    print('Looked up {} DNS names @ {}/s'.format((len(t.sharedIP) - t.sharedDns[0]), round((len(t.sharedIP) - t.sharedDns[0])/runTime,2)))
    # print('Downloaded {} robots @ {}/s'.format())

if __name__ == '__main__':
    main()
