import json
from pprint import pprint
import time
from dateutil import parser
from pytz import timezone

def compare(a, b):
  a_time = parser.parse(a["sunrise"]) 
  a_utc = a_time.astimezone(timezone('UTC'))
  b_time = parser.parse(b["sunrise"]) 
  b_utc = b_time.astimezone(timezone('UTC'))
  return a_utc.date() < b_utc.date()


json_data=open('webcams.json')

data = json.load(json_data)
#pprint(data)
mylist = data["webcams"]
mylist.sort(key=lambda r: parser.parse(r["sunrise"]))


for webcam in mylist:
  sunrise_time = parser.parse(webcam["sunrise"]) 
  #sunrise_utc = sunrise_time.astimezone(timezone('Australia/Victoria'))
  sunrise_utc = sunrise_time.astimezone(timezone('CET'))
  print sunrise_utc.strftime("%H:%M:%S") + " / " + webcam["name"]
json_data.close()
