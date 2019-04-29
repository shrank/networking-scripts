#!/bin/bash

#fetch a backup(tar) from a netonix wisp switch

user=admin
filename=backups/$1.ncfg
echo password for $1:
read -s password

curl --insecure --data "username=$user&password=$password" --cookie-jar cookies  https://$1/index.php
curl --insecure --cookie cookies -o $filename https://$1/api/v1/backup/$1
