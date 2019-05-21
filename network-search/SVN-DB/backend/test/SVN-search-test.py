import unittest
import sys
import os
import shutil
sys.path.insert(0,"../src/")
import SVN

class TestSVNsearch(unittest.TestCase):

	def setUp(self):
		self.workerc=4
		self.workdir="testdir/workdir"
		self.repodir="testdir/repo"
		self._prepareRepo()
		self.repo.addFile("test2","file1","""
		aaaaaaaaaaaaaaaaaaaaaaaaaaaa
		bbbbbbbbbbbbbbbbbbbbbbbbbbbb
		cccccccccccccccccccccccccccc
		dddddddddddddddddddddddddddd
		eeeeeeeeeeeeeeeeeeeeeeeeeeee
		ffffffffffffzzffffffffffffff
		gggggggggggggggggggggggggggg
""")
		self.repo.addFile("test2","file2","""
		gggggggggggggggggggggggggggg
		hhhhhhhhhhhhhhhhhhhhhhhhhhhh
		iiiiiiiiiiiiiiiiiiiiiiiiiiii
		kkkkkkkkkkkkkkkkkkkkkkkkkkkk
		jjjjjjjjjjjjjjjjjjjjjjjjjjjj
		kkkkkkkkkkkkkkkkkkkkkkkkkkkk
		kkkkkkkkkkkkkkkkkkkkkkkkkkkk
""")
	def _prepareRepo(self):
		shutil.rmtree(self.workdir, ignore_errors=True)
		shutil.rmtree(self.repodir, ignore_errors=True)
		self.repo=SVN.SVNBackend(self.workdir,self.repodir,self.workerc)
	def _testCleanUp(self):
		for a in range(self.workerc):
			for f in os.listdir(os.path.join(self.repo.workdir,"wd%d"%a)):
				self.assertTrue(f.startswith('.'))
		self.assertTrue(self.repo.workers.qsize()==self.workerc)

	def test_simple(self):
		res=self.repo.search('ccccccc')
		self.assertTrue(len(res)==1)
		self.assertTrue("test2" in res.keys())
		self.assertTrue(len(res["test2"])==1)
		self.assertTrue("file1" in res["test2"].keys())
		self.assertTrue(len(res["test2"]["file1"]["matches"])==1)
		self.assertTrue(4==res["test2"]["file1"]["matches"][0]["lnr"])
		self._testCleanUp()
	def test_simple2(self):
		res=self.repo.search('ggggggggggg')
		self.assertTrue(len(res)==1)
		self.assertTrue("test2" in res.keys())
		self.assertTrue(len(res["test2"])==2)
		for a in ["file1","file2"]:
			self.assertTrue(a in res["test2"].keys())
			self.assertTrue(len(res["test2"][a]["matches"])==1)
		self._testCleanUp()
	def test_simple3(self):
		res=self.repo.search('kkkkkk')
		self.assertTrue(len(res)==1)
		self.assertTrue("test2" in res.keys())
		self.assertTrue(len(res["test2"])==1)
		self.assertTrue("file2" in res["test2"].keys())
		self.assertTrue(len(res["test2"]["file2"]["matches"])==3)
		self.assertTrue(5==res["test2"]["file2"]["matches"][0]["lnr"])
		self.assertTrue(7==res["test2"]["file2"]["matches"][1]["lnr"])
		self.assertTrue(8==res["test2"]["file2"]["matches"][2]["lnr"])
		self._testCleanUp()
		
		
if __name__ == '__main__':
    unittest.main()
