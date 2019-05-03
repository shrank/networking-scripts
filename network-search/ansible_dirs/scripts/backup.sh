#!/bin/bash
sh /data/scripts/open_svn.sh
wdir=/data/workdir/config

if [ ! -e $wdir ]; then
mkdir -p $wdir
svn add $wdir
fi

for a in cisco.yml netonix.yml fortigate.yml; do
ansible-playbook -e backup_dir=$wdir -i /data/inventory/prod $1 /data/tasks/backup/$a
cd $wdir
svn add * 2> /dev/null
svn commit -m"auto-comitted by ansible $0"
cd 
done
