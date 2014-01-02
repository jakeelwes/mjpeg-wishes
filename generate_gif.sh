GIFPATH=$1/togif
if ls $1/snap*.jpg > /dev/null 2>&1; then
    mkdir -p $GIFPATH
    mkdir -p archives
    rm --f $GIFPATH/*.jpg
    TS=$( date +%Y%m%d%H%M%S )
    find $1/ -name \*.jpg -printf "%C+ %h/%f\n" | sort -r | head -n70 | awk '{print "\""$2"\""}' | xargs -I {} cp --preserve=timestamps {} $GIFPATH/
    for f in stream_*.jpg; do cp --preserve=timestamps "$f" $GIFPATH/"$f"; done
    for f in stream_*.jpg; do cp --preserve=timestamps "$f" $GIFPATH/2"$f"; done
    for f in stream_*.jpg; do cp --preserve=timestamps "$f" $GIFPATH/3"$f"; done
    mogrify -shave 0x16 -resize 500x355 $GIFPATH/snap*.jpg
    python watermark.py $GIFPATH
    convert -delay 15 -loop 0 -colors 64 $GIFPATH/*.jpg $GIFPATH/$1.gif
    cp $GIFPATH/$1.gif archives/$1-$TS.gif
    mv $GIFPATH/$1.gif /var/www/petit-prince/sunrise_im.gif
  else
    echo "No files in $1"
fi
exit
