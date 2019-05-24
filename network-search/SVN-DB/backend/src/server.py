from starlette.applications import Starlette
from starlette.responses import JSONResponse, PlainTextResponse
import SVN
import os
import json


svnDB = Starlette(debug=False)

@svnDB.route('/')
async def homepage(request):
    return JSONResponse({'hello': 'world'})


@svnDB.route('/store/{collection}/{object_id}')
async def getObject(request):
	object_id = request.path_params['object_id']
	collection = request.path_params['collection']
	result=backend.getFile(collection,object_id)
	return PlainTextResponse(result)

@svnDB.route('/store/')
async	def getCollections(request):
	a=backend.getCollections()
	return JSONResponse(a)

@svnDB.route('/search/')
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

backend=SVN.SVNBackend("/srv/workdir",os.environ['SVNREPO'])


if __name__ == '__main__':
	import uvicorn
	uvicorn.run(svnDB, host='0.0.0.0', port=8000)