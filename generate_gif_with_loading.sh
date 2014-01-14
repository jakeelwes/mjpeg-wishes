GIFPATH=$1/cleangif
WWWPATH=/var/www/soixantesunrises/$1
WWWPATHROOT=/var/www/soixantesunrises
GIFMAILPATH=/var/www/soixantesunrises
FILELIST=$GIFPATH/images_list.txt
if ls $WWWPATH/*.gif > /dev/null 2>&1; then
    #GIF=$(find $WWWPATH/ -name \*.gif -printf "%C+ %h/%f\n" | sort -r | head -n1 | awk '{print ""$2""}') 
    GIF=last.gif
    convert -delay 15 -loop 0 -colors 64 loading.gif $WWWPATH/$GIF $GIFPATH/$1_im.gif
    mv $GIFPATH/$1_im.gif $GIFMAILPATH/sunrise_im.gif
    # facebook jpg
    LIST=$(cat $FILELIST)
    set $LIST
    cp ${68} $WWWPATHROOT/sunrise_im_600x315_.jpg
    mogrify -resize 650x -crop 600x315+25+0 $WWWPATHROOT/sunrise_im_600x315_.jpg
    mv  $WWWPATHROOT/sunrise_im_600x315_.jpg $WWWPATHROOT/sunrise_im_600x315.jpg
  else
    echo "No gif for $1, can't create mailgif"
fi
exit

