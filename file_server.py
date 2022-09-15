from web_server import WebServer, WebModule

class FileServer(WebModule):
	def GET(self, router):
		print(str(router.receive_body(), 'utf-8'))
		router.send_simple('')
		return True

class WebpageServer(WebModule):
	def GET(self, router):
		with open('index.html', 'r') as page:
			router.send_simple(page.read())
		return True

if __name__ == "__main__":
	server = WebServer("localhost", 80)
	server.add_module(WebpageServer(), FileServer("/files"))
	server.start()
