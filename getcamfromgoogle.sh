function google { Q="$@"; GOOG_URL='https://www.google.de/search?tbs=li:1&num=100&q='; AGENT="Mozilla/4.0"; stream=$(curl -A "$AGENT" -skLm 100 "${GOOG_URL}${Q//\ /+}" | grep -oP '\/url\?q=.+?&amp' | sed 's|/url?q=||; s|&amp||'); echo -e "${stream//\%/\x}"; }

google inurl:nphMotionJpeg | sed -n 's/http:\/\/\([^\/]*\)\/nph[mM]otion[jJ]peg.*$/\1/p' | while read line; do sh get_ip_info.sh $line;done > webcams_panasonic.json
