#!/bin/bash

# configure timezone and syslog on a netonix wisp switch

user=admin
echo password for $1:
read -s password
echo configure on $1
cat << EOF | expect -f - 
set timeout 60
spawn ssh $user@$1

expect "yes/no" { 
	send "yes\r"
	expect "*?assword" { send "$password\r" }
	} "*?assword" { send "$password\r" }

expect "#" { send "configure\r" }
expect "(config)#" { send "syslog host 10.0.0.1\r" }
expect "(config)#" { send "syslog port 514\r"}
expect "(config)#" { send "timezone PST8PDT\r"}
expect "(config)#" { send "end\r"}
expect "Press ENTER to confirm configuration change." { send "\r" }
expect "#" { send "exit\r" }
EOF
