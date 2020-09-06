# 


from tcpsocket import TCPsocket 
from urlparser import URLparser 
from request import Request 
from queue import Queue 

def main():
    Q = Queue()
    print("number of urls: ", Q.qsize())
    ps = URLparser() 
    r = Request()
    ws = TCPsocket()

    try: 
        with open("URL-input-100.txt") as file:
            for line in file:
                Q.put(line)
    except IOError: 
        print('No such file')
        exit(1)
    count = 0
    while no Q.empty():
        url = Q.get()
        count += 1 
        print(count)
        print("url: ", url)
        host, port, path, query = ps.parse(url)
        r equest = r.getRequest(host, path, query)
        print("request: ", request)
        ws.crawl(host, port, request)
    
    if __name__ == "__main__":
        main()