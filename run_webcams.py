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

def start_webcam(webcam):
  if webcam.get("process") and webcam["process"].is_running():
    return
  mjpeg2images_script = 'mjpeg2watermarked.py'
  subp = subprocess.Popen(['python ' + mjpeg2images_script + ' --ip ' + webcam['url'] + ':' + webcam['port'] + ' --request ' + webcam['request'] + ' --path ' + webcam['slug'] + ' --name "' + webcam['city'] + ', ' + webcam['country'] + '" --localtime "'+ str(parser.parse(webcam["sunrise"])) + '"' ], shell=True)
  webcam["process"] = psutil.Process(subp.pid)
  print "************************ start webcam " + webcam["city"]

def start_gif(webcam):
  if webcam.get("process_gif"):
    try:
      webcam["process_gif"].wait(1)
    except psutil.TimeoutExpired:
      #print webcam.get("process_gif")
      return
  print "make gif " + webcam["city"]
  subp = subprocess.Popen(['./generate_clean_gif.sh ' + webcam['slug'] ], shell=True)
  
  webcam["process_gif"] = psutil.Process(subp.pid)
 

def start_gif_blocking(webcam):
  print "make gif " + webcam["city"]
  os.system('./generate_clean_gif.sh ' + webcam['slug'])
  
 
def start_gifmail(webcam):
  if webcam.get("process_gifmail"):
    try:
      webcam["process_gifmail"].wait(1)
    except psutil.TimeoutExpired:
      #print webcam.get("process_gif")
      return
  subp = subprocess.Popen(['./generate_gif_with_loading.sh ' + webcam['slug'] ], shell=True)
  
  webcam["process_gifmail"] = psutil.Process(subp.pid)
  print "make gif mail" + webcam["city"]
  
def stop_webcam(webcam):
  if webcam.get("process") and webcam["process"].is_running():
    webcam["process"].kill()
    print "stop " + webcam["city"]

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

# remove down cameras
for webcam in mylist[:]:
  if webcam.get("down"):
    mylist.remove(webcam)

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

# slugify
for webcam in mylist:
  webcam["slug"] = slugify(webcam["city"])

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

for webcam in mylist:
  sunrise_time = parser.parse(webcam["sunrise"]) 
  #sunrise_utc = sunrise_time.astimezone(timezone('Australia/Victoria'))
  sunrise_utc = sunrise_time.astimezone(timezone('CET'))
  print sunrise_utc.strftime("%H:%M:%S") + " / " + webcam["city"]
  #webcam["starttime"] = sunrise_utc - datetime.timedelta(0,30*60) # 30 minutes 
  #webcam["endtime"] = sunrise_utc + datetime.timedelta(0,90*60) # 90 minutes 
  webcam["starttime"] = sunrise_utc
for i, webcam in enumerate(mylist):
  webcam["endtime"] = mylist[(i+1)%len(mylist)]["starttime"]
  print webcam["starttime"]
  print webcam["endtime"]


for i, webcam in enumerate(mylist):
  start_webcam(webcam)
print ("\n")
while True:
    try:
      now = datetime.datetime.now(timezone('CET'))
      #now -= datetime.timedelta(0,6*60*60)
      print now
      for i, webcam in enumerate(mylist):
        # start webcam if not
        start_webcam(webcam)
        start_gif_blocking(webcam)
        if now > webcam["endtime"]:
          webcam["starttime"] += datetime.timedelta(1,0)
          webcam["endtime"] = mylist[(i+1)%len(mylist)]["starttime"]
          mylist[(i-1)%len(mylist)]["endtime"] = webcam["starttime"] 
        if now < webcam["endtime"] and now > webcam["starttime"] :
          # make gif
          start_gifmail(webcam)

      #time.sleep(30)  
    except KeyboardInterrupt:
      for webcam in mylist:
        stop_webcam(webcam)
      sys.exit()

