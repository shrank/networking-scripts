# network-search docker image
collect data from network devices with ansible and search it using a simple web-search.

## Overview
this image includes:
 - ansible to collect data from network devices
 - the netonix ansible modules from https://github.com/shrank/python_netonix_api
 - nmap for simple device discovery
 - subversion to store data
 - a simple web frontend to search the data

## Getting started
### run docker image
The image creates some basic folders and scripts if /data/ is empty. `DATA_GID` is used to define the group id of those files.
```
sudo docker run -e DATA_GID=1000 -v /srv/nw-search:/data -v /etc/localtime:/etc/localtime:ro -P murxs/network-search:0.1
```
### basic configuration
 1. edit /data/cron/contrabs/root to change the timeing for cron
   - docker images run in UTC, mount the corect file to /etc/localtime to a spcific timezone
 2. set your login credentials for your devices in /data/inventory/prod/group_vars/all/creds.yml
 
### inventory
The default inventory in all scripts is /data/inventory/prod. I use one file per group. 
Checkout the discovery script in /data/cron/examples.

### collect data
 - The plays in /data/tasks/ are an example how to collect data
 - To run the plays, use the scripts in /data/scripts
 - to run your scripts automatically, place them in a subdirectory of /data/cron/
   - check /data/cron/examples
 - the mac filters assume a very specific environment. Checkout the source-code for more details

### search your data
 - the server.py script provides a simple web search using grep within the svn working directory.