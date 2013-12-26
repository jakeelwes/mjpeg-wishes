GIFPATH=stream/togif
mkdir $GIFPATH
rm $GIFPATH/snap*.jpg
find stream/ -name \*.jpg -printf "%C+ %h/%f\n" | sort -r | head -n70 | awk '{print "\""$2"\""}' | xargs -I {} cp {} $GIFPATH/
mogrify -shave 0x16 -resize 500x355 $GIFPATH/*.jpg
python watermark.py $GIFPATH
convert -delay 10 -loop 0 -colors 16 $GIFPATH/*.jpg $GIFPATH/sunrise_im.gif
cp $GIFPATH/sunrise_im.gif /var/www/petit-prince/sunrise_im.gif

