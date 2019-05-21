import os
import shutil
import subprocess
from queue import SimpleQueue
import re

class SVNBackend():
	def __init__(self,workdir,repo,workers=10):
		self.num_workdirs=workers
		self.workdir=os.path.abspath(workdir)
		self.repo=os.path.abspath(repo)
		self._createRepo()
		self.workers=SimpleQueue()
		for i in range(self.num_workdirs):
			self.freeWorkdir(SVNWorkdir(os.path.join(self.workdir,"wd%d"%i),self.repo))
	def _createRepo(self):
		if(os.path.isdir(self.repo)):
			ret=subprocess.run(["svnadmin", "info",self.repo],capture_output=True)
			if(ret.returncode==0):
				return
		try:
			os.makedirs(self.repo)
		except FileExistsError:
			pass
		ret=subprocess.run(["svnadmin", "create",self.repo])
		if(ret.returncode!=0):
			raise Exception("unable to create repository: %s"%self.repo)
	def getWorkdir(self):
		return self.workers.get()
	def freeWorkdir(self,wd):
		wd.cleanup()
		self.workers.put(wd)
	def addFile(self,collection,object_id,content):
		wd=self.getWorkdir()
		o= wd.openFile(collection,object_id,'w+')
		o.write(content)
		wd.closeAndCommit(o)
		self.freeWorkdir(wd)	
	def getFile(self,collection,object_id):
		wd=self.getWorkdir()
		res=""
		try:
			with wd.openFile(collection,object_id,'r') as o:
				res+=o.read()
		except:
			res=""
		self.freeWorkdir(wd)
		return res
	def getCollections(self):
		wd=self.getWorkdir()
		res=wd.loadCollections()
		self.freeWorkdir(wd)
		return res
	def search(self,query,collection=None):
		q = re.compile(query,re.IGNORECASE)
		wd=self.getWorkdir()
		res={}
		if(collection==None):
			collections=wd.loadCollections()
		else:
			collections=[collection]
		for c in collections:
			objects=wd.loadObjects(c)
			for o in objects:
				lc=0
				f=wd.openFile(c,o,'r')
				for l in f:
					lc+=1
					match=q.search(l)
					if(match):
						if(c not in res.keys()):
							res[c]={}
						if(o not in res[c].keys()):
							res[c][o]=wd.getFileInfo(f)
							res[c][o]["matches"]=[]
						res[c][o]["matches"].append({"line":l,"lnr":lc,"start":match.start(0),"end":match.end(0)})
				f.close()
			wd.closeCollection(c)
		if(len(res)==0 and collection!=None):
			res[collection]={};
		self.freeWorkdir(wd);
		return res

class SVNWorkdir():
	def __init__(self,workdir,repo):
		self.workdir=os.path.abspath(workdir)
		self.repo="file://"+os.path.abspath(repo)
		self.cache={}
		self.add=[]
		try:
			os.makedirs(self.workdir)
		except FileExistsError:
			pass
		if(os.path.isdir(self.workdir)):
			shutil.rmtree(self.workdir, ignore_errors=True)
		ret=subprocess.run(["svn", "checkout","--depth","empty",self.repo,self.workdir], capture_output=True)
		if(ret.returncode!=0):
			raise Exception("unable to checkout repo:"+ret.stderr.decode("utf8"))
	def cleanup(self):
		for a in self.cache.keys():
			self.closeCollection(a)
		self.cache={}
		self.add=[]
	def getFileInfo(self,fp):
		res={}
		f=fp.name
		ret=subprocess.run(["svn","info","--show-item","last-changed-date",f],cwd=self.workdir,capture_output=True)
		if(ret.returncode!=0):
			raise Exception("Error getting file info:"+ret.stderr.decode("utf8"))
		res["changed"]=ret.stdout.decode("utf8").strip(" \n\r\t")
		return res
	def openFile(self,collection,object_id,mode):
		f=os.path.join(collection,object_id)
		pf=os.path.join(self.workdir,collection,object_id)
		if(collection not in self.cache):
			self.cache[collection]=[]
		if(object_id not in self.cache[collection]):
			ret=subprocess.run(["svn","update","--parents",f],cwd=self.workdir)
			if(not os.path.isfile(pf)):
				if(mode=='w+' or mode=='wb+'):
					ret=subprocess.run(["svn","update","--parents","--depth","empty",collection],cwd=self.workdir)
					if(not os.path.isdir(os.path.join(self.workdir,collection))):
						os.mkdir(os.path.join(self.workdir,collection))
					self.add.append(pf)
				else:
					raise Exception("Unable to load file: %s"%f)
			self.cache[collection].append(object_id)			
		return open(pf,mode)
	def closeAndCommit(self,fp):
		f=fp.name
		fp.close()
		if(f in self.add):
			ret=subprocess.run(["svn","add","--parents",f],cwd=self.workdir)
			if(ret.returncode!=0):
				raise Exception("Error adding file:%s"%f)
		ret=subprocess.run(["svn","commit","--non-interactive" ,"-m","autocommit",os.path.dirname(f)],cwd=self.workdir,capture_output=True)
		if(ret.returncode!=0):
			raise Exception("Error commiting file:"+ret.stderr.decode("utf8"))
	def loadCollections(self):
		res=[]
		ret=subprocess.run(["svn","update","--set-depth","immediates","."],cwd=self.workdir,capture_output=True)
		if(ret.returncode!=0):
			raise Exception("Unable to load collections:"+ret.stderr.decode("utf8"))
		dirs = os.listdir( self.workdir )
		for a in dirs:
			if(os.path.isdir(os.path.join(self.workdir,a))):
				if(a.startswith(".")):
					continue
				if(a not in self.cache):
					self.cache[a]=[]
				res.append(a)
		return res 
	def closeCollection(self,collection):
		shutil.rmtree(os.path.join(self.workdir,collection), ignore_errors=True)
	def loadObjects(self,collection):
		res=[]
		ret=subprocess.run(["svn","update","--parents","--set-depth","files",collection],cwd=self.workdir)
		if(ret.returncode!=0):
			raise Exception("Unable to load objects for collection: %s"%collection)
		if(collection not in self.cache):
			self.cache[collection]=[]
		dirs = os.listdir(os.path.join(self.workdir,collection))
		for a in dirs:
			if(os.path.isfile(os.path.join(self.workdir,collection,a))):
				if(a.startswith(".")):
					continue
				self.cache[collection].append(a)			
				res.append(a)
		return res 
