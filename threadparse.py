import revhelper
import os.path
import urllib
import imgchar
import traf
import revs
import shutil
import threading
import time

starttime = time.time()

infile = open("lookup.tmp")
names = []
for line in infile:
    names.append(line.strip())

def timgchar(playername, month, year):
    """thread worker function"""
    print 'Imgchar: %s' % playername + " at " + str(time.clock())
    imgchar.updateimgcharlookup(playername,month,year)
    return

def ttraf(playername, month, year):
    """thread worker function"""
    print 'Traf: %s' % playername + " at " + str(time.clock())
    traf.updatetraflookup(playername, month, year)
    return

def trevs(playername, month, year):
    """thread worker function"""
    print 'Revs: %s' % playername + " at " + str(time.clock())
    revs.updaterevslookup(playername, month, year)
    return

threads = []
count = 0

for name in names:
    count = count + 1
    for month in range(12,13):
        for year in range(2011,2012):
            # for each combination get revid information and update lookup
            playername = urllib.quote(name)
            print 
            print "Getting " + playername + ":" + str(month) +"," + str(year)

            t1 = threading.Thread(target=timgchar, args=(playername,month, year,))
            threads.append(t1)
            t1.start()

            t2 = threading.Thread(target=ttraf, args=(playername,month, year,))
            threads.append(t2)
            t2.start()

            t3 = threading.Thread(target=trevs, args=(playername,month, year,))
            threads.append(t3)
            t3.start()

        print
        if count % 3 == 0:
            print "waiting for threads \n"
            for thread in threading.enumerate():
                if thread is not threading.currentThread():
                    thread.join()

print "elapsed time " + str(time.time() - starttime)
