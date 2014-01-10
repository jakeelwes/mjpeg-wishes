import time  
import sys
import os
import httplib  
import base64  
import StringIO  
import Image
import pygame  
from pygame.locals import *  
import getopt
  
class mjpegviewer:  
    path = 'stream/'
    filename = 'snap'
    extension = 'jpg'
    number = 0
    request = '/axis-cgi/mjpg/video.cgi'
    nowindow = False
    lastread = ''
  
    def __init__(self, ip, username='admin', password='admin', request = '/axis-cgi/mjpg/video.cgi', path=0, nowindow=False):  
  
        self.ip = ip  
        self.username = username  
        self.password = password  
        self.base64string = base64.encodestring('%s:%s' % (username, password))[:-1]  
        self.number = 0
        self.path = path
        self.request = request
        self.nowindow = nowindow
        if not os.path.exists(self.path):
              os.makedirs(self.path)
  
    def connect(self):  
  
        h = httplib.HTTP(self.ip)  
        h.putrequest('GET',self.request)  
        h.putheader('Authorization', 'Basic %s' % self.base64string)  
        h.endheaders()  
        errcode, errmsg, headers = h.getreply()  
        self.file = h.getfile()  
  
    def update(self, window, size, offset):          
          
          data = self.lastread+self.file.read(15000)  
          parts = data.split('\xff\xd8')
          for i,part in enumerate(parts):
            partsofpart = part.split('\xff\xd9')
            if len(partsofpart) < 2:
              self.lastread = partsofpart[0]
              continue
            s = '\xff\xd8' + partsofpart[0] + '\xff\xd9'
                  
            if self.path != 0:
              p = StringIO.StringIO(s)  
              im = Image.open(p)
              try:
                im.load()
              except KeyboardInterrupt:
                self.close()
              except Exception, x:  
                pass
              fullpath = self.path + self.filename + ("%04d" % self.number) + '.' + self.extension
              im.save(fullpath)
              self.number += 1

            if not self.nowindow:

              try:  
                  p = StringIO.StringIO(s)  
                  campanel = pygame.image.load(p).convert()  
                  #pygame.image.save(campanel,fullpath)
                  campanel = pygame.transform.scale(campanel, size)  
                  window.blit(campanel, offset)  
            
              except KeyboardInterrupt:
                self.close()
              except Exception, x:  
                  print x  
                    
            p.close()  
              
    def close(self):  
      sys.exit()
      
def main(argv):
  nowindow = False
  host = 'skywave-lr-rkr.skywavebroadband.net:8888'
  path = 'stream/'
  request = '/axis-cgi/mjpg/video.cgi'
  request = "/nphMotionJpeg?Resolution=640x480"
  screen = ''

  try:
    opts, args = getopt.getopt(argv,"hni:p:r:",["nowindow", "ip=", "path=", "request="])
  except getopt.GetoptError:
    print 'mjpegviewer.py -h to get help'
    sys.exit(2)
  for opt, arg in opts:
    if opt == '-h':
      print 'run "mjpegviewer.py --nowindow" for a x-less run'
      print 'run "mjpegviewer.py --ip 127.0.0.1" to specify your camera\'s IP'
      print 'run "mjpegviewer.py --path myfolder" to specify a path to save images to'
      print 'run "mjpegviewer.py --ip 127.0.0.1  --request /axis-cgi/mjpg/video.cgi" to specify a custom request'
      sys.exit()
    elif opt in ("-n", "--nowindow"):
        nowindow = True
    elif opt in ("-i", "--ip"):
      host =  arg
    elif opt in ("-p", "--path"):
      path = arg + '/'
    elif opt in ("-r", "--request"):
      request = arg


  pygame.init()  
      
  if not nowindow:
    screen = pygame.display.set_mode((660,500), 0, 32)  
    pygame.display.set_caption('mjpegviewer.py')  
      
    background = pygame.Surface((660,500))  
    background.fill(pygame.Color('#E8E8E8'))  
    screen.blit(background, (0,0))  
    
  camera = mjpegviewer(host, '', '', request, path, nowindow)  
  camera.connect()  
    
  while True:  
    try:
    
      camera.update(screen, (640,480), (10,10))  
      pygame.display.update()  
    
      for event in pygame.event.get():  
        if event.type == QUIT:  
          sys.exit(0)  
            
      time.sleep(.01)  
    except KeyboardInterrupt:
      camera.close()

if __name__ == '__main__':
	main(sys.argv[1:])
