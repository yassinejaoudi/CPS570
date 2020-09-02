'''
Team Members:
    Yassine Jaoudi
    Akpan, Samuel Cyril  
'''

# import libraries or classes
# import validators # source: https://validators.readthedocs.io/en/latest/#
import sys
# from urllib.parse import urlparse # source: https://docs.python.org/3/library/urllib.parse.html 
from Asg1Socket import TCPsocket
from Asg1Request import Request
from Asg1Urlparser import URLparser

# TODO: main must accept two args:
    # 1-) number of threads
    # 2-) Input file
    # Example: python main.py 1 URL-input-100.txt

def main(): # function, method are the same

    mysocket = TCPsocket() # create an object of TCP socket
    myrequest = Request()
    myparser  = URLparser()
    
    URL = sys.argv[1]
    host, port, path, query  = myparser.parse(URL)
    print('URL: {}'.format(URL))
    print('         Parsing URL... host {}, port {}, path {}, request {}'.format(host, port, path, query))
    
    # TODO: For politeness, the code will need to hit only unique IPs (Check if the ip is unique)
    # TODO: Abort all pages that takes longer than 10 secs or are more than 2MB
    
    msg = myrequest.headRequest(host) # build our request
    data = mysocket.crawl(host, port, msg)
    idx = data.find('HTTP/1.0')
    if idx != -1:
        statusCode = data[idx+8:idx+13]
        sys.stdout.write("status code {}\n".format(statusCode))
'''
Notice: switched out the cleanStr function. The responseParse function is what I used to rearrange the display
'''
    
    #if len(data) != 0:
    #   myrequest.cleanStr(data) 

    myparser.responseParser(data)
    mysocket.close()
    

# call main() method:
if __name__ == "__main__":
   main()

# TODO: Things to check before submitting the assignment:
    # writing poorly designed or convoluted code, not checking for errors in every API you call, 
    # and allowing buffer overflows, access violations, debug-assertion failures,
    # heap corruption, synchronization bugs, memory leaks, or any conditions that lead to a crash