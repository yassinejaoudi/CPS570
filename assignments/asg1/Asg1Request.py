
'''
Team Members:
    Yassine Jaoudi
    Akpan, Samuel Cyril  
'''

class Request:
    def __init__(self):
        self.request = ''    # a string

    def getRequest(self, host, path, query):
        """Build an HTTP GET request """
        self.request = 'GET ' + path + query + ' HTTP/1.0' +  '\nHost: ' + host + '\nConnection: close\n\n'
        return self.request

    def headRequest(self, host):
        """Build a HEAD request, to check if host has "robots.txt" file """
        self.request = 'HEAD /robots.txt HTTP/1.0\n' + 'Host: ' + host + '\n\n'
        return self.request