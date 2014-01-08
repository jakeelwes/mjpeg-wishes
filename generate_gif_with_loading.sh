GIFPATH=$1/cleangif
WWWPATH=/var/www/soixantesunrise/$1
GIFMAILPATH=/var/www/soixantesunrise/
if ls $WWWPATH/*.gif > /dev/null 2>&1; then
    GIF=find $WWWPATH/ -name \*.gif -printf "%C+ %h/%f\n" | sort -r | head -n1 | awk '{print "\""$2"\""}' 
    convert -delay 15 -loop 0 -colors 64 loading.gif $GIF $GIFPATH/$1_im.gif
    mv $GIFPATH/$1_im.gif /var/www/soixantesunrise/sunrise_im.gif
  else
    echo "No files in $1"
fi
exit

