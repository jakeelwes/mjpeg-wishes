import os
import json
from pprint import pprint
import time
from dateutil import parser
from pytz import timezone,utc
import datetime
import subprocess
import psutil
import sys
from slugify import slugify
import ephem  
import glob


def listdir_fullpath(d):
    files = glob.iglob(d+'/*.[jJ][Pp][gG]')
    return [os.path.join("", f) for f in files]

def get_sunrise(webcam):
  o=ephem.Observer()  
  o.lat=str(webcam['location']['lat'])
  o.long=str(webcam['location']['lng'])
  s=ephem.Sun()  
  s.compute()  
  #print ephem.localtime(o.previous_rising(s))
  #print ephem.localtime(o.next_rising(s))
  sunrise = o.next_rising(s).datetime().replace(tzinfo=timezone("UTC")).astimezone((parser.parse(webcam["sunrise"]).tzinfo))
  return sunrise

json_data=open('webcams.json')

data = json.load(json_data)
#pprint(data)
mylist = data["webcams"]
json_data.close()

# slugify
for webcam in mylist:
  webcam["slug"] = slugify(webcam["city"])

# remove down cameras
for webcam in mylist[:]:
  print webcam["city"]
  remove = False
  if (webcam.get("down") == 1):
    remove = True
    print "user sets down in file"
  try:
    get_sunrise(webcam)
  except ephem.AlwaysUpError:
    remove = True
    print "sun never starts"
  if not os.path.exists(webcam["slug"]):
    remove = True
    print "folder does not exist"
  else:
    files = listdir_fullpath(webcam["slug"])
    if len(files) == 0:
        remove = True
        print "no files"
    else:
      newest = max(files, key = os.path.getctime)
      print os.path.getctime(newest) 
      print time.time()
      if (time.time() - os.path.getctime(newest) > 3600):
        remove = True
        print "files too old!"
  if remove == True:
    mylist.remove(webcam)
    print "remove " + webcam["city"]



#calculate sunrise
for webcam in mylist:
  #print webcam["city"]
  #print webcam["sunrise"]
  webcam["sunrise"] = get_sunrise(webcam).strftime("%H:%M:%S %z")
  #print webcam["sunrise"]


# sort
mylist.sort(key=lambda r: parser.parse(r["sunrise"]))

for webcam in mylist:
  sunrise_time = parser.parse(webcam["sunrise"]) 
  #sunrise_utc = sunrise_time.astimezone(timezone('Australia/Victoria'))
  sunrise_utc = sunrise_time.astimezone(timezone('CET'))
  print sunrise_utc.strftime("%H:%M:%S") + " / " + webcam["city"]

#print datetime.datetime.utcnow().replace(tzinfo=timezone("UTC")).astimezone((parser.parse(mylist[0]["sunrise"]).tzinfo))


# write json for website
if not os.path.exists("/var/www/soixantesunrises"):
  os.makedirs("/var/www/soixantesunrises")
print "Number of webcams: " + str(len(mylist)) 
try:
  outfile=open('/var/www/soixantesunrises/webcams.json','w')
  json.dump(mylist,outfile)
except:
  pass
outfile.close()
