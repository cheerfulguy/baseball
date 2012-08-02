import revhelper
import os.path
import urllib
import imgchar
import traf
import revs
import shutil
import time

# i added this on ec2
# names = ["Hank Aaron","Yogi Berra", "Joe Coleman"]

starttime = time.time()
infile = open("lookup.tmp")

names = []

for line in infile:
    names.append(line.strip())

#shutil.move("lookups/revid.csv","lookups/revid_old.csv")

for name in names:
    for month in range(12,13):
        for year in range(2006,2012):
            # for each combination get revid information and update lookup
            playername = urllib.quote(name)
            print "Processing " + playername + ":" + str(month) +"," + str(year)
            revhelper.updaterevlookup(playername, month, year)
            
this gets longform revision files based on lookup
print "HOLDUP : Here come all the big files"
revhelper.getrevfiles()

# for name in names:
#     for month in range(12,13):
#         for year in range(2006,2012):
#             # for each combination get revid information and update lookup
#             playername = urllib.quote(name)
#             print "Getting " + playername + ":" + str(month) +"," + str(year)

#             imgchar.updateimgcharlookup(playername,month,year)
#             traf.updatetraflookup(playername, month, year)
#             revs.updaterevslookup(playername, month, year)

print "elapsed time " + str(time.time() - starttime)

            
