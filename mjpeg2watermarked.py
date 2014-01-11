import time  
import sys
import os
import httplib  
import base64  
import StringIO  
import Image
import getopt
from PIL import Image, ImageDraw, ImageFont
import datetime
from pytz import timezone
from dateutil.tz import tzlocal
from dateutil import parser
  
class mjpeg2images:  
    path = 'stream/'
    filename = 'snap'
    extension = 'jpg'
    number = 0
    request = '/axis-cgi/mjpg/video.cgi'
    name = 'PARIS, FRANCE'
    localtime = "2014-01-07 00:03:33.923494+09:00"
    verbose = False
    lastread = ''
  
    def __init__(self, ip, username='admin', password='admin', request = '/axis-cgi/mjpg/video.cgi', path="stream/", name = 'PARIS, FRANCE', localtime = "2014-01-07 00:03:33.923494+09:00", verbose=False):  
  
        self.ip = ip  
        self.username = username  
        self.password = password  
        self.base64string = base64.encodestring('%s:%s' % (username, password))[:-1]  
        self.number = 0
        self.path = path
        self.request = request
        self.name = name
        self.localtime = str(localtime)
        self.verbose = verbose
        if not os.path.exists(self.path):
              os.makedirs(self.path)
  
    def connect(self):  
  
        h = httplib.HTTP(self.ip)  
        h.putrequest('GET',self.request)  
        if (self.username == ''):
          h.putheader('', '')  
        else:
          h.putheader('Authorization', 'Basic %s' % self.base64string)  
        h.endheaders()  
        errcode, errmsg, headers = h.getreply()  
        self.file = h.getfile()  

    def update(self):          
          isPictureFound = False
          if len(self.lastread) > 500000:
            if self.verbose:
              print "Too much data, trashing it"
              print self.lastread
            self.lastread = ''

          data = self.file.read(15000)  
          if self.verbose:
            print "Length of data: " + str(len(data))
          if len(data) == 0:
            if self.verbose:
              print "Reconnect ******************************************************"
            self.connect()
            return False
          data = self.lastread + data 
          parts = data.split('\xff\xd8')
          if self.verbose:
            print "Length of data+lastread: " + str(len(data))
            print "Number of parts: " + str(len(parts))
          for i,part in enumerate(parts):
            partsofpart = part.split('\xff\xd9')
            if len(partsofpart) < 2:
              self.lastread = partsofpart[0]
              continue
            s = '\xff\xd8' + partsofpart[0] + '\xff\xd9'
            if self.verbose:
              print str(datetime.datetime.now()) + ' '  +str(self.number)
              print "Image size: " + str(len(s))
          
                         
            p = StringIO.StringIO(s)  
            im = Image.open(p)
            try:
              im.load()
            except KeyboardInterrupt:
              self.close()
            except Exception, x:  
              pass
            im = self.process(im)
            fullpath = self.path + self.filename + ("%02d" % self.number) + '.' + self.extension
            im.save(fullpath)
            # mofrify gif
            #os.system('mogrify -format gif -colors 64 ' + fullpath)
            self.number += 1
            self.number %= 100
            p.close()  
            isPictureFound = True
          return isPictureFound
     
    def trashcurrentreadimage(self):          
      while True:
          data = self.file.read(15000)  
          if len(data) == 0:
            return 
          partsofpart = data.split('\xff\xd9')
          if len(partsofpart) < 2:
            continue
          self.lastread = partsofpart[1]
          return
                          
    def close(self):  
      sys.exit()
    def process(self, myimage):
# crop
      w, h = myimage.size
      if w < 640 or h < 480:
        myimage = myimage.transform((640,480), Image.EXTENT,(0,0,w,h),Image.NEAREST)
        w, h = myimage.size
      w2,h2 = 640,440
      myimage = myimage.crop((w/2 - w2/2, h/2 - h2/2, w/2 + w2/2, h/2 + h2/2))
      myimage.thumbnail((500,344), Image.ANTIALIAS)

      text_as_img = Image.open("mask.png")
      
# Create a new image for the watermark with an alpha layer (RGBA)
# the same size as the original image
      watermark = Image.new("RGBA", myimage.size)
# Get an ImageDraw object so we can draw on the image
      waterdraw = ImageDraw.ImageDraw(watermark, "RGBA")
# Place the text at (10, 10) in the upper left corner. Text will be white.
      font = ImageFont.truetype("Brandon_blk.otf", 22)
      font2 = ImageFont.truetype("Brandon_blk.otf", 16)
      modifiedTime = datetime.datetime.now().replace(tzinfo=tzlocal())
      modifiedTime = modifiedTime.astimezone(parser.parse(self.localtime).tzinfo)
      str_time = modifiedTime.strftime('%H:%M:%S')
      str_day = modifiedTime.strftime('%B %d, %Y')
      waterdraw.text((300, 304), str_time, font= font)
      waterdraw.text((46, 304), str_day.upper(), font= font)
      w, h = waterdraw.textsize(self.name, font=font2)
      waterdraw.text((250-w/2, 174), self.name, font= font2)
       
      myimage.paste(watermark, None, watermark)
      myimage.paste(text_as_img, (0,0), text_as_img)
      return myimage
      
def main(argv):
  nowindow = False
  host = '216.123.238.207'
  path = 'stream/'
  request = '/axis-cgi/mjpg/video.cgi'
  screen = ''
  name = 'PARIS, FRANCE'
  localtime = "2014-01-07 00:03:33.923494+09:00"
  verbose=False

  try:
    opts, args = getopt.getopt(argv,"hi:p:r:n:t:v",["ip=", "path=", "request=", "name=", "localtime=", "verbose"])
  except getopt.GetoptError:
    print 'mjpeg2images.py -h to get help'
    sys.exit(2)
  for opt, arg in opts:
    if opt == '-h':
      print 'run "mjpeg2images.py --ip 127.0.0.1" to specify your camera\'s IP'
      print 'run "mjpeg2images.py --path myfolder" to specify a path to save images to'
      print 'run "mjpeg2images.py --ip 127.0.0.1  --request /axis-cgi/mjpg/video.cgi" to specify a custom request'
      sys.exit()
    elif opt in ("-n", "--nowindow"):
        nowindow = True
    elif opt in ("-i", "--ip"):
      host =  arg
    elif opt in ("-p", "--path"):
      path = arg + '/'
    elif opt in ("-r", "--request"):
      request = arg
    elif opt in ("-n", "--name"):
      name = arg.upper()
    elif opt in ("-t", "--localtime"):
      localtime = arg
    elif opt in ("-v", "--verbose"):
      verbose = True
  camera = mjpeg2images(host, '', '', request, path, name, localtime, verbose)  
  camera.connect()  
    
  while True:  
    try:
      before = time.time()
    
      while not camera.update():
        #time.sleep(.1)  
        pass
      functiontime = time.time() - before
      sleeptime = 2.3 - functiontime
      if sleeptime > 0:
        #print "sleep " + str(sleeptime)
        camera.trashcurrentreadimage()
        time.sleep(sleeptime)  
    except KeyboardInterrupt:
      camera.close()

if __name__ == '__main__':
	main(sys.argv[1:])
