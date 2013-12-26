mkdir togif
find stream/ -name \*.jpg -printf "%C+ %h/%f\n" | sort -r | head -n20 | awk '{print "\""$2"\""}' | xargs -I {} cp {} togif/
