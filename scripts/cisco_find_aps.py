#!/usr/bin/python
"""
find known MAC-Adresses on cisco switches

The primary goal of this script is to find known devices(e.g. Wifi APs) in the mac-address table. 
It compairs all MACs against a list of known devices and assumes that all ports with 
maximum 2 known devices are edge port. Those edge-ports with the mac and ip information 
are return as the result.

This filter assumes a very specific environment:
 - the known adress file must be in format of the mikrotik static lease configuration export
 - it assumes all devices with mac "80:5e:c0:*:*:*" as known devices(voip phones) 
 - the switch IP is prepended to each output line
 - known mac file is hard-coded
 - input file is a "sh mac address" output from a cisco switch
 
"""

import json
import sys
import re
import traceback
import time
import os


def read_file(f):
	res={}
	f=open(f)
	for l in f:
		a=l.split(" ")
		ip=""
		mac=""
		comment=""
		for i in a:
			if(i.startswith("address=")):
				ip=i.split("=")[1].strip()
			if(i.startswith("mac-address=")):
				mac=i.split("=")[1].strip()
			if(i.startswith("comment=")):
				comment=i.split("=")[1].strip()
		if(mac!=""):
			res[mac.lower()]=(ip.lower(),mac.lower(),comment)
	return res 
	

if __name__ == '__main__':
	ip=sys.argv[1]
	macs=read_file("190408-leases.rsc")
	target=[]
	
	print("%s\t%s\t%s\t%s\t%s"%("Switch","Port","MAC","IP DHCP","IP Switch"))
	for f in os.listdir(ip):
		mac_all={}
		with open(ip+"/"+f) as source:
			for line in source:
				line=line.strip()
				line=re.sub(' +',' ',line)
				b=line.split(" ")
				try:
					a=b[1].replace(".","")
					mac="%s:%s:%s:%s:%s:%s"%(a[0:2],a[2:4],a[4:6],a[6:8],a[8:10],a[10:12])
					mac_all[mac]={"MAC":mac,"Port":b[3],"Last_IP":""}
				except:
					continue
		res={}
		for pm in mac_all.keys():
			current_mac=mac_all[pm]
			try:
				current_mac["AP_IP"]=macs[pm][0]
			except:
				if(not pm.startswith("80:5e:c0:")):
					continue
				current_mac["AP_IP"]="unknown"
			try:
				res[current_mac["Port"]][pm]=current_mac
			except:
				res[current_mac["Port"]]={pm:current_mac}
		for a in res.keys():
			if(len(res[a])<3):
				for ml in res[a].keys():
					i=res[a][ml]
					print("%s\t%s\t%s\t%s\t%s"%(f.strip(".mac"),i["Port"],i["MAC"].replace("-",":").lower(),i["AP_IP"],i["Last_IP"]))
