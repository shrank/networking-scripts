"""
find known MAC-Adresses Filter for ansible

This is free and unencumbered software released into the public domain.

Anyone is free to copy, modify, publish, use, compile, sell, or
distribute this software, either in source code form or as a compiled
binary, for any purpose, commercial or non-commercial, and by any
means.

In jurisdictions that recognize copyright laws, the author or authors
of this software dedicate any and all copyright interest in the
software to the public domain. We make this dedication for the benefit
of the public at large and to the detriment of our heirs and
successors. We intend this dedication to be an overt act of
relinquishment in perpetuity of all present and future rights to this
software under copyright law.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.

For more information, please refer to <http://unlicense.org/>


Description:

The primary goal of this filter is to find known devices(e.g. Wifi APs) in the mac-address table. 
It compairs all MACs against a list of known devices and assumes that all ports with 
maximum 2 known devices are edge port. Those edge-ports with the mac and ip information 
are return as the result.

This filter assumes a very specific environment:
 - the known adress file must be in format of the mikrotik static lease configuration export
 - it assumes all devices with mac "80:5e:c0:*:*:*" as known devices(voip phones)
 - find_ap() assumes the input data is structured like the netonix mac-table 
 - the first parameter to find_ap() is prepended to each output line
 - cisco_mac2dict() create a netonix like data structure from a cisco "sh mac address"
 
 exmples:
 	
  tasks:
  - name: get mac table
    block:
     - netonix_command:
         username: "{{ ansible_user}}"
         password: "{{ ansible_password}}"
         target: "{{ inventory_hostname }}"
         command:  mac
       register: output
     - local_action: copy content='{{output.output | find_ap(inventory_hostname,'/data/dhcp_leases.rsc') }}' dest="{{output_dir}}/{{ inventory_hostname }}.mac"

  tasks:
  - name: get mac table
    block:
     - ios_command:
         commands: 
           - sh mac address
       register: output
     - local_action: copy content='{{output.stdout[0] | cisco_mac2dict | find_ap(inventory_hostname,'/data/dhcp_leases.rsc') }}' dest="{{output_dir}}/{{ inventory_hostname }}.mac"

"""

import json
import sys
import re

def _read_mikrotik_file(f):
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
	
def cisco_mac2dict(value):
	mac_all={}
	if(not isinstance(value, list)):
		value=value.split("\n")
		for line in value:
				line=line.strip()
				line=re.sub(' +',' ',line)
				b=line.split(" ")
				try:
					a=b[1].replace(".","")
					mac="%s:%s:%s:%s:%s:%s"%(a[0:2],a[2:4],a[4:6],a[6:8],a[8:10],a[10:12])
					mac_all[mac]={"MAC":mac,"Port":b[3],"Last_IP":""}
				except:
					continue
	return mac_all
def find_ap(value,ip="",macfile=None):
	macs={}
	if(macfile!=None):
		macs=_read_mikrotik_file(macfile)
	res={}
	for pm in value.keys():
		current_mac=value[pm]
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
	ret=""
	ip+="\t"
	for a in res.keys():
		if(len(res[a])<3):
			for ml in res[a].keys():
				i=res[a][ml]
				ret+="%s%s\t%s\t%s\t%s\n"%(ip,i["Port"],i["MAC"].replace("-",":").lower(),i["AP_IP"],i["Last_IP"])
	return ret
	
# ---- Ansible filters ----
class FilterModule(object):
	''' find devices in file from mac table '''
	filter_map = {
		'find_ap': find_ap,
		'cisco_mac2dict': cisco_mac2dict
	}

	def filters(self):
		return self.filter_map
		