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
    sharedRplSz = [0]
    SharedRbtChecks = [0]
    sharedHTTPCodes = []
    sharedOtherHttp = []
    sharedLinks = [0]

    def __init__(self, ID, name, urlqueue, uniqueIPs, uniqueHost, count, extUrls, DnsLooks, transRate, robochecks,rplSz, ppsRate, pendingQ, links, vldHTTP, httpCodes, otherHttp):
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
        self.SharedRbtChecks = robochecks
        self.sharedRplSz = rplSz
        self.sharedPpsRate = ppsRate
        self.sharedpendingQ = pendingQ
        self.sharedLinks = links
        self.sharedVldHTTP = vldHTTP
        self.sharedHTTPCodes = httpCodes
        self.sharedOtherHttp = otherHttp
    
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
        ctr = 1

        while not self.sharedQ.empty():
            if(self.threadID == 0):
                
                # Reinitialize the packet per sec variable
                self.sharedPpsRate[0] = 0
                
                time.sleep(2)
                self.sharedLock.acquire()
                tm = 2 * ctr
                print("[", tm,"]", self.sharedpendingQ, " Q", (self.sharedCount[0] - self.sharedpendingQ),"      ", len(self.sharedExtUrl), " E      ", 
                    len(self.sharedHost), " H      ", len(self.sharedIP) - self.sharedDns[0], " D        ", len(self.sharedIP), " I       ", 
                    self.SharedRbtChecks[0], " R      ", self.sharedVldHTTP[0], " C        ", self.sharedLinks[0], " L       ") #Add XK - count?
                print("       *** crawling {} pps @ {} Mbps".format(self.sharedPpsRate[0]/2, round(self.sharedRplSz[0]*10**-6/2,6)))
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
                        self.sharedLock.acquire()
                        msg = myrequest.headRequest(host) # build our request
                        self.sharedPpsRate[0] += 1
                        self.sharedLock.release()

                        self.sharedLock.acquire()
                        if query.find('download') == -1:
                            
                            rbtcheck = mysocket.checkrobots(host)
                            # print('Rbtchecks: ',rbtcheck)
                            if rbtcheck != None:
                                self.SharedRbtChecks[0] += 1

                            # self.sharedLock.acquire()
                            currentURL = url[0]
                            # print('Before ',self.sharedLinks[0])
                            links = myparser.parsePage(currentURL)
                            # print(links, type(links))
                            if links != None:
                                self.sharedLinks[0] += len(links)
                                # print('after: ',self.sharedLinks[0])
                            #might need to update links)
                            # self.sharedLock.release()

                            # self.sharedLock.acquire()

                            data = mysocket.crawl(port, msg, host, myIp)
                            # Increment the received data
                            self.sharedRplSz[0] += len(data)
                            idx = data.find('HTTP/')
                            if idx != -1:
                                statusCode = data[idx+8:idx+13]
                                # print('statusCode: ',statusCode[1])
                                if (statusCode[1] == '2' or '3' or '4' or '5'):
                                    self.sharedVldHTTP[0] += 1
                                    self.sharedHTTPCodes.append(statusCode[1:4])
                                    mysocket.close()
                                else:
                                    self.sharedOtherHttp.append(statusCode[1:4])
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
    robochecks = [0]
    rplSz = [0]
    ppsRate = [0]
    vldHTTP = [0]
    pendingQ = numThreads
    links = [0]
    count = 0
    httpCodes = []
    otherHttp = []
    
    for i in range(0, numThreads, 1):
        t = MyThread(i, "Hi, ", Q, uniqueIPs, uniqueHost, count, extUrls, DnsLooks, transRate, robochecks, rplSz, ppsRate, pendingQ, links, vldHTTP, httpCodes, otherHttp)
        t.start()
        listOfThreads.append(t)
    for t in listOfThreads:
        t.join()
    runTime = time.time() - startT

    twx = [0]
    trwx = [0]
    fxx = [0]
    fivx = [0]
    for i in t.sharedHTTPCodes:
        if i[0] == '2':
            twx[0] += 1
        elif i[0] == '3':
            trwx[0] +=1
        elif i[0] == '4':
            fxx[0] += 1
        else:
            fivx[0] += 1

    print("\nRunning time is ", runTime)

    print('Extracted {} URLs @ {}/s'.format(len(t.sharedExtUrl), round(len(t.sharedExtUrl)/runTime,2)))
    print('Looked up {} DNS names @ {}/s'.format((len(t.sharedIP) - t.sharedDns[0]), round((len(t.sharedIP) - t.sharedDns[0])/runTime,2)))
    print('Downloaded {} robots @ {}/s'.format(t.SharedRbtChecks[0], round(t.SharedRbtChecks[0]/runTime,2)))
    # TODO: Fill the variables below with the correct ones
    print('Crawled {} pages @ {}/s ({} MB)'.format(11,1,0.23))
    print('Parsed {} links @ {}/s'.format(t.sharedLinks[0],  round(t.sharedLinks[0]/runTime,2)))
    print('HTTP codes: 2xx = {}, 3xx = {}, 4xx = {}, 5xx = {}, other = {}'.format(twx[0],trwx[0],fxx[0],fivx[0],len(t.sharedOtherHttp)))

if __name__ == '__main__':
    main()
