GIFPATH=stream/togif
mkdir $GIFPATH
rm $GIFPATH/snap*.jpg
for f in stream*.jpg; do cp "$f" $GIFPATH/"$f"; done
for f in stream*.jpg; do cp "$f" $GIFPATH/2"$f"; done
for f in stream*.jpg; do cp "$f" $GIFPATH/3"$f"; done
find stream/ -name \*.jpg -printf "%C+ %h/%f\n" | sort -r | head -n70 | awk '{print "\""$2"\""}' | xargs -I {} cp {} $GIFPATH/
mogrify -shave 0x16 -resize 500x355 $GIFPATH/snap*.jpg
python watermark.py $GIFPATH
convert -delay 15 -loop 0 -colors 16 $GIFPATH/*.jpg $GIFPATH/sunrise_im.gif
cp $GIFPATH/sunrise_im.gif /var/www/petit-prince/sunrise_im.gif

