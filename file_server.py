from genericpath import isdir
from web_server import WebServer, WebModule
from os import listdir, path, walk
import os
from pathlib import Path
import mimetypes
import json
import sys

class FileServer(WebModule):
	def __init__(self, path, params, files_path = './share'):
		super().__init__(path, params)
		self.files_path = files_path
	
	def get_files_tree(self, this_dir):
		# generate a tree of the share folder structure. 
		content = {d: self.get_files_tree(path.join(this_dir, d)) for d in listdir(this_dir) if path.isdir(path.join(this_dir, d))}
		content['.'] = [f for f in listdir(this_dir) if path.isfile(path.join(this_dir, f))]
		return content

	def send_files(self, router):
		# check auth
		pass

		# get the file structure
		tree = self.get_files_tree(self.files_path)

		# send the JSON tree
		router.send_json(json.dumps(tree))
		return True

	def send_file(self, router, filepath):
		# check auth
		pass

		# check is subdir of files, i.e. not outside the safe share folder.
		if Path(self.files_path) not in Path(filepath).parents:
			print('access beyond bounds.')
			router.send_error(403, "File unavailable")
			return False

		# try and safely open the file, give feedback if not.
		try:
			file = open(filepath, 'rb')
		except IOError:
			print('error retrieving file.')
			router.send_error(404, "File not found")
			return False
		else:
			# get the filetype and send to the user.
			print('file found.')
			mimetype = mimetypes.guess_type(filepath)
			router.send({'Content-Type': mimetype}, file.read())
			return True

	def GET(self, router):
		# get the url parameters.
		params = self.get_url_params(router.path)
		print(params)
		
		# validate that there were params to check, otherwise it's just a simple get-all request.
		if not params or 'method' not in params or not params['method']:
			self.send_files(router)
			return True
		# return the get-all request.
		elif params['method'] == 'all':
			self.send_files(router)
			return True
		# return the file specified in the request body.
		elif params['method'] == 'get':
			# validate that the request has a body.
			req_body = str(router.receive_body(), 'utf-8')
			if not req_body: 
				router.send_error(400, "No request body specified")
				return True

			# validate that the request json has the filepath attribute.
			req_json = json.loads(req_body)
			if 'filepath' not in req_json: 
				router.send_error(400, "No `filepath` specified")
				return True

			# send the file, if it exists.
			filepath = req_json['filepath']
			self.send_file(router, filepath)
			return True
		# the specified method or parameter was invalid.
		else:
			router.send_error(400, "Invalid method")
			return True
		

class WebpageServer(WebModule):
	def GET(self, router):
		with open('./public/index.html', 'r') as page:
			router.send_simple(page.read())
		return True

if __name__ == "__main__":
	server = WebServer(sys.argv[1], int(sys.argv[2]))
	server.add_module(WebpageServer(), FileServer("/files", "/method/id"))
	server.start()
