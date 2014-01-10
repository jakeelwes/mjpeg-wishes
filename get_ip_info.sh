ALL=$(echo $1 | sed -n "s/http:\/\///p" | sed -n "s/^\([^:\/]\+\)\(:\([^\/]\+\)\)\?\(\/.*$\)/\1 \3 \4/p")
set $ALL
IP=$1
PORT=$2
REQUEST=$3
if [ -z "$PORT" ]; then
  PORT=80
fi
COUNTRY=$(geoiplookup $IP | sed -n 's/GeoIP Country Edition: .*, \(.*\)$/\1/p')
DATA=$(geoiplookup $IP -f /usr/local/share/GeoIP/GeoIPCity.dat)
CITY=$(echo $DATA | sed -n 's/GeoIP City Edition, .*: .*, .*, \(.*\), .*, \(.*\), \(.*\), .*, .*$/\1/p')
LAT=$(echo $DATA | sed -n 's/GeoIP City Edition, .*: .*, .*,\(.*\), .*, \(.*\), \(.*\), .*, .*$/\2/p')
LONG=$(echo $DATA | sed -n 's/GeoIP City Edition, .*: .*, .*,\(.*\), .*, \(.*\), \(.*\), .*, .*$/\3/p')
SUNRISE=$( w3m "google.com/search?q=sunrise:$CITY" | sed -n 's/[^0-9]*\([0-9]\+:[0-9]\+\).* (\(.*\)) - Sunrise in.*/\1 \2/p' )
echo  {
 echo     \"url\" : \"$IP\",
 echo     \"request\" : \"$REQUEST\",
 echo     \"port\" : \"$PORT\",
echo    \"sunrise\": \"$SUNRISE\",
 echo     \"city\" : \"$CITY\",
 echo     \"country\" : \"$COUNTRY\",
 echo     \"website\" : \"\",
 echo     \"location\" : {
 echo       \"lat\" : $LAT,
 echo       \"lng\" : $LONG
 echo     }
 echo   },
