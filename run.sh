#!/bin/sh
 
PROJECTPATH='/home/petitprince/apps/mjpeg-wishes'
LAUNCHCOMMAND='cpulimit -l 240 python run_webcams.py &'

if ps ax | grep -v grep | grep '/bin/$PROJECTPATH' 
then
echo "found" 
else
cd $PROJECTPATH
$LAUNCHCOMMAND
fi
