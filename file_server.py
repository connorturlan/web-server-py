from web_server import WebServer, WebModule
from pathlib import Path
import mimetypes
import json
import sys

class FileServer(WebModule):
	def __init__(self, path, files_path = './share'):
		super().__init__(path)
		self.files_path = files_path

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

	def GET(self, router):
		print(router.params)
		req_body = str(router.receive_body(), 'utf-8')
		if not req_body: 
			router.send_error(400, "No request body specified")
			return

		filepath = json.loads(req_body)['filepath']
		self.send_file(router, filepath)
		return

class WebpageServer(WebModule):
	def GET(self, router):
		with open('./public/index.html', 'r') as page:
			router.send_simple(page.read())
		return True

if __name__ == "__main__":
	server = WebServer(sys.argv[1], int(sys.argv[2]))
	server.add_module(WebpageServer(), FileServer("/files"))
	server.start()
