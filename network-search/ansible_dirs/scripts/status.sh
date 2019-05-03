#!/bin/bash
cd /data
sh /data/scripts/open_svn.sh
wdir=/data/workdir/status

if [ ! -e $wdir ]; then
mkdir -p $wdir
svn add $wdir
fi

for a in cisco.yml netonix.yml fortigate.yml; do
ansible-playbook -e status_dir=$wdir -i /data/inventory/prod $1 /data/tasks/status/$a
cd $wdir
svn add * 2> /dev/null
svn commit -m"auto-comitted by ansible $0"
cd 
done
