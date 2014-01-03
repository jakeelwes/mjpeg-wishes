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
  subp = subprocess.Popen(['python mjpeg2images_panasonic.py --ip ' + webcam['url'] + ':' + webcam['port'] + ' --request ' + webcam['request'] + ' --path ' + webcam['slug']], shell=True)
  webcam["process"] = psutil.Process(subp.pid)
  print "start webcam " + webcam["slug"]

def start_gif(webcam):
  if webcam.get("process_gif"):
    try:
      webcam["process_gif"].wait(1)
    except psutil.TimeoutExpired:
      #print webcam.get("process_gif")
      return
  subp = subprocess.Popen(['./generate_gif.sh ' + webcam['slug'] + ' "' + webcam['city'] + ', ' + webcam['country'] + '"'], shell=True)
  webcam["process_gif"] = psutil.Process(subp.pid)
  print "make gif " + webcam["slug"]
  
def stop_webcam(webcam):
  if webcam.get("process") and webcam["process"].is_running():
    webcam["process"].kill()
    print "stop " + webcam["slug"]

json_data=open('webcams_panasonic.json')

data = json.load(json_data)
#pprint(data)
mylist = data["webcams"]
json_data.close()
#mylist.sort(key=lambda r: parser.parse(r["sunrise"]))


for webcam in mylist:
  webcam["slug"] = slugify("pan"+webcam["url"]+webcam["city"])
  print webcam["slug"]

print ("\n")
while True:
    try:
      now = datetime.datetime.now(utc)
      #now -= datetime.timedelta(0,6*60*60)
      print now
      for webcam in mylist:
        if True:
          # start webcam if not
          start_webcam(webcam)
          # make gif
          start_gif(webcam)

      time.sleep(5)  
    except KeyboardInterrupt:
      for webcam in mylist:
        stop_webcam(webcam)
      sys.exit()

