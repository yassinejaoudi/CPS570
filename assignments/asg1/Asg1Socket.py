'''
Team Members:
    Yassine Jaoudi
    Akpan, Samuel Cyril 
    Samantha Clark 
'''

# resources: https://docs.python.org/3/howto/sockets.html

import socket, select, time, sys, urllib.request, requests
from Asg1Request import Request 
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from Asg1Urlparser import URLparser

TIMEOUT = 10 # unit is seconds
BUF_SIZE = 1024 # unit is bytes ##was 4096

class TCPsocket:

    # Set the default timeout in seconds
    timeout = 20
    socket.setdefaulttimeout(timeout)

    # list our instance variables
    # Constructor: create an object
    def __init__(self):
        self.sock = None  # each object's instance variables
        self.host = ""  # remote host name
        # print("create an object of TCPsocket")

    def createSocket(self):
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # self.sock is an instance variable
            # print("created a tcp socket!")
        except socket.error as e:
            print("Failed to create a TCP socket {}".format(e))
            self.sock = None

    # www.google.com -> host name
    # given a host name, how to get its ip address
    # Return the ip of input hostname. Both ip and hostname in string
    def getIP(self, hostname):
        self.host = hostname
        try:
            dns_start = time.time()
            ip = socket.gethostbyname(hostname)   # ip is a local variable to getIP(hostname), ip is of string type
            dns_end = time.time()
            dns_time = (dns_end - dns_start) * 1000 # in ms 
            # print('         Doing DNS... done in {} ms, found {}'.format(round(dns_time,2), ip))
        except socket.gaierror:
            # print("DNS failure... Unable to obtain IP address")
            return None
        return ip

    def checkrobots(self,hostname):
        # useragent = requests.utils.default_user_agent()
        self.host = hostname
        hostblist = ["allybruener.com", "ask.arabnews.com"]
        if hostname not in hostblist:
            robotlink = "https://" + hostname + "/robots.txt"
            # headers = {}
            # headers = [useragent]
            #resp = requests.get(robotlink, headers={"HTTP_HOST":"MyHost"}, timeout=5, verify=False)
            connSt = time.time()
            session = requests.Session()
            # sys.stdout.write("         Connecting on robots... ")
            retry = Retry(connect=3, backoff_factor=0.5)
            adapter = HTTPAdapter(max_retries=retry)
            session.mount('http://', adapter)
            session.mount('https://', adapter)
            connFinish = time.time()
            connTime = connFinish - connSt
            # sys.stdout.write(" done in {} ms\n".format(connTime))

            # sys.stdout.write("         Loading... ")
            startrbtTime= time.time()
            # print('startrbtTime {} & type: {}'.format(startrbtTime, type(startrbtTime)))
            # if startrbtTime < 10:
            try:
                #resp = session.get(robotlink, headers={"HTTP_HOST":"MyHost"}, timeout=(5, 5), stream=False)
                resp = urllib.request.urlopen(robotlink)
             
                if resp.get_code() != 200:
                    return None
                    # if "content-length" in resp.headers:            
                    #     sys.stdout.write(" done in {} ms with {} bytes\n".format(round(rbt_time,2), resp.headers['content-length']))
                    # else:
                    #     sys.stdout.write(" done in {} ms with no content length\n".format(round(rbt_time,2)))
                # else:
                    # sys.stdout.write(errormsg)
                # sys.stdout.write("         Verifying header... status code {} \n".format(resp.status_code))
            except Exception as e:
                errormsg = str(e)
                return None
        
            # else:
            #     sys.stdout.write("Not Loaded \n")
        


    # connect to a remote server: IP address, port
    def connect(self, ip, port):
        if self.sock is None or ip is None:
            print("Invalid or null IP address")
            return 
        if port < 1 or port > 49151:    # Validate given Port number
            print('Invalid/Non-existent Port Number')
            sys.exit()
        try:
            conn_start = time.time()
            # print('         Connecting on page... ', end='')
            # sys.stdout.write("         Connecting on page... ")
            self.sock.connect((ip, port))   # server address is defined by (ip, port)
            conn_end = time.time()
            # sys.stdout.write('done in {} ms'.format(round((conn_end - conn_start) * 1000,2)) + '\n')
        except socket.error as e:
            print("Failed to connect: {}".format(e))
            self.sock.close() 
            self.sock = None

    # return the number of bytes sent
    def send(self, request):
        bytesSent = 0       # bytesSent is a local variable
        if self.sock is None:
            return 0
        try:
            bytesSent = self.sock.sendall(request.encode())   # encode(): convert string to bytes
        except socket.error as e:
            print("socket error in send: {}".format(e))
            self.sock.close()
            self.sock = None
        return bytesSent

    # Receive the reply from the server. Return the reply as string
    def receive(self):
        if self.sock is None:
            return ""
        reply = bytearray()    # b'', local variable, bytearray is multable
        bytesRecd = 0   # local integer

        self.sock.setblocking(0)    # flag 0 to set non-blocking mode of the socket
        ready = select.select([self.sock], [], [], TIMEOUT) # https://docs.python.org/3/library/select.html
        if ready[0] == []:     # timeout
            print("Time out on", self.host)
            return ""
        # else reader has data to read
        try:
            rcv_start = time.time()
            # sys.stdout.write("         Loading... ")
            while True:         # use a loop to receive data until we receive all data
                data = self.sock.recv(BUF_SIZE)  # returned chunk of data with max length BUF_SIZE. data is in bytes
                if data == b'':  # if empty bytes
                    break
                # elif (bytesRecd < 96000000):
                #     break
                else:
                    reply += data  # append to reply
                    bytesRecd += len(data)

            rcv_end  = time.time()
            rcv_time = (rcv_end - rcv_start) * 1000 # in ms 
            # sys.stdout.write('done in {} ms with {} bytes'.format(round(rcv_time,2), bytesRecd) + '\n')
            # sys.stdout.write("         Verifying header... ")
        except socket.error as e:
            print("socket error in receive: {}".format(e))
            self.sock.close()
            self.sock = None
        return str(reply)

    # Close socket
    def close(self):
        if not (self.sock is None):
            self.sock.close()


    def crawl(self, port, msg, host, myIp):
        self.createSocket()
        # myIp = self.getIP(host)
        self.connect(myIp, port)
        self.send(msg)
        reply = self.receive()
        return reply


"""        
        try:
            print()
            print("robotlink: ", robotlink)
            headers = {}
            headers['User-Agent'] = useragent
            
            #req = urllib.request.Request(robotlink, headers = headers)
"""            
        
            
        
            
            
"""            
        except urllib.error.HTTPError as e:
            error = e.code
            #print(error)
"""   