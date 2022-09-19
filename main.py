from src.webpage_server import WebpageServer
from src.file_server import FileServer
from src.web_server import WebServer
import sys

if __name__ == "__main__":
	print("Starting file server.")
	server = WebServer(sys.argv[1], int(sys.argv[2]))
	server.add_module(FileServer("/files"),
	                  WebpageServer('/', '../file-server-react/dist'))
	server.start()