# takes a players name and a date and writes revision info in a file if it doesnt exist
def writerevinfo(playername, dateutc):

    filename = 'dumps/revdata/' + playername+"_"+str(dateutc)[:-2]+'.xml'

    if os.path.exists(filename):
        pass
    else:
        query = "http://en.wikipedia.org/w/api.php?action=query&prop=revisions&rvlimit=1&rvprop=timestamp|ids&format=xml&rvstart="+str(dateutc)[:-2]+"&titles="+playername
        print "getting " + playername + "\n------------------------\n"
        page = urllib2.urlopen(query)
        revdata = open(filename,'w+')
        revdata.write(page.read())

# returns the revid from a given revision file 
def parserevs(filename): 
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

def getrevfile(playername, revid):

    filename = 'dumps/revdumps/' + playername + "_" + str(revid)+'.html'

    # fetch the file from wikipedia only if that file does not exist
    if os.path.exists(filename):
        #print "data exists. not downloading again for "+ revid
        pass
    else:
        query = "http://en.wikipedia.org/w/index.php?oldid="+str(revid)
        print query
        page = urllib2.build_opener()
        page.addheaders = [('User-agent', 'Mozilla/5.0')]
        result = page.open(query)
        revdumpdata = open(filename,'w+')
        revdumpdata.write(result.read())
        revdumpdata.close()
