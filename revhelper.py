import time 
import xml.dom.minidom as minidom
import datetime
import re
import os.path
import urllib2
import threading

#takes a players name and a date and writes revision info in a file if it doesnt exist

def updaterevlookup(playername, month, year):

    dateutc = time.mktime((year, month, 1, 0, 0, 0, 0, 0, 0))
    
    # get the file containing revid if it does not exist
    filename = writerevinfo(playername, dateutc)
    lookupfile = "lookups/revid.csv"
    lookup = open(lookupfile,"r")

    flag = 0
    for line in lookup:
        line = line.strip()
        items = line.split("\t")

        if len(items)>3 and items[0]==playername:
            if items[1]==str(month):
                if items[2]==str(year):
                    if items[3]!="":
                        flag = 1 ## all OK, revid exists
                        revid = items[3]

    if flag == 0:
        revid = parserevs(filename)
        lookup = open(lookupfile,"a")
        line = ""
        line = playername + "\t" + str(month) + "\t" + str(year) + "\t" + str(revid) + "\n"
        lookup.write(line)

        
def writerevinfo(playername, dateutc):

    filename = 'dumps/revdata/' + playername+"_"+str(dateutc)[:-2]+'.xml'

    if os.path.exists(filename):
        pass
    else:
        query = "http://en.wikipedia.org/w/api.php?action=query&prop=revisions&rvlimit=1&rvprop=timestamp|ids&format=xml&rvstart="+str(dateutc)[:-2]+"&titles="+playername
        print query
        print "getting " + playername + "\n------------------------\n"
        page = urllib2.urlopen(query)
        revdata = open(filename,'w+')
        revdata.write(page.read())

    return filename
        

# returns the revid from a given revision file 
def parserevs(filename): 
    print "now parsing " + filename
    doc = minidom.parse(filename)
    page = doc.getElementsByTagName("page")

    title = page[0].getAttribute("title")
    pageid = page[0].getAttribute("pageid")

    #print title, pageid
    revs = doc.getElementsByTagName("rev")
    #return revid = 0 if page did not exist
    revid = 0

    for rev in revs:
        revid = rev.getAttribute("revid")
        timestamp = rev.getAttribute("timestamp")
        parentid = rev.getAttribute("parentid")
    
    #print revid, timestamp, title, pageid
    return revid

# thread helper function
def worker(playername, revid):
    """thread worker function"""
    query = "http://en.wikipedia.org/w/index.php?oldid="+str(revid)
    print "getting revision file :" + playername + "_"+ str(revid)
    page = urllib2.build_opener()
    page.addheaders = [('User-agent', 'Mozilla/5.0')]
    result = page.open(query)
    revdumps = "dumps/revdumps/" + playername + "_" + str(revid)
    revdumpdata = open(revdumps,'w+')
    revdumpdata.write(result.read())
    revdumpdata.close()
    return


# creates physical files from lookup
def getrevfiles(cutoff):
    
    count = 0
    filename = "lookups/revid_small.csv"
    lookup = open(filename,"r")
    threads = []


    for line in lookup:
        count = count + 1
        items = line.strip().split("\t")
        if len(items)>3: 
            revid = items[3]
            playername = items[0]
            revdumps = "dumps/revdumps/" + playername + "_" + str(revid)
            if os.path.exists(revdumps) | int(revid) == 0:
                print "not downloading again for " + playername + "_" + revid
                pass
            else:
                t = threading.Thread(target=worker, args=(playername,revid,))
                threads.append(t)
                t.start()

        print
        if count % 30 == 0:
            print "waiting for threads \n-------------------------"
            for thread in threading.enumerate():
                if thread is not threading.currentThread():
                    thread.join()

        if count > cutoff:
            return
                
def getrevid(playername, month, year):
    
    lookupfile = "lookups/revid.csv"
    lookup = open(lookupfile,"r")

    revid = -1
    
    for line in lookup:
        line = line.strip()
        items = line.split("\t")

        if len(items)>3 and items[0]==playername:
            if items[1]==str(month):
                if items[2]==str(year):
                    if items[3]!="":
                        revid = items[3]

    return revid
