'''
Team Members:
    Yassine Jaoudi
    Akpan, Samuel Cyril  
    Samantha Clark
'''

# import libraries or classes
import sys 
import os 
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

    print("Opened {} with size {} bytes".format(filename, os.stat(filename).st_size))
   

    try:
        with open(filename) as file:
            for line in file:
                Q.put(line)
    except IOError:
        print('No such file')
        exit(1)
    
    count = 0
    uniqueIPs = set()
    uniqueHost = set()
    hlinks = 0

    while not Q.empty():
        URL = Q.get()
        count += 1
        host, port, path, query  = myparser.parse(URL)
        print('URL: {}'.format(URL))
        print('         Parsing URL... host {}, port {}, path {}, request {}'.format(host, port, path, query))
        
        msg = myrequest.headRequest(host) # build our request
        data = mysocket.crawl(port, msg, host)
        idx = data.find('HTTP/')
        if idx != -1:
            statusCode = data[idx+8:idx+13]
            sys.stdout.write("status code {}\n".format(statusCode))
        # Notice: switched out the cleanStr function. The responseParse function is what I used to rearrange the display
        myparser.responseParser(data)
        
        mysocket.close()
    

# call main() method:
if __name__ == "__main__":
   main()
