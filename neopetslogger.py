import HttpClient
import sys

class Neopets:
    
    htp = HttpClient.HTTP()

    def debugString( self, msg, filename='debug.html' ):
        try:
            fileWrite = open(filename, 'wb' )
            fileWrite.write( msg.encode("utf8") )
            fileWrite.close()
        except:
            print( str(sys.exc_info()[1]) )
    def isloggedin(self, page):
        return True if page.find("Welcome, ") >= 0 else False
            
    def neoLogin( self, username, password ):
        loginHtml = self.htp.POST( "http://www.neopets.com/login.phtml", {"destination" :  "", "username" : username, "password" : password } )[1]
        self.debugString( loginHtml )
        return self.isloggedin(loginHtml)
