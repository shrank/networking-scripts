#!/bin/bash

# Runs some usefull show commands on cisco and stores the ouput in a file


user=admin
echo password for $1:
read -s password
echo collect status from $1
cat << EOF | expect -f - > status/$1.status 
set timeout 60
spawn ssh $user@$1 

expect "yes/no" { 
	send "yes\r"
	expect "*?assword" { send "$password\r" }
	} "*?assword" { send "$password\r" }
expect "#" { send "term length 0\r" }
expect "#" { send "sh int status\r" }
expect "#" { send "sh interface counters errors\r" }
expect "#" { send "sh span\r" }
expect "#" { send "sh int trunk\r" }
expect "#" { send "sh cdp neighbor\r" }
expect "#" { send "sh version\r" }
expect "#" { send "exit\r" }
EOF
