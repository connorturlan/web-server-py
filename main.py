from file_server import FileServer, WebpageServer
from web_server import WebServer
import sys

if __name__ == "__main__":
	print("Starting file server.")
	server = WebServer(sys.argv[1], int(sys.argv[2]))
	server.add_module(FileServer("/files"),
	                  WebpageServer('/', '../file-server-react/dist'))
	server.start()