#!/bin/bash
target=/data/inventory/prod
filename=/data/inventory/discovery
mkdir -p $filename
filename=$filename/$1
target=$target/$1

echo [$1] > $filename
nmap -sP -oG - $2 | awk '$5=="Up"{print $2}' >> $filename
test -e $target && cat $target >> $filename
cat $filename | sort | sort -u | sort -r > $target 
