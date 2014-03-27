__author__ = 'computerex'

import urllib
import gzip
import http.cookiejar
import socket
import io
import sys

socket.setdefaulttimeout(10)

class HTTP:

    def __init__(self):
        self.USER_AGENT = "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/533.4 (KHTML, like Gecko) Chrome/5.0.375.86 Safari/533.4"
        self.Cookie_Jar = http.cookiejar.LWPCookieJar()
        self.opener = None
        self.track_progress = False
        self.init()
    def init(self):
        self.opener = self.getopener()
    def setrefer (self, Ref = ""):
        if  self.opener == None :
            return
        self.opener.addheaders = [('User-Agent', self.USER_AGENT), ('Accept-Encoding', 'gzip'), ('Referer', Ref)]
    def eatcookies (self):
        self.Cookie_Jar.clear_session_cookies()
    def getopener(self):
        opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(self.Cookie_Jar))
        opener.addheaders = [('User-Agent', self.USER_AGENT), ('Accept-Encoding', 'gzip')]
        return opener

    def POST (self, URL, Data):
        if Data.__class__ == dict:
            Data = urllib.parse.urlencode(Data)
            Data = Data.encode( 'utf8' ) # Fix for version 3.2. Convert to bytes.
        return self.GET(URL, Data)

    def GET (self, URL, Data = None, enc = "utf-8"):
        if self.track_progress == True:
            self.setrefer(URL)
        try:
            request = urllib.request.Request(URL, Data)
            contents = self.opener.open(request)
            headers = dict(contents.info())
            source = contents.read()
            if headers.get("Content-Encoding") == "gzip":
                try:
                    packedbytes = io.BytesIO(source)
                    source = gzip.GzipFile(fileobj = packedbytes).read()
                except:
                    print("Error decoding GZip.\nURL: " + URL + "\nData: " + Data + "\n\n")
            if "text" not in headers.get("Content-Type"):
                return [headers, source]
            else:
                return [headers,str(source, enc)]
        except:
            print(sys.exc_info()[1])
            return None
