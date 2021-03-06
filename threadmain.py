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

infile = open("listu_part.csv")
names = []
for line in infile:
    names.append(line.strip())

def worker(playername, month, year):
    """thread worker function"""
    print 'Worker: %s' % playername + " at " + str(time.clock())
    revhelper.updaterevlookup(playername, month, year)
    return

threads = []
count = 0

for name in names:
    count = count + 1
    for month in range(14,13):
        for year in range(2006,2012):
            # for each combination get revid information and update lookup
            playername = urllib.quote(name)
            print "Processing " + playername + ":" + str(month) +"," + str(year)

            t = threading.Thread(target=worker, args=(playername,month, year,))
            threads.append(t)
            t.start()

    print
    if count % 5 == 0:
        print "waiting for threads \n"
        for thread in threading.enumerate():
            if thread is not threading.currentThread():
                thread.join()

print "HOLDUP : Here come all the big files"
revhelper.getrevfiles(40000)

# for name in names:
#     for month in range(12,13):
#         for year in range(2006,2012):
#             # for each combination get revid information and update lookup
#             playername = urllib.quote(name)
#             print "Getting " + playername + ":" + str(month) +"," + str(year)


#             t = threading.Thread(target=worker, args=(playername,month, year,))
#             threads.append(t)
#             t.start()

#             imgchar.updateimgcharlookup(playername,month,year)
#             traf.updatetraflookup(playername, month, year)
#             revs.updaterevslookup(playername, month, year)

print "elapsed time " + str(time.time() - starttime)
