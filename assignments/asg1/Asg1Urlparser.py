'''
Team Members:
    Yassine Jaoudi
    Akpan, Samuel Cyril 
    Samantha Clark  
'''
from urllib.request import urlopen
import urllib
from bs4 import BeautifulSoup
import html
import requests, time, sys, re

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

    def responseParser(self, data):
        index = data.find('bytearray')
        if index != -1:
            data = data.strip('bytearray(b\'\'\)')
            data = data.split('\\r\\n')
            print('\n----------------------------------------------------------')
            for i in range(len(data)):
                print(data[i])

    def parsePage(self, URL):
        
        try:
            # sys.stdout.write("         Parsing Page... ")
            parseStart = time.time()
            html = urlopen(URL)
            # using BeautifulSoup
            # bsObj = BeautifulSoup(html.read(), features="lxml")
                    
            # for link in bsObj.findAll('a'):
            #     links.append(link.get('href'))
            # parseFinish = time.time()
            # timeParse = parseFinish - parseStart
           
            # Using urllib
            text = html.read()
            plaintext = text.decode('utf8')
            links = re.findall("href=[\"\'](.*?)[\"\']", plaintext)
            # print('\nLinks len: {}'.format(len(links)))
            return links
            #print(len(links)) ---shows links are being processed and added
         
            # sys.stdout.write("done in {} ms with {} links \n".format(timeParse, len(links)))
            
        except Exception as exception:
            # TODO: Add a set variable to count the error exception
            errormsg = str(exception)
            return None
        
      
        
        
