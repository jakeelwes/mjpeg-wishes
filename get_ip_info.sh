COUNTRY=$(geoiplookup $1 | sed -n 's/GeoIP Country Edition: .*, \(.*\)$/\1/p')
DATA=$(geoiplookup $1 -f /usr/local/share/GeoIP/GeoIPCity.dat)
CITY=$(echo $DATA | sed -n 's/GeoIP City Edition, .*: .*, .*,\(.*\), .*, \(.*\), \(.*\), .*, .*$/\1/p')
LAT=$(echo $DATA | sed -n 's/GeoIP City Edition, .*: .*, .*,\(.*\), .*, \(.*\), \(.*\), .*, .*$/\2/p')
LONG=$(echo $DATA | sed -n 's/GeoIP City Edition, .*: .*, .*,\(.*\), .*, \(.*\), \(.*\), .*, .*$/\3/p')
SUNRISE=$( w3m "google.com/search?q=sunrise:$CITY" | sed -n 's/.*\([0-9]\+:[0-9]\+\).* (\(.*\)) - Sunrise in.*/\1 \2/p' )
echo  {
 echo     \"url\" : \"$1\",
 echo     \"request\" : \"/axis-cgi/mjpg/video.cgi\",
 echo     \"port\" : \"80\",
echo    \"sunrise\": \"$SUNRISE\",
 echo     \"name\" : \"$CITY, $COUNTRY\",
 echo     \"website\" : \"\",
 echo     \"location\" : {
 echo       \"lat\" : $LAT,
 echo       \"lng\" : $LONG
 echo     }
 echo   },
