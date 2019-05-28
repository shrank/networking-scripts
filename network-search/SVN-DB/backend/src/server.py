from starlette.applications import Starlette
from starlette.responses import JSONResponse, PlainTextResponse, RedirectResponse
import SVN
import os
import json
frontend=False
try:
	if(os.environ['SVNDB_FRONTEND'].lower() in ["yes","true"]):
		frontend=True
except:
	frontend=False


svnDB = Starlette(debug=False)

if(frontend):
	from starlette.staticfiles import StaticFiles
	svnDB.mount('/html', StaticFiles(directory="html"))
	@svnDB.route('/')
	async def homepage(request):
		response = RedirectResponse(url='/html/search.html')

@svnDB.route('/api/store/{collection}/{object_id}')
async def getObject(request):
	object_id = request.path_params['object_id']
	collection = request.path_params['collection']
	result=backend.getFile(collection,object_id)
	return PlainTextResponse(result)

@svnDB.route('/api/store/')
async	def getCollections(request):
	a=backend.getCollections()
	return JSONResponse(a)

@svnDB.route('/api/search/')
async def search(request):
	result={}
	args={}
	args['q'] = request.query_params['q']
	try:
		args['c'] = request.query_params['c']
	except:
		args['c']=None
	result=backend.search(args['q'],args["c"])
	return JSONResponse(result)

try:
	repodir=os.environ['SVNREPO']
except:
	print("Unabel to get Reository Path form environment variable %SVNREPO")
	exit(1)

backend=SVN.SVNBackend("/srv/workdir",repodir)


if __name__ == '__main__':
	import uvicorn
	uvicorn.run(svnDB, host='0.0.0.0', port=80)