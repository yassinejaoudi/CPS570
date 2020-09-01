# urlparser.py
class URLparser:
    
    def __init__(self):
        self.port = 80

    def parse(self, string): # string is a url
        self.query = '' # default query is an empty string
        self.path = '/' # default path
        self.host = '' # host is always defined for valid URLs
        index = string.find('\n')
        if index != -1:
            string = string[:index] # remove line break that is in the end of one line
        
        # remove 'http://' or 'https://' if it is present in the URL given
        index = string.find('://')
        if index != -1:
            string = string[index+3:]
        
        # remove fragment from url
        index = string.find('#')
        if index != -1: # if it found a fragment
            string = string[:index] # strip fragment
        
        # remove user:pass@ if exists
        index = string.find('@')
        if index != -1:
            string = string[index + 1:]

        # get query first, then remove query from url
        index = string.find('?')
        if index != -1: # if found a query
            self.query = string[index:] # get the query
            string = string[:index] # remove the query from the string
        
        # get path next, remove path from url
        index = string.find('/')
        if index != -1:
            self.path = string[index:]
            string = string[:index]

        # get port
        index = string.find(':')
        if index != -1:
            self.port = string[index + 1:]
            string = string[:index]


        # get host …
        self.host = string
        
        return self.host, int(self.port), self.path, self.query