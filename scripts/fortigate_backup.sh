#!/bin/bash

# fetch config from a fortigate device

user=admin
echo password for $1:
read -s password
echo collect status from $1
cat << EOF | expect -f - > wlc/$1.config
set timeout 60
spawn ssh $user@$1 

expect "yes/no" { 
	send "yes\r"
	expect "*?assword" { send "$password\r" }
	} "*?assword" { send "$password\r" }
expect "#" { send "sh running-config\r" }
expect "#" { send "exit\r" }
EOF
