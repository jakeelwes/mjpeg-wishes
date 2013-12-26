from PIL import Image, ImageDraw
import os
import sys
 
def process(filename):
# Open the original image
  main = Image.open(filename)
  text_as_img = Image.open("no_time.png")
  
# Create a new image for the watermark with an alpha layer (RGBA)
# the same size as the original image
  watermark = Image.new("RGBA", main.size)
# Get an ImageDraw object so we can draw on the image
  waterdraw = ImageDraw.ImageDraw(watermark, "RGBA")
# Place the text at (10, 10) in the upper left corner. Text will be white.
  waterdraw.text((10, 10), "The Image Project")
   
# Get the watermark image as grayscale and fade the image
# See <http://www.pythonware.com/library/pil/handbook/image.htm#Image.point>
# for information on the point() function
# Note that the second parameter we give to the min function determines
# how faded the image will be. That number is in the range [0, 256],
# where 0 is black and 256 is white. A good value for fading our white
# text is in the range [100, 200].
  watermask = watermark.convert("L").point(lambda x: min(x, 100))
# Apply this mask to the watermark image, using the alpha filter to
# make it transparent
  watermark.putalpha(watermask)
    
# Paste the watermark (with alpha layer) onto the original image and save it
  #main.paste(watermark, None, watermark)
  #main.paste(watermark, None, watermask)
  main.paste(text_as_img, (0,0), text_as_img)
  main.save(filename, "JPEG")
   
if __name__ == '__main__':
  path = 'stream/togif'
  if sys.argv[1]:
    path = sys.argv[1]+'/'
  file_names = sorted((fn for fn in os.listdir(path) if fn.startswith('snap')))
  for im in file_names:
    process(path + im)
