#!/bin/bash

# uses nmap to find hosts and stores them into a file
# sh find_devices.sh 10.10.0.0-255

filename=device_scan-$1
nmap -sP -oG - $1 | awk '$5=="Up"{print $2}' >> $filename
cat $filename | sort | uniq > $filename.tmp
rm $filename
mv $filename.tmp $filename
echo devices discoverd:
wc -l $filename
