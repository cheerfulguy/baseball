import json
import os.path
import urllib2

def updatetraflookup(playername, month, year):

    month = "%0.2d" % (month) 
    somedate = str(year)+str(month)

    filename = 'dumps/traffic/' + playername+"_"+somedate+'.json'

    # date like "200811"
    # fetch the file from wikipedia only if that file does not exist
    getfile(playername,somedate)
        
    average = gettraf(playername,month,year)
    if  average == -1:

        jsondata = open(filename,'r')
        jsonobj = json.load(jsondata)
        daily_views = jsonobj['daily_views']
    
        count = 0
        total = 0

        for day, views in daily_views.iteritems():
            total = views + total
            count = count + 1

        if count !=0:
            average = total/count
            average = "%.3f" % average
        else:
            average = 0

        writetraf(playername,month,year,average)

def getfile(playername, somedate):

    filename = 'dumps/traffic/' + playername+"_"+somedate+'.json'
    if os.path.exists(filename):
        pass
    else:
        query = "http://stats.grok.se/json/en/" + somedate +"/"+playername
        print query
        page = urllib2.urlopen(query)
        jsondata = open(filename,'w+')
        jsondata.write(page.read())
        jsondata.close()


        
def gettraf(playername, month, year):
    
    lookupfile = "lookups/traf.csv"
    lookup = open(lookupfile,"r")

    traf = -1
    
    for line in lookup:
        line = line.strip()
        items = line.split("\t")

        if len(items)>3 and items[0]==playername:
            if items[1]==str(month):
                if items[2]==str(year):
                    if items[3]!="":
                        traf = items[3]

    return traf

def writetraf(playername,month,year,traf):
    lookupfile = "lookups/traf.csv"
    lookup = open(lookupfile,"a")
    line = playername + "\t" + str(month) + "\t" + str(year) + "\t" + str(traf) + "\n"
    lookup.write(line)
    print "wrote traffic :" + line