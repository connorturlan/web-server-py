from web_server import WebServer, WebModule

class FileServer(WebModule):
	def GET(self, router):
		with open('index.html', 'r') as page:
			router.send_simple(page.read())
		return True

if __name__ == "__main__":
	server = WebServer("localhost", 8080)
	server.add_module(FileServer("/files"))
	server.start();
