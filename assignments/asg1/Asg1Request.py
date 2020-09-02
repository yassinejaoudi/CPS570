
'''
Team Members:
    Yassine Jaoudi
    Akpan, Samuel Cyril  
'''

import sys

class Request:
    def __init__(self):
        self.request = ''    # a string

    def getRequest(self, host, path, query):
        """Build an HTTP GET request """
        self.request = 'GET ' + path + query + ' HTTP/1.0' +  '\nHost: ' + host + '\nConnection: close\n\n'
        try:
            return self.request
        except ValueError:
            print('Non-HTTP Reply...')

    def headRequest(self, host):
        """Build a HEAD request, to check if host has "robots.txt" file """
        self.request = 'HEAD /robots.txt HTTP/1.0\n' + 'Host: ' + host + '\n\n'
        return self.request

    def cleanStr (self, data):
        """Cleans the data str recieved from the request()"""
        self.http = 'HTTP/1.0'
        self.date = 'Date:'
        self.svr  = 'Server:'
        self.cache = 'Cache-Control:'
        self.Cont = 'Content-Type:'
        self.lang = 'Content-Language:'
        self.lct  = 'Location:'
        self.len  = 'Content-Length'
        self.str_end = '\r)'

        
        idx = data.find('HTTP/1.0')
        if idx != -1:
            self.http = data[idx:data.find(self.date)-4]
            idx_end = data.find(self.http[-1:-4]+'\r\n')
            # print('idx_end: ',idx_end)
            data = data[:idx_end]

        idx = data.find('Date:')
        if idx != -1:
            self.date = data[idx:data.find(self.svr)-4]
            idx_end = data.find(self.date[-1:-4]+'\r\n')
            data = data[:idx_end]

        idx = data.find('Server:')
        if idx != -1:
            self.svr = data[idx:data.find(self.cache)-4]
            idx_end = data.find(self.svr[-1:-4]+'\r\n')
            data = data[:idx_end]

        idx = data.find('Cache-Control:')
        if idx != -1:
            self.cache = data[idx:data.find(self.Cont)-4]
            idx_end = data.find(self.cache[-1:-4]+'\r\n')
            data = data[:idx_end]

        idx = data.find('Content-Type:')
        if idx != -1:
            self.Cont = data[idx:data.find(self.lang)-4]
            idx_end = data.find(self.Cont[-1:-4]+'\r\n')
            data = data[:idx_end]
        
        idx = data.find('Content-Language:')
        if idx != -1:
            self.lang = data[idx:data.find(self.lct)-4]
            idx_end = data.find(self.lang[-1:-4]+'\r\n')
            data = data[:idx_end]
        
        idx = data.find('Cache-Control:')
        if idx != -1:
            self.lang = data[idx:data.find(self.lct)-4]
            idx_end = data.find(self.lang[-1:-4]+'\r\n')
            data = data[:idx_end]
        
        idx = data.find('Location:')
        if idx != -1:
            self.lct = data[idx:data.find(self.len)-4]
            idx_end = data.find(self.lct[-1:-4]+'\r\n')
            data = data[:idx_end]

        idx = data.find('Content_Length:')

        if idx != -1:
            self.len = data[data.find(self.lct)-2:idx]
            print('Content Length: {} & LCT: {}'.format(idx,data.find(self.lct)-2))
            idx_end = data.find(self.len[-1:-4]+'\r\n')
            data = data[idx_end:]

        print('\n-----------------------------------------------------\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n' \
                .format(self.http, self.date, self.svr,self.cache,self.Cont,\
                    self.lct,self.len))