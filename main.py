'''
Created on Dec 15, 2011

@author: computerex
'''
import neopetslogger
import time
import sys
import glob
import os

if __name__ == '__main__':
    np = neopetslogger.Neopets()
    np.htp.track_progress=True
    if ( np.neoLogin("", "") == True):
        print("Logged in!!")
        items = []
        try:
            os.chdir("./shops")
            shoplist = glob.glob("*.txt")
            for shop in shoplist:
                nameandsymb = os.path.splitext(os.path.basename(shop))
                inx = len(items)
                items.append([nameandsymb[0]]) 
                itemfile = open(shop, "r")
                for line in itemfile:
                    line = str(line).replace("\n","")
                    if len(line) > 0:
                        items[inx].append(line)
                itemfile.close()
            for i in range(0, len(items)):
                print("\n"+"shop: "  + items[i][0])
                for j in range(3, len(items[i])):
                    print(items[i][j])
        except:
            print(sys.exc_info()[0])
            exit()
        print()
        print()
        while 1 == 1:
            for i in range(0, len(items)):
                time.sleep(5)
                urlreq = "http://www.neopets.com/objects.phtml?type=shop&obj_type="+items[i][0]
                np.debugString(np.htp.GET(urlreq), filename='output.html')
                inputfile = open("output.html", "rb")
                inputstr = str(inputfile.read())
                inputfile.close()
                if np.isloggedin(inputstr) == False:
                    print("Connection lost! Terminating...")
                    break
                filelen = len(inputstr)
                pos, posbreak = 0, 0
                lookfor = " in stock<BR>Cost: "
                lookforlen = len(lookfor)
                breakstr = "<B>"
                breakstrlen = len(breakstr)
                itemsinstock = []
                itemcost=0
                while 1==1:
                    pos = inputstr.find(lookfor, pos, filelen)
                    if pos == -1 :
                        break
                    itemcost=int(int(inputstr[pos+lookforlen:inputstr.find("NP", pos+lookforlen)-1].replace(",", "").replace(" ", "")))
                    posbreak = inputstr[0:pos].rfind(breakstr)
                    if posbreak == -1:
                        pos+=lookforlen+1
                        continue
                    posbreak+=breakstrlen
                    itemstr = inputstr[posbreak:inputstr.find("</B>", posbreak, filelen)]
                    if items[i][1] == "negate" or items[i][1] == "match" or items[i][1] == "partialmatch":
                        for j in range(3, len(items[i])):
                            if items[i][1] == "match":
                                if items[i][j].lower() == itemstr.lower():
                                    print("Shop " + items[i][0] + ": " + itemstr + " has just restocked!! Get it now!")
                            elif items[i][1] == "negate":
                                if items[i][j].lower() != itemstr.lower():
                                    print("Shop " + items[i][0] + ": " + itemstr + " has just restocked!! Get it now!")
                            elif items[i][1] == "partialmatch":
                                memtest = items[i][j].lower()
                                if itemstr.lower().find(items[i][j].lower()) != -1:
                                    print("Shop " + items[i][0] + ": " + itemstr + " has just restocked!! Get it now!")
                                
                    elif items[i][1] == "greaterorequal":
                        if int(items[i][2]) <= itemcost:
                            print("Shop " + items[i][0] + ": " + itemstr + " has just restocked!! Get it now!")
                    elif items[i][1] == "everything":
                        print("Shop " + items[i][0] + ": " + itemstr + " has just restocked!! Get it now!")
                    else:
                        print("Error!! Unknown comparison mode!")
                    pos+=lookforlen
                    itemsinstock.append(itemstr)
                print("Shop " + items[i][0] + ": " + str(len(itemsinstock)) + " items in stock")
                itemsinstock = []
            print("\n\n\n")
    else:
        print("Loggin failure!!!")
    
    
