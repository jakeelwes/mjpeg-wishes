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
  subp = subprocess.Popen(['python mjpeg2images.py --ip ' + webcam['url'] + ':' + webcam['port'] + ' --request ' + webcam['request'] + ' --path ' + webcam['slug']], shell=True)
  webcam["process"] = psutil.Process(subp.pid)
  print "start webcam " + webcam["city"]

def start_gif(webcam):
  if webcam.get("process_gif"):
    try:
      webcam["process_gif"].wait(1)
    except psutil.TimeoutExpired:
      #print webcam.get("process_gif")
      return
  subp = subprocess.Popen(['./generate_gif.sh ' + webcam['slug'] + ' "' + webcam['city'] + ', ' + webcam['country'] + '"'], shell=True)
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


for webcam in mylist:
  sunrise_time = parser.parse(webcam["sunrise"]) 
  #sunrise_utc = sunrise_time.astimezone(timezone('Australia/Victoria'))
  sunrise_utc = sunrise_time.astimezone(timezone('CET'))
  print sunrise_utc.strftime("%H:%M:%S") + " / " + webcam["city"]
  webcam["starttime"] = sunrise_utc - datetime.timedelta(0,30*60) # 30 minutes 
  webcam["endtime"] = sunrise_utc + datetime.timedelta(0,90*60) # 90 minutes 
  webcam["slug"] = slugify(webcam["city"])
  print webcam["slug"]

print ("\n")
while True:
    try:
      now = datetime.datetime.now(utc)
      now -= datetime.timedelta(0,4*60*60)
      print now
      for webcam in mylist:
        if now > webcam["endtime"]:
          webcam["starttime"] += datetime.timedelta(1,0)
          webcam["endtime"] += datetime.timedelta(1,0)
          # stop process
          stop_webcam(webcam)
        if now < webcam["endtime"] and now > webcam["starttime"] :
        #if True:
          # start webcam if not
          start_webcam(webcam)
          # make gif
          start_gif(webcam)

      time.sleep(5)  
    except KeyboardInterrupt:
      for webcam in mylist:
        stop_webcam(webcam)
      sys.exit()

