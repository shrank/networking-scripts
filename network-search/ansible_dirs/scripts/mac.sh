#!/bin/bash
cd /data
sh /data/scripts/open_svn.sh
wdir=/data/workdir/mac

if [ ! -e $wdir ]; then
mkdir -p $wdir
svn add $wdir
fi

target_file=/data/ALL_DEVICES_MAC-PORT_LIST.txt
old_file=/data/ALL_DEVICES_MAC-PORT_LIST.txt_old
for a in cisco.yml netonix.yml; do
ansible-playbook -e output_dir=$wdir -i /data/inventory/prod $1 /data/tasks/mac/$a
cd $wdir
svn add * 2> /dev/null
svn commit -m"auto-comitted by ansible $0"
cd 
done

mv $target_file $old_file
cat  $old_file $wdir/* | sort | sort -u >  $target_file
rm  $old_file
