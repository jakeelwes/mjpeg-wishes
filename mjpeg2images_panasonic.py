import time  
import sys
import os
import httplib  
import base64  
import StringIO  
import Image
import getopt
  
class mjpeg2images:  
    path = 'stream/'
    filename = 'snap'
    extension = 'jpg'
    number = 0
    request = '/axis-cgi/mjpg/video.cgi'
  
    def __init__(self, ip, username='admin', password='admin', request = '/axis-cgi/mjpg/video.cgi', path="stream/"):  
  
        self.ip = ip  
        self.username = username  
        self.password = password  
        self.base64string = base64.encodestring('%s:%s' % (username, password))[:-1]  
        self.number = 0
        self.path = path
        self.request = request
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
          
        data = self.file.readline()  
        if data[0:7] == 'Content':  
            s = self.file.read(1)      
            while s[0] != chr(0xff):  
              s = self.file.read(1)      
            s = [s]
            endofjpeg = False
            while endofjpeg != True:
                s[len(s):] = [self.file.read(1)]      
                if s[len(s)-1] == chr(0xff):
                  s[len(s):] = [self.file.read(1)]      
                  if s[len(s)-1] == chr(0xd9):
                    endofjpeg = True
            s = ''.join(s)
                          
            p = StringIO.StringIO(s)  
            im = Image.open(p)
            try:
              im.load()
            except KeyboardInterrupt:
              self.close()
            except Exception, x:  
              pass
            fullpath = self.path + self.filename + ("%02d" % self.number) + '.' + self.extension
            im.save(fullpath)
            self.number += 1
            self.number %= 100
            p.close()  
              
    def close(self):  
      sys.exit()
      
def main(argv):
  nowindow = False
  host = '216.123.238.207'
  path = 'stream/'
  request = '/axis-cgi/mjpg/video.cgi'
  screen = ''

  try:
    opts, args = getopt.getopt(argv,"hi:p:r:",["ip=", "path=", "request="])
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
   
  camera = mjpeg2images(host, '', '', request, path)  
  camera.connect()  
    
  while True:  
    try:
    
      camera.update()  
      time.sleep(.01)  
    except KeyboardInterrupt:
      camera.close()

if __name__ == '__main__':
	main(sys.argv[1:])
