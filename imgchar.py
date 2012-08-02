import os.path
import re
from BeautifulSoup import BeautifulSoup 
import time
import revhelper

def updateimgcharlookup(playername, month, year):

    dateutc = time.mktime((year, month, 1, 0, 0, 0, 0, 0, 0))

    lookupfile = "lookups/imgchar.csv"
    lookup = open(lookupfile)

    flag = 0
    for line in lookup:
        line = line.strip()
        items = line.split("\t")

        if len(items)>4 and items[0]==playername:
            if items[1]==str(month):
                if items[2]==str(year):
                    if items[3]!="":
                        flag = 1 ## all OK, img exists
                        img = items[3]
                    if items[3]!="":
                        flag = flag + 2 ## all OK, char exists
                        char = items[4]

    lookup.close()

    if flag != 3:

        revid = revhelper.getrevid(playername,month,year)
        filename = "dumps/revdumps/" + playername + "_" + str(revid)
        filedata = open(filename,'r')
        content = filedata.read()
        soup = BeautifulSoup(content)

        if flag == 2:
            char = getcharsizeinfo(soup)

        if flag == 1:
            img = getimginfo(soup)

        if flag == 0:
            char = getcharsizeinfo(soup)
            img = getimginfo(soup)
            
        lookup = open(lookupfile,"a")
        line = ""
        line = playername + "\t" + str(month) + "\t" + str(year) + "\t" + str(img) + "\t" + str(char) + "\n"
        lookup.write(line)
        print "wrote : " + line

def getimginfo(soup):

    #return len(soup.findAll("img","thumbimage"))
    images = soup.find(id="bodyContent").findAll("img")

    # remove duplicates
    images = list(set(images))
    imgcount = 0

    # count only those images that are greater than 75px
    for image in images:
        try:
            if int(image["width"])>75:
                imgcount = imgcount + 1
            #print "true " + str(imgcount) + " " + image["width"] 
            #print image["src"]
        except:
            pass
    
    # return number of images
    return imgcount

# takes soup and returns charactersize
def getcharsizeinfo(soup):

    #return len(soup.findAll("img","thumbimage"))
    text = str(soup.find('div', id="bodyContent"))
    # return number of characters
    return len(text)

