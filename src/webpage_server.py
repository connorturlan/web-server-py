from modules.web_server import WebServer, WebModule
from pathlib import Path
from os import path
import mimetypes
import sys

class WebpageServer(WebModule):

	def __init__(self, path="/", local_dir="./public"):
		super().__init__(path, "")
		self.local_dir = local_dir

	def isChildPath(self, child_path):
		parent = path.realpath(self.local_dir)
		child = path.realpath(child_path)
		return Path(parent) in Path(child).parents

	def GET(self, router):
		# format the request path to begin at the modules local directory.
		path = "index.html" if router.path.endswith("/") else router.path
		request_page = self.local_dir + "/" + path

		# check that the page is within the domain.
		if not self.isChildPath(request_page):
			print("access beyond bounds.")
			router.send_error(403, "File unavailable")
			return False

		# try and serve the web resource.
		try:
			page = open(request_page, "rb")
		except IOError:
			router.send_error(404, "Page not found")
		else:
			mimetype = mimetypes.guess_type(request_page)
			router.send({"Content-Type": ";".join((str(m) for m in mimetype))},
						page.read())

		return True

	def do_METHOD(self, router, method):
		# for all get methods, return this get.
		if router.command == "GET":
			return self.GET(router)
		return super().do_METHOD(router, method)

if __name__ == "__main__":
	server = WebServer(sys.argv[1], int(sys.argv[2]))
	server.add_module(WebpageServer('/', '../public'))
	server.start()