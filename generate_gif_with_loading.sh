GIFPATH=$1/cleangif
WWWPATH=/var/www/soixantesunrises/$1
GIFMAILPATH=/var/www/soixantesunrises/
if ls $WWWPATH/*.gif > /dev/null 2>&1; then
    #GIF=$(find $WWWPATH/ -name \*.gif -printf "%C+ %h/%f\n" | sort -r | head -n1 | awk '{print ""$2""}') 
    GIF=last.gif
    convert -delay 15 -loop 0 -colors 64 loading.gif $GIF $GIFPATH/$1_im.gif
    mv $GIFPATH/$1_im.gif /var/www/soixantesunrises/sunrise_im.gif
  else
    echo "No gif for $1, can't create mailgif"
fi
exit

