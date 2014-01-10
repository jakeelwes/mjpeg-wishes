SLUG=$1
GIFPATH=$SLUG/cleangif
WWWPATH=/var/www/soixantesunrises/$SLUG
FILELIST=$GIFPATH/images_list.txt
if ls $SLUG/snap*.jpg > /dev/null 2>&1; then
    mkdir -p $GIFPATH
    mkdir -p $WWWPATH
    mkdir -p archives
    TS=$( date +%Y%m%d%H%M%S )
    find $SLUG/ -name \*.jpg -printf "%C+ %h/%f\n" | sort -r | head -n70 | awk '{print ""$2""}' | sed -n '1!G;h;$p' > $FILELIST 
    LIST=$(cat $FILELIST)
    convert -delay 15 -loop 0 -colors 64 $LIST $GIFPATH/$SLUG.gif
    mv $GIFPATH/$SLUG.gif $WWWPATH/last.gif
    #cp $WWWPATH/last.gif $WWWPATH/$SLUG-$TS.gif
    set $LIST
    cp $SLUG/${68} $WWWPATH/last_.jpg
    mv $WWWPATH/last_.jpg $WWWPATH/last.jpg
    echo "{\"last\":\"$SLUG-$TS.gif\"}" > $WWWPATH/last.json
  else
    echo "No files in $SLUG"
fi
exit

