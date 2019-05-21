import unittest
import sys
import os
sys.path.insert(0,"../src/")
import SVN
import shutil
class TestSVNbackend(unittest.TestCase):

	def setUp(self):
		self.workerc=4
		self.workdir="testdir/workdir"
		self.repodir="testdir/repo"
		self.text="""
Lorem ipsum dolor sit amet, consectetur adipiscing elit. Ut metus massa,
sagittis consequat tincidunt non, sodales at quam. Cras bibendum, mauris eu
placerat condimentum, magna nisi laoreet massa, eget venenatis ligula velit eu
nisi. Aenean nec turpis vel nunc porta ornare. Donec dolor dolor, imperdiet vel
ultricies interdum, eleifend at lorem. Aliquam vitae nunc lacus. Suspendisse
vitae leo sed risus tempor fermentum quis ut odio. Nunc eu faucibus nunc.
Integer accumsan tempus eros, vitae placerat risus pulvinar ut. Quisque eu
congue ipsum. Fusce ultrices sapien erat, sed pulvinar erat faucibus ac. Nullam
sit amet lectus mauris. Donec et tincidunt justo. Fusce porttitor augue et
libero varius pretium. Sed aliquet metus nec quam bibendum commodo. Morbi
venenatis sagittis semper. Integer venenatis accumsan magna vel bibendum. Aenean
elementum lorem lacus, nec imperdiet velit sagittis quis. Praesent lorem metus,
consectetur et consequat sit amet, suscipit in velit. Etiam ornare augue enim.
Phasellus egestas nunc vitae nisi imperdiet, sed lacinia ante sollicitudin.
Lorem ipsum dolor sit amet, consectetur adipiscing elit. Ut ut quam fringilla
est elementum fringilla et ut ligula. Nullam augue ipsum, porta ut turpis id,
facilisis lacinia eros. Nullam euismod fringilla massa, non lobortis tortor
placerat vitae. Cras risus mi, pulvinar quis augue at, convallis dignissim est.
Curabitur malesuada, massa a lacinia fermentum, ligula lorem molestie erat, in
consectetur risus purus ut justo. Aliquam lobortis laoreet enim, condimentum
consectetur felis. Aenean id scelerisque lectus, a placerat ex. Mauris felis
diam, interdum vitae augue sit amet, faucibus euismod velit. Vestibulum
malesuada augue at quam pharetra gravida. Vestibulum ante ipsum primis in
faucibus orci luctus et ultrices posuere cubilia Curae; Etiam tempus faucibus
justo vel vestibulum. Nulla ipsum lorem, blandit nec scelerisque ut, blandit at
"""

	def _prepareRepo(self):
		shutil.rmtree(self.workdir, ignore_errors=True)
		shutil.rmtree(self.repodir, ignore_errors=True)
		self.repo=SVN.SVNBackend(self.workdir,self.repodir,self.workerc)
	def _testCleanUp(self):
		for a in range(self.workerc):
			for f in os.listdir(os.path.join(self.repo.workdir,"wd%d"%a)):
				self.assertTrue(f.startswith('.'))
		self.assertTrue(self.repo.workers.qsize()==self.workerc)
	def test_add_get(self):
		self._prepareRepo()
		self.repo.addFile("test1","file1",self.text)
		res=self.repo.getFile("test1","file1")
		self.assertTrue(self.text==res)
		self._testCleanUp()
	def test_changefile(self):
		self._prepareRepo()
		self.repo.addFile("test1","file1",self.text)
		res=self.repo.getFile("test1","file1")
		self.assertTrue(self.text==res)
		self.repo.addFile("test1","file1",self.text[10:])		
		res=self.repo.getFile("test1","file1")
		self.assertTrue(self.text[10:]==res)
		self._testCleanUp()
	def test_loadCollections(self):
		self._prepareRepo()
		self.repo.addFile("test1","file1",self.text)
		self.repo.addFile("test2","file1",self.text)
		wd=self.repo.getWorkdir()
		res=wd.loadCollections()
		self.assertTrue(len(res)==2)
		self.assertTrue("test1" in res)
		self.assertTrue("test2" in res)
		self.repo.freeWorkdir(wd)
		self._testCleanUp()
	def test_loadObjects(self):
		self._prepareRepo()
		self.repo.addFile("test2","file1",self.text)
		self.repo.addFile("test2","file2",self.text)
		wd=self.repo.getWorkdir()
		res=wd.loadObjects("test2")
		self.assertTrue(len(res)==2)
		self.assertTrue("file2" in res)
		self.assertTrue("file1" in res)
		self.repo.freeWorkdir(wd)
		self._testCleanUp()
	def test_getFileInfo(self):
		self._prepareRepo()
		self.repo.addFile("test2","file1",self.text)
		wd=self.repo.getWorkdir()
		fp=wd.openFile("test2","file1",'r')
		res=wd.getFileInfo(fp)
		fp.close()
		self.assertTrue("changed" in res)
		self.repo.freeWorkdir(wd)
		self._testCleanUp()
	def test_reopen(self):
		self._prepareRepo()
		self.repo.addFile("test3","file1",self.text)
		repo2=SVN.SVNBackend(self.workdir+"2",self.repodir,1)
		res=repo2.getFile("test3","file1")
		self.assertTrue(self.text==res)
		self._testCleanUp()
		
		
		
if __name__ == '__main__':
    unittest.main()
