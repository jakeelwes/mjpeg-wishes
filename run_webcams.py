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

def start_webcam(webcam):
  if webcam.get("process") and webcam["process"].is_running():
    return
  mjpeg2images_script = 'mjpeg2images.py'
  if webcam['request'][0:4] == '/nph':
    mjpeg2images_script = 'mjpeg2images_panasonic.py'
    print mjpeg2images_script 
  subp = subprocess.Popen(['python ' + mjpeg2images_script + ' --ip ' + webcam['url'] + ':' + webcam['port'] + ' --request ' + webcam['request'] + ' --path ' + webcam['slug']], shell=True)
  webcam["process"] = psutil.Process(subp.pid)
  print "start webcam " + webcam["city"]

def start_gif(webcam):
  if webcam.get("process_gif"):
    try:
      webcam["process_gif"].wait(1)
    except psutil.TimeoutExpired:
      #print webcam.get("process_gif")
      return
  subp = subprocess.Popen(['./generate_gif.sh ' + webcam['slug'] + ' "' + webcam['city'] + ', ' + webcam['country'] + '" "'+ str(parser.parse(webcam["sunrise"])) + '"' ], shell=True)
  
  webcam["process_gif"] = psutil.Process(subp.pid)
  print "make gif " + webcam["city"]
  
def stop_webcam(webcam):
  if webcam.get("process") and webcam["process"].is_running():
    webcam["process"].kill()
    print "stop " + webcam["city"]

json_data=open('webcams.json')

data = json.load(json_data)
#pprint(data)
mylist = data["webcams"]
json_data.close()
mylist.sort(key=lambda r: parser.parse(r["sunrise"]))

#print datetime.datetime.utcnow().replace(tzinfo=timezone("UTC")).astimezone((parser.parse(mylist[0]["sunrise"]).tzinfo))

for webcam in mylist:
  sunrise_time = parser.parse(webcam["sunrise"]) 
  #sunrise_utc = sunrise_time.astimezone(timezone('Australia/Victoria'))
  sunrise_utc = sunrise_time.astimezone(timezone('CET'))
  print sunrise_utc.strftime("%H:%M:%S") + " / " + webcam["city"]
  #webcam["starttime"] = sunrise_utc - datetime.timedelta(0,30*60) # 30 minutes 
  #webcam["endtime"] = sunrise_utc + datetime.timedelta(0,90*60) # 90 minutes 
  webcam["starttime"] = sunrise_utc
  webcam["slug"] = slugify(webcam["city"])
  print webcam["slug"]
for i, webcam in enumerate(mylist):
  webcam["endtime"] = mylist[(i+1)%len(mylist)]["starttime"]
  print webcam["starttime"]
  print webcam["endtime"]
print ("\n")
while True:
    try:
      now = datetime.datetime.now(timezone('CET'))
      #now -= datetime.timedelta(0,6*60*60)
      print now
      for i, webcam in enumerate(mylist):
        if now > webcam["endtime"]:
          webcam["starttime"] += datetime.timedelta(1,0)
          webcam["endtime"] = mylist[(i+1)%len(mylist)]["starttime"]
          mylist[(i-1)%len(mylist)]["endtime"] = webcam["starttime"] 
          # stop process
          stop_webcam(webcam)
          # clean folder
          subp = subprocess.Popen(['rm --f -r ' + webcam['slug']], shell=True)
        if now < webcam["endtime"] and now > webcam["starttime"] - datetime.timedelta(0,60) :
          # start webcam if not
          start_webcam(webcam)
        if now < webcam["endtime"] and now > webcam["starttime"] :
          # make gif
          start_gif(webcam)

      time.sleep(5)  
    except KeyboardInterrupt:
      for webcam in mylist:
        stop_webcam(webcam)
      sys.exit()

