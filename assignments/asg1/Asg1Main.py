'''
Team Members:
    Yassine Jaoudi
    Akpan, Samuel Cyril  
    Samantha Clark
'''

# import libraries or classes
import sys 
import os 
<<<<<<< HEAD
#from Path import pathlib 
=======
>>>>>>> 072540a4ffe02df8ad8b79fad51d9d698da7d682
from Asg1Socket import TCPsocket
from Asg1Request import Request
from Asg1Urlparser import URLparser
from queue import Queue



def main(): # function, method are the same
    if len(sys.argv) < 3:
        print("Error: insufficient arguments \nCorrect Usage: <interpreter> <Program Name> <No. of threads> <URL>")
        sys.exit()
    mysocket = TCPsocket() # create an object of TCP socket
    myrequest = Request()
    myparser  = URLparser()
    Q = Queue()

    numThreads = sys.argv[1]
    filename = sys.argv[2]


    print('\nSys.argv: ',sys.argv)
    print('\nFilename: {} & numThreads: {}'.format(filename,numThreads))
<<<<<<< HEAD
    ###print("Opened {} with size {}".format(filename, os.stat.(filename).st_size))
    
=======
    print("Opened {} with size {} bytes".format(filename, os.stat(filename).st_size))
    sys.exit()
>>>>>>> 072540a4ffe02df8ad8b79fad51d9d698da7d682
    try:
        with open(filename) as file:
            for line in file:
                Q.put(line)
    except IOError:
        print('No such file')
        exit(1)
    
    count = 0
    uniqueIPs = set()
    hlinks = 0

    while not Q.empty():
        URL = Q.get()
        count += 1
        host, port, path, query  = myparser.parse(URL)
        print('URL: {}'.format(URL))
        print('         Parsing URL... host {}, port {}, path {}, request {}'.format(host, port, path, query))
        getIpInfo = mysocket.getIP(host)
        myIp = getIpInfo[0]
        
        sys.stdout.write("         Checking IP uniqueness... ")
        if myIp not in uniqueIPs:
            uniqueIPs.add(myIp)
            sys.stdout.write("passed\n")
            msg = myrequest.headRequest(host) # build our request
            getIpInfo = mysocket.getIP(host)
            myIp = getIpInfo[0]
            print('         Doing DNS... done in {} ms, found {}'.format(round(getIpInfo[1],2), myIp))
            # uniqueIPs = mysocket.IPUnique(myIp, uniqueIPs)
            data = mysocket.crawl(port, msg, myIp)
            idx = data.find('HTTP/')
            if idx != -1:
                statusCode = data[idx+8:idx+13]
                sys.stdout.write("status code {}\n".format(statusCode))

            # Notice: switched out the cleanStr function. The responseParse function is what I used to rearrange the display
            myparser.responseParser(data)
        else:
            print('IP not unique\n')
        
        # TODO: Hint Use a dict data type for How many links in this link? keyword "href" for counting 
        # TODO: For politeness, the code will need to hit only unique IPs (Check if the ip is unique)
        # TODO: Abort all pages that takes longer than 10 secs or are more than 2MB
        
        mysocket.close()
    

# call main() method:
if __name__ == "__main__":
   main()

# TODO: Things to check before submitting the assignment:
    # writing poorly designed or convoluted code, not checking for errors in every API you call, 
    # and allowing buffer overflows, access violations, debug-assertion failures,
    # heap corruption, synchronization bugs, memory leaks, or any conditions that lead to a crash
