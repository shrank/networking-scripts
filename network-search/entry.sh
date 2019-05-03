#!/bin/sh
if [ ! -e /data/.DONTOVERWRITE ]; then
cp -r /distdata/* /data/
touch /data/.DONTOVERWRITE
cat /data/cron/crontabs/root | awk '$6=="run-parts"{print $7}' | xargs mkdir -p {}
chgrp -R $DATA_GID /data/*
chmod -R g+w /data/*
find /data/ -type d -exec chmod g+s {} \;
fi
python3 app/server.py  &> /data/log/frontend.log  &
/usr/sbin/crond -f -c /data/cron/crontabs -L /data/log/cron.log 
