GIFPATH=$1/cleangif
WWWPATH=/var/www/soixantesunrise/$1
FILELIST=$GIFPATH/images_list.txt
if ls $1/snap*.jpg > /dev/null 2>&1; then
    mkdir -p $GIFPATH
    mkdir -p $WWWPATH
    mkdir -p archives
    TS=$( date +%Y%m%d%H%M%S )
    find $1/ -name \*.jpg -printf "%C+ %h/%f\n" | sort -r | head -n70 | awk '{print ""$2""}' | sed -n '1!G;h;$p' > $FILELIST 
    LIST=$(cat $FILELIST)
    convert -delay 15 -loop 0 -colors 64 $LIST $GIFPATH/$1.gif
    mv $GIFPATH/$1.gif $WWWPATH/$1-$TS.gif
    echo "{\"last\":\"$1-$TS.gif\"}" > $WWWPATH/last.json
  else
    echo "No files in $1"
fi
exit

