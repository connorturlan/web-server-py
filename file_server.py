from web_server import WebServer, WebModule
from urllib.parse import unquote
from os import listdir, path
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
		content['..'] = [this_dir.lstrip(self.files_path)]
		return content
	
	def get_files_branch(self, this_dir):
		# generate a tree of a single folder in the share folder structure. 
		content = {d: {} for d in listdir(this_dir) if path.isdir(path.join(this_dir, d))}
		content['.'] = [f for f in listdir(this_dir) if path.isfile(path.join(this_dir, f))]
		content['..'] = [this_dir.lstrip(self.files_path)]
		return content

	def send_folders(self, router):
		# check auth
		pass

		# get the file structure
		tree = self.get_files_tree(self.files_path)

		# send the JSON tree
		router.send_json(json.dumps(tree))
		return True

	def send_folder(self, router, path):
		# check auth
		pass

		# get the file structure
		folderpath = self.files_path if not path else self.files_path + '/' + path
		tree = self.get_files_branch(folderpath)

		# send the JSON tree
		router.send_json(json.dumps(tree))
		return True

	def send_file(self, router, path):
		# check auth
		pass

		filepath = self.files_path if not path else self.files_path + '/' + path

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
	
	def receive_files(self, router, filepath):
		# validate that the request has a body.
		req_body = router.receive_body()
		if not req_body: 
			router.send_error(400, "No request body specified")
			return True

		# print("===== START =====")
		# print(req_body)
		# print("=====  END  =====")

		with open(filepath, 'wb') as file:
			file.write(bytearray(req_body))
		print("write finished.")

		router.send_simple("Accepted", 202)
		return True

	def GET(self, router):
		# get the url parameters.
		params = self.get_url_params(router.path)

		# validate that there were params to check, otherwise it's just a simple get-all request.
		if not params or 'method' not in params or not params['method']:
			self.send_folders(router)
			return True
		# return the get-all request.
		elif params['method'] == 'all':
			self.send_folders(router)
			return True
		# return the request for a specific folder tree.
		elif params['method'] == 'folder':
			filepath = unquote('/'.join(params['']))
			self.send_folder(router, filepath)
			return True
		# return the file specified in the request body.
		elif params['method'] == 'get':
			filepath = unquote('/'.join(params['']))

			# send the file, if it exists.
			self.send_file(router, filepath)
			return True
		# the specified method or parameter was invalid.
		else:
			router.send_error(400, "Invalid method")
			return True
	
	def POST(self, router):
		# get the url parameters.
		params = self.get_url_params(router.path)
		
		# validate that there were params to check, otherwise it's just a simple upload request.
		if not params or 'method' not in params or not params['method']:
			filepath = unquote(self.files_path + '/' + '/'.join(params['']))
			self.receive_files(router, filepath)
			return True
		# return the get request for the specified file.
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
		# return the get-all request.
		elif params['method'] == 'upload':
			filepath = unquote(self.files_path + '/' + '/'.join(params['']))
			self.receive_files(router, filepath)
			return False
		# the specified method or parameter was invalid.
		else:
			router.send_error(400, "Invalid method")
			return True

	def OPTIONS(self, router):
		# send a CORS header for preflight requests.
		router.send(
			{
				'Access-Control-Allow-Methods': 'GET, POST, UPDATE, DELETE, OPTIONS', 
				'Access-Control-Allow-Headers': '*'
			}, 
			b''
		)
		return True
		

class WebpageServer(WebModule):
	def __init__(self, path='/', local_dir='./public'):
		super().__init__(path)
		self.local_dir = local_dir

	def GET(self, router):
		# format the request path to begin at the modules local directory.
		path = 'index.html' if router.path.endswith('/') else router.path
		request_page = self.local_dir + '/' + path
		print('requested:', request_page)

		# check that the page is within the domain.
		if Path(self.local_dir) not in Path(request_page).parents:
			print('access beyond bounds.')
			router.send_error(403, "File unavailable")
			return False

		# try and serve the web resource.
		try:
			page = open(request_page, 'rb')
		except IOError:
			router.send_error(404, 'Page not found')
		else:
			mimetype = mimetypes.guess_type(request_page)
			router.send({'Content-Type': ';'.join((str(m) for m in mimetype))}, page.read())

		return True
	
	def do_METHOD(self, router, method):
		# for all get methods, return this get.
		if router.command == 'GET': return self.GET(router)
		return super().do_METHOD(router, method)

if __name__ == "__main__":
	server = WebServer(sys.argv[1], int(sys.argv[2]))
	server.add_module(FileServer("/files", "/method"), WebpageServer('/', '../file-server-vite/dist'))
	server.start()
