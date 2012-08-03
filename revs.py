import os.path
import urllib2
import time
import calendar
import xml.dom.minidom as minidom

def updaterevslookup(playername, month, year):

    # this gets how many days there were in that month
    monthrange = calendar.monthrange(year, month)[1]

    datestart = time.mktime((year, month, 1, 0, 0, 0, 0, 0, 0))
    dateend = time.mktime((year, month, monthrange, 0, 0, 0, 0, 0, 0))

    if getrevs(playername,month,year)==-1:
        count = getrevcount(playername,datestart,dateend)
        writerevs(playername, month, year, count)

def getrevcount(playername,datestart,dateend):
    
    filename2 = 'dumps/revdata_long/' + playername+"_"+str(datestart)[:-2]+'.xml'

    count = 0
    cont_flag = 1
    uniqueid = str(datestart)[:-2]
    urlstring = "rvstart="+str(dateend)[:-2]

    while cont_flag>0:
        if os.path.exists(filename2):
            pass
        else:
            query = "http://en.wikipedia.org/w/api.php?action=query&prop=revisions&rvlimit=500&format=xml&rvprop=timestamp%7Cuser%7Csize%7Cflags&"+urlstring+"&rvend="+str(datestart)[:-2]+"&rvcontinue&titles="+playername
            print query
            print "\n getting revs: " + playername  + "\n------------------------\n"
            cur_page = urllib2.urlopen(query)
            revdata = open(filename2,'w+')
            revdata.write(cur_page.read())
            revdata.close()
            
        revdata = open(filename2,'r')
        doc = minidom.parse(revdata)
        rvcont = doc.getElementsByTagName("query-continue")

        if len(rvcont)>0:
            revisions = rvcont[0].getElementsByTagName("revisions")
            rvstartid = revisions[0].getAttribute("rvstartid")
            urlstring = "rvstartid=" + str(rvstartid)
            uniqueid = rvstartid
            cont_flag = 1
            filename2 = 'dumps/revdata_long/' + playername+"_"+str(uniqueid)+'.xml'
        else:
            cont_flag = 0


    cont_flag = 1
    count = 0
    uniqueid = str(datestart)[:-2]

    while cont_flag>0:

        filename2 = 'dumps/revdata_long/' + playername+"_"+str(uniqueid)+'.xml'
        revdata = open(filename2,'r')
        doc = minidom.parse(revdata)

        count = count + len(doc.getElementsByTagName("rev"))

        rvcont = doc.getElementsByTagName("query-continue")

        if len(rvcont)>0:
            revisions = rvcont[0].getElementsByTagName("revisions")
            rvstartid = revisions[0].getAttribute("rvstartid")
            urlstring = "rvstartid=" + str(rvstartid)
            uniqueid = rvstartid
            cont_flag = 1
        else:
            cont_flag = 0

    return count

def getrevs(playername, month, year):
    
    lookupfile = "lookups/revs.csv"
    lookup = open(lookupfile,"r")

    revs = -1
    
    for line in lookup:
        line = line.strip()
        items = line.split("\t")

        if len(items)>3 and items[0]==playername:
            if items[1]==str(month):
                if items[2]==str(year):
                    if items[3]!="":
                        revs = items[3]

    return revs

def writerevs(playername,month,year,revs):
    lookupfile = "lookups/revs.csv"
    lookup = open(lookupfile,"a")
    line = playername + "\t" + str(month) + "\t" + str(year) + "\t" + str(revs) + "\n"
    lookup.write(line)
    print "wrote revisions :" + line
