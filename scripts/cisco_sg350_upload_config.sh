#!/bin/bash

# Send Config to Cisco SG350 line by line because the devices crash if you paste multiple lines at the time
# usage: sh cisco_sg350_upload_config.sh 192.168.1.55 config.txt

echo username for $1:
read user
echo password:
read -s password
echo connecting to $1
cat << EOF | expect -f -
set timeout 60
set fp [open "$2" r]
spawn ssh $1

#expect "yes/no" {
#       send "yes\r"
#       expect "User Name:" { send "$user\r" }
#       expect "*?assword:" { send "$password\r" }
#       }
expect "User Name:" { send "$user\r" }
expect "Password" { send "$password\r" }

while { [gets \$fp line] >= 0 } {
    expect "#" { send "\$line\r" }
}
expect "#" { send "exit\r" }
expect "#" { send "exit\r" }
EOF
