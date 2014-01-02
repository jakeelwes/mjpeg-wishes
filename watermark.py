from PIL import Image, ImageDraw, ImageFont
import os
import sys
import os.path, time
import datetime
import getopt
 
def process(filename, path, original_path, name):
# Open the original image
  main = Image.open(path + '/' + filename)
  text_as_img = Image.open("mask.png")
  
# Create a new image for the watermark with an alpha layer (RGBA)
# the same size as the original image
  watermark = Image.new("RGBA", main.size)
# Get an ImageDraw object so we can draw on the image
  waterdraw = ImageDraw.ImageDraw(watermark, "RGBA")
# Place the text at (10, 10) in the upper left corner. Text will be white.
  font = ImageFont.truetype("Brandon_blk.otf", 22)
  font2 = ImageFont.truetype("Brandon_blk.otf", 16)
  modifiedTime = os.path.getmtime(original_path + '/' + filename)
  str_time = datetime.datetime.fromtimestamp(modifiedTime).strftime('%H:%M:%S')
  str_day = datetime.datetime.fromtimestamp(modifiedTime).strftime('%B %d, %Y')
  waterdraw.text((300, 304), str_time, font= font)
  waterdraw.text((46, 304), str_day.upper(), font= font)
  w, h = waterdraw.textsize(name, font=font2)
  waterdraw.text((250-w/2, 154), name, font= font2)
   
# Get the watermark image as grayscale and fade the image
# See <http://www.pythonware.com/library/pil/handbook/image.htm#Image.point>
# for information on the point() function
# Note that the second parameter we give to the min function determines
# how faded the image will be. That number is in the range [0, 256],
# where 0 is black and 256 is white. A good value for fading our white
# text is in the range [100, 200].
  #watermask = watermark.convert("L").point(lambda x: min(x, 100))
# Apply this mask to the watermark image, using the alpha filter to
# make it transparent
  #watermark.putalpha(watermask)
    
# Paste the watermark (with alpha layer) onto the original image and save it
  #main.paste(watermark, None, watermark)
  main.paste(watermark, None, watermark)
  main.paste(text_as_img, (0,0), text_as_img)
  main.save(path + '/' + filename, "JPEG")
   
if __name__ == '__main__':
  path = 'stream/togif'
  original_path = 'stream'
  name = "CENTRAL TOWER"
  try:
    opts, args = getopt.getopt(sys.argv[1:],"hp:n:",["name=", "path="])
  except getopt.GetoptError:
    print 'watermark.py -h to get help'
    sys.exit(2)
  for opt, arg in opts:
    if opt == '-h':
      print 'run "watermark.py --path myfolder" to specify a path to save images to'
      print 'run "watermark.py --name \"Paris, France\"" to specify your camera\'s IP'
      sys.exit()
    elif opt in ("-p", "--path"):
      path = arg + '/'
      original_path = path.split('/')[0] + '/'
    elif opt in ("-n", "--name"):
      name = arg.upper()
   
  file_names = sorted((fn for fn in os.listdir(path) if fn.startswith('snap')))
  for im in file_names:
    process(im, path, original_path, name)
