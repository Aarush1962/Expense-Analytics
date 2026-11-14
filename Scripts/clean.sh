#!/bin/bash

OriginalFile=$1
FinalFile=$2


head -n 1 "$OriginalFile" > "$FinalFile"

tail -n +2 "$OriginalFile" \
| grep -v "FAILED" \
| sed '/^$/d; s/ *, */,/g ' \
|sort -t',' -k2,2 >> "$FinalFile"  


echo  "Raw Data File is Cleaned -> $FinalFile "
