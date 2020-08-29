'''
Team Members:
    Yassine Jaoudi
    Akpan, Samuel Cyril  
'''

# import libraries or classes
import validators # source: https://validators.readthedocs.io/en/latest/#
import sys
from Asg1Socket import TCPsocket
from Asg1Request import Request

# TODO: main must accept two args:
    # 1-) number of threads
    # 2-) Input file
    # Example: python main.py 1 URL-input-100.txt

def main(): # function, method are the same

    mysocket = TCPsocket() # create an object of TCP socket
    mysocket.createSocket()
    
    # TODO: Loop over the input file to read URLs 
    # Not sure if we need to create a socket for each one
    # print("arg: {} & type: {}".format(sys.argv[1],type(str(sys.argv[1]))))
    # TODO: (Part1) We might need to pass only one arg instead of a list of args to
    # satisfy part 1 requirement (program must accept a single command-line arg)
    host = sys.argv[1]
    if (validators.url(host)):
        print('URL: {}'.format(host))
        ip = mysocket.getIP(host)
        # TODO: For politeness, the code will need to hit only unique IPs (Check if the ip is unique)
        port  = 80
        # TODO: Abort all pages that takes longer than 10 secs or are more than 2MB
        mysocket.connect(ip, port)

        # build our request
        myrequest = Request()
        msg = myrequest.headRequest(host)

        # send out request
        mysocket.send(msg)
        data = mysocket.receive() # receive a reply from the server
        print("data received: ", data)
        
        mysocket.close()
    else:
        print('Please type a valid URL ...')   
    

# call main() method:
if __name__ == "__main__":
   main()

# TODO: Things to check before submitting the assignment:
    # writing poorly designed or convoluted code, not checking for errors in every API you call, 
    # and allowing buffer overflows, access violations, debug-assertion failures,
    # heap corruption, synchronization bugs, memory leaks, or any conditions that lead to a crash