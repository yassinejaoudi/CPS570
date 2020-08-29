'''
Team Members:
    Yassine Jaoudi
    Akpan, Samuel Cyril  
'''

# import libraries or classes
import validators # source: https://validators.readthedocs.io/en/latest/#
import sys
from urllib.parse import urlparse # source: https://docs.python.org/3/library/urllib.parse.html 
from queue import Queue
from Asg1Socket import TCPsocket
from Asg1Request import Request

# TODO: main must accept two args:
    # 1-) number of threads
    # 2-) Input file
    # Example: python main.py 1 URL-input-100.txt

def main(): # function, method are the same

    mysocket = TCPsocket() # create an object of TCP socket
    mysocket.createSocket()
    Q = Queue()
    myrequest = Request()
    
    # TODO: (Not needed in part 1) Loop over the input file to read URLs 
    # Not sure if we need to create a socket for each one
    # try:
    #     with open("URL-input-100.txt") as file:
    #         for line in file:
    #             Q.put(line)
    # except IOError:
    #     print('No such file. Please include an existing file name ...')
    #     exit(1)

    # print("arg: {} & type: {}".format(sys.argv[1],type(str(sys.argv[1]))))
    # TODO: (Part1) We might need to pass only one arg instead of a list of args to
    # satisfy part 1 requirement (program must accept a single command-line arg)
    parsedHost = urlparse(sys.argv[1])
    host = parsedHost.geturl()
    if (validators.url(host)):
        print('URL: {}'.format(host))
        print('         Parsing URL... host {}, port {}, request /{}'.format(parsedHost.netloc,parsedHost.port,parsedHost.query))
        getIpInfo = mysocket.getIP(parsedHost.netloc)
        myIp = getIpInfo[0]
        print('         Doing DNS... done in {} ms, found {}'.format(getIpInfo[1], myIp))
        # TODO: For politeness, the code will need to hit only unique IPs (Check if the ip is unique)
        # TODO: Abort all pages that takes longer than 10 secs or are more than 2MB
        port = 80
        mysocket.connect(myIp, port)

        # build our request
        msg = myrequest.headRequest(parsedHost.netloc)

        # send out request
        mysocket.send(msg)
        data = mysocket.receive() # receive a reply from the server
        print("data received: ", data)
        
        mysocket.close()
    else:
        print('Please include a valid URL in command line ...')   
    

# call main() method:
if __name__ == "__main__":
   main()

# TODO: Things to check before submitting the assignment:
    # writing poorly designed or convoluted code, not checking for errors in every API you call, 
    # and allowing buffer overflows, access violations, debug-assertion failures,
    # heap corruption, synchronization bugs, memory leaks, or any conditions that lead to a crash