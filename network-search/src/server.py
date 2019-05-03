# Python 3 server example
from http.server import BaseHTTPRequestHandler, HTTPServer
import time
from urllib import parse
import subprocess
import re
import os
hostName = ''
serverPort = 80
MAC_File="/data/ALL_DEVICES_MAC-PORT_LIST.txt"
data_dir="/data/workdir/"

class MyServer(BaseHTTPRequestHandler):
	def do_GET(self):
		query_components = parse.parse_qs(parse.urlparse(self.path).query)
		result=""
		q=""
		if("q" in query_components.keys()):
			q=query_components['q'][0]
			q=q.replace("'","")
			if(os.path.isfile(MAC_File)):
				response = subprocess.run("grep -i '%s' %s"%(q,MAC_File), stdout=subprocess.PIPE, shell=True)
				result+="<h3>MAC Tables\n</h3>"
				result+="<pre>"			
				result+="Switch\tPort\tMAC\tDHCP IP\t IP\n"
				result+=response.stdout.decode("utf-8")
				result+="</pre>"			
			if(os.path.isdir(os.path.join(data_dir,"config"))):
				result+="\n\n<h3>From Configuration:</h3>\n"			
				response = subprocess.run("grep -i -B 3 -C 3 '%s' config/*"%q, stdout=subprocess.PIPE, shell=True,cwd=data_dir)
				result+="<pre>"			
				result+=response.stdout.decode("utf-8")
				result+="</pre>"			
			if(os.path.isdir(os.path.join(data_dir,"status"))):
				result+="\n\n<h3>From Baseline Data:</h3>\n"			
				result+="<pre>"			
				response = subprocess.run("grep -i '%s' status/*"%q, stdout=subprocess.PIPE, shell=True,cwd=data_dir)
				result+=response.stdout.decode("utf-8")
				result+="</pre>"			
		result=result.replace("\n","<br/>")
		result = re.sub(r'(status/)?([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+)', r'<a href="https://\2">\2</a>', result)
		result=result.replace(q,"<strong>%s</strong>"%q)
		searchfield="<form name='myform' method='get'>Search:<input type='text' name='q' value='%s'/><input type='submit' name='btn' value='go'/></form>"%q

		self.send_response(200)
		self.send_header("Content-type", "text/html")
		self.end_headers()
		self.wfile.write(bytes("<html><head><title>Search network data</title></head>", "utf-8"))
		self.wfile.write(bytes("<body OnLoad='document.myform.q.focus();'>", "utf-8"))
		self.wfile.write(bytes(searchfield, "utf-8"))
		self.wfile.write(bytes(result, "utf-8"))
		self.wfile.write(bytes("</body></html>", "utf-8"))

if __name__ == "__main__":        
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
