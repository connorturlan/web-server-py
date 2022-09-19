from http.server import HTTPServer, BaseHTTPRequestHandler
""" 
# example web module for the web server. 
"""


class WebModule:

	def __init__(self, path="/", params=""):
		self.path = path
		self.url_params = (params.lstrip("/")).split("/") if params else []
		self.params = {}

	def get_url_params(self, path):
		# parametrize the url splitting after each `/` and map to the provided url_params for the module.
		params = path.split("/")[len(self.path.split("/")):]
		self.params = {
		    key: params[i]
		    for i, key in enumerate(self.url_params[:len(params)])
		}
		self.params[""] = params[len(self.url_params):]
		return self.params

	def POST(self, router):
		router.send_simple("(POST) Hello, World!", 501)
		return True

	def GET(self, router):
		router.send_simple("(GET) Hello, World!", 501)
		return True

	def PATCH(self, router):
		router.send_simple("(PATCH) Hello, World!", 501)
		return True

	def DELETE(self, router):
		router.send_simple("(DELETE) Hello, World!", 501)
		return True

	def OPTIONS(self, router):
		router.send_simple("(OPTIONS) Hello, World!", 501)
		return True

	def do_METHOD(self, router, method):
		# if there are url params defined for this module, match the start of the path.
		if self.url_params:
			return (method(router) or True
			        if router.path.startswith(self.path) else False)
		# otherwise, match the exact path.
		else:
			return method(router) or True if router.path == self.path else False

	def do_POST(self, router):
		return self.do_METHOD(router, self.POST)

	def do_GET(self, router):
		return self.do_METHOD(router, self.GET)

	def do_PATCH(self, router):
		return self.do_METHOD(router, self.PATCH)

	def do_DELETE(self, router):
		return self.do_METHOD(router, self.DELETE)

	def do_OPTIONS(self, router):
		return self.do_METHOD(router, self.OPTIONS)


""" 
# a controller object for http requests.
"""


class HTTPController(BaseHTTPRequestHandler):

	def init(self):
		self.modules = []
		return self

	def add_module(self, *modules):
		for module in modules:
			self.modules.append(module)

	def send_body(self, b):
		self.wfile.write(b)

	def receive_body(self):
		content_length = int(self.headers.get("content-length", 0))
		return self.rfile.read(content_length)

	def send(self, header, body, code=200):
		self.send_response(code)
		for field in header:
			self.send_header(field, header[field])
		self.send_header("Access-Control-Allow-Origin", "*")
		self.end_headers()
		self.send_body(body)

	def send_simple(self, body, code=200):
		self.send({"Content-Type": "text/html"}, bytes(body, "utf-8"), code)

	def send_json(self, body, code=200):
		self.send({"Content-Type": "application/json"}, bytes(body, "utf-8"),
		          code)

	def do_METHOD(self, method):
		for module in self.modules:
			if method(module, self):
				break
		else:
			self.send_error(404, "File not found")

	def do_POST(self):
		self.do_METHOD(WebModule.do_POST)

	def do_GET(self):
		self.do_METHOD(WebModule.do_GET)

	def do_PATCH(self):
		self.do_METHOD(WebModule.do_PATCH)

	def do_DELETE(self):
		self.do_METHOD(WebModule.do_DELETE)

	def do_OPTIONS(self):
		self.do_METHOD(WebModule.do_OPTIONS)


""" 
# a simple web server.
"""


class WebServer:

	def __init__(self, hostname, port):
		self.hostname = hostname
		self.port = port

		self.http_server = HTTPServer((self.hostname, self.port),
		                              HTTPController)
		self.router = HTTPController.init(self.http_server.RequestHandlerClass)

	def add_module(self, *modules):
		for module in modules:
			HTTPController.add_module(self.router, module)

	def start(self):
		print("Web server running on %s:%d." % (self.hostname, self.port))
		try:
			self.http_server.serve_forever()
		except KeyboardInterrupt:
			print("Web server shutting down.")


if __name__ == "__main__":
	server = WebServer("localhost", 8080)
	server.add_module(WebModule())
	server.start()
