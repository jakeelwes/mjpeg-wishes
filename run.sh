#!/bin/sh
 
PROJECTPATH='/home/petitprince/apps/mjpeg-wishes'
SCRIPT='run_webcams.py'
LAUNCHCOMMAND="python $SCRIPT &"

if ps ax | grep -v grep | grep "$SCRIPT" 
then
echo "found" 
else
cd $PROJECTPATH
$LAUNCHCOMMAND
fi
