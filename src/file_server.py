from src.web_server import WebServer, WebModule
from urllib.parse import unquote
from os import listdir, path
from pathlib import Path
import mimetypes
import shutil
import json
import sys
import os


class FileServer(WebModule):

	def __init__(self, path, files_path="./share"):
		super().__init__(path, "/method")
		self.local_files_path = files_path.replace('\\', '/')

		# define all error messages for the file server. as specified in the internal error documentation.
		self.error_messages = {
		    0: (200, "Success"),
		    1: (500, "Failed"),
		    10: (400, "Unspecified method"),
		    11: (405, "Invalid method"),
		    12: (400, "Request body missing"),
		    13: (400, "Request body empty"),
		    14: (400, "Request body must be JSON"),
		    15: (400, "Request body incorrect"),
		    20: (401, "User unauthenticated"),
		    21: (403, "User unauthorized"),
		    22: (403, "Path unavailable"),
		    30: (409, "Source and destination path must be different"),
		    40: (404, "File not found"),
		    41: (409, "File already exists"),
		    42: (404, "Destination file doesn't exist"),
		    43: (409, "Destination file already exists"),
		    50: (404, "Folder doesn't exist"),
		    51: (409, "Folder already exists"),
		    52: (404, "Destination folder doesn't exist"),
		    53: (409, "Destination folder already exists"),
		    54: (404, "Parent folder doesn't exist")
		}

	def get_local_path(self, rel_path):
		return self.local_files_path if not rel_path else self.local_files_path + "/" + rel_path

	def send_error(self, router, error_code):
		# check that the error code does exist, then send.
		if error_code in self.error_messages:
			code, message = self.error_messages[error_code]
			router.send_error(code, message)
		# otherwise send an generic server-side error.
		else:
			router.send_error(500)

	def generate_files_branch(self, this_dir, isTree):
		# get the specific path
		dir_path = self.local_files_path + this_dir
		# generate a tree of the share folder structure.
		content = {
		    d: self.get_files_tree(path.join(this_dir, d)) if isTree else {}
		    for d in listdir(dir_path)
		    if path.isdir(path.join(dir_path, d))
		}
		content["."] = [
		    f for f in listdir(dir_path) if path.isfile(path.join(dir_path, f))
		]
		content[".."] = [
		    dir_path.lstrip(self.local_files_path).replace('\\', '/')
		]
		return content

	def get_files_tree(self, this_dir='\\'):
		return self.generate_files_branch(this_dir, True)

	def get_files_branch(self, this_dir='\\'):
		return self.generate_files_branch(this_dir, False)

	def isChildPath(self, child_path):
		parent = path.realpath(self.local_files_path)
		child = path.realpath(child_path)
		return parent == child or Path(parent) in Path(child).parents

	def send_folders(self, router):
		# check auth
		pass

		# get the file structure
		tree = self.get_files_tree()

		# send the JSON tree
		router.send_json(json.dumps(tree))
		return True

	def send_folder(self, router, folder_path):
		# check auth
		pass

		# get the file structure
		tree = self.get_files_branch(folder_path)

		# send the JSON tree
		router.send_json(json.dumps(tree))
		return True

	def send_file(self, router, file_path):
		# check auth
		pass

		# convert the relative file path to the local path.
		local_path = self.get_local_path(file_path)

		# check is subdir of files, i.e. not outside the safe share folder.
		if not self.isChildPath(local_path):
			self.send_error(router, 22)    # not in share dir
			return False

		# try and safely open the file, give feedback if not.
		if not os.path.exists(local_path):
			self.send_error(router, 40)    # file doesn't exist.
			return False

		# get the filetype and send to the user.
		file = open(local_path, "rb")
		mimetype = mimetypes.guess_type(local_path)
		router.send({"Content-Type": mimetype}, file.read())
		return True

	def server_create_unit(self, item_path, isFile, item_data):
		# create the full item path.
		local_path = self.get_local_path(item_path)

		# check that the path exists in the share directory.
		if not self.isChildPath(local_path):
			return False, 22

		# check that the item doesn't already exist.
		if os.path.exists(local_path):
			return False, (41 if isFile else 51)

		# check that the parent folder does exist.
		if not os.path.exists(os.path.dirname(local_path)):
			return False, 54

		# create the directory if it doesn't exist.
		if isFile:
			with open(local_path, "wb") as file:
				file.write(bytearray(item_data))
		# write the request body to the file
		else:
			os.mkdir(local_path)

		# send a successful status code.
		return True, 201

	def create_unit(self, router, item_path, isFile=False, item_data=''):
		# check auth
		pass

		# create the unit.
		success, status = self.server_create_unit(item_path, isFile, item_data)

		# respond to the request.
		if success:
			# send a successful status code.
			if isFile:
				router.send_simple("File created", 201)
			else:
				router.send_simple("Folder created", 201)
		# respond with error when unsuccessful.
		else:
			self.send_error(router, status)
		return success

	def create_folder(self, router, folder_path):
		# create the folder.
		return self.create_unit(router, folder_path)

	def create_file(self, router, file_path, file_body):
		# create the file.
		return self.create_unit(router, file_path, True, file_body)

	def server_delete_file(self, file_path):
		local_path = self.get_local_path(file_path)

		# check is subdir of files, i.e. not outside the safe share folder.
		if not self.isChildPath(local_path):
			return False, 22

		# check that the file exists.
		if not os.path.exists(local_path):
			return False, 40

		# remove the directory.
		if path.isdir(local_path):
			shutil.rmtree(local_path)
		# remote the file.
		else:
			os.remove(local_path)

		# send a successful status code.
		return True, 0

	def delete_file(self, router, file_path):
		# check auth
		pass

		# perform the delete.
		success, status = self.server_delete_file(file_path)

		# send a successful status code.
		if success:
			router.send_simple("Deleted", 204)
		# otherwise, send the error.
		else:
			self.send_error(router, status)
		return success

	def server_shuttle_file(self, origin, destination, doCopy=True):
		# get the local paths of the src and dst.
		local_origin = self.get_local_path(origin)
		local_destination = self.get_local_path(destination)

		# check is subdir of files, i.e. not outside the safe share folder.
		if not self.isChildPath(local_origin) or not self.isChildPath(
		    local_destination):
			return False, 22

		# check that the source file exists.
		if not os.path.exists(local_origin):
			return False, 40

		# check that the destination parent folder exists.
		if not os.path.exists(os.path.dirname(local_destination)):
			return False, 54

		# check that the origin and destination are different.
		if local_origin == local_destination:
			return False, 30

		# perform the copy/move.
		if doCopy:
			if path.isdir(local_origin):
				shutil.copytree(local_origin, local_destination)
			else:
				shutil.copyfile(local_origin, local_destination)
		else:
			shutil.move(local_origin, local_destination)
		return True, 0

	def shuttle_file(self, router, origin, destination, doCopy):
		# check auth
		pass

		# perform the shuttle.
		success, status = self.server_shuttle_file(origin, destination, doCopy)

		# if successful send the correct response.
		if success:
			if doCopy:
				router.send_simple("Copied", 201)
			else:
				router.send_simple("Moved", 202)
		# if unsuccessful send the correct error.
		else:
			self.send_error(router, status)
		return success

	def copy_file(self, router, origin, destination):
		return self.shuttle_file(router, origin, destination, True)

	def move_file(self, router, origin, destination):
		return self.shuttle_file(router, origin, destination, False)

	def GET(self, router):
		# get the url parameters.
		params = self.get_url_params(router.path)

		# validate that there were params to check, otherwise it's just a simple get-all request.
		if not params or "method" not in params or not params["method"]:
			self.send_folders(router)

		# return the get-all request.
		elif params["method"] == "all":
			self.send_folders(router)

		# return the request for a specific folder tree.
		elif params["method"] == "folder":
			file_path = unquote("/" + "/".join(params[""]))

			# send the folder branch, if it exists.
			self.send_folder(router, file_path)

		# return the file specified in the request body.
		elif params["method"] == "get":
			file_path = unquote("/" + "/".join(params[""]))

			# send the file, if it exists.
			self.send_file(router, file_path)

		# the specified method or parameter was invalid.
		else:
			self.send_error(router, 11)    # incorrect method.

	def POST(self, router):
		# get the url parameters.
		params = self.get_url_params(router.path)

		# validate that there were params to check, otherwise it's just a simple upload request.
		if not params or "method" not in params or not params["method"]:
			router.send_error(400, "Unspecified method")
		#
		elif params["method"] == "mkdir":
			folder_path = unquote("/" + "/".join(params[""]))
			self.create_folder(router, folder_path)
		#
		elif params["method"] == "upload":
			# validate that the request has a body.
			file_body = router.receive_body()
			if not file_body:
				self.send_error(router, 12)    # no request body
				return True

			# get the file_path.
			file_path = unquote("/" + "/".join(params[""]))
			self.create_file(router, file_path, file_body)
			return True
		# the specified method or parameter was invalid.
		else:
			self.send_error(router, 11)    # incorrect method.
			return True

	def DELETE(self, router):
		# get the url parameters.
		params = self.get_url_params(router.path)

		# validate that there was a method specified.
		if not params or "method" not in params or not params["method"]:
			self.send_error(router, 10)    # missing method.
		# return the get-all request.
		elif params["method"] == "delete":
			file_path = unquote("/" + "/".join(params[""]))
			self.delete_file(router, file_path)
		# the specified method or parameter was invalid.
		else:
			self.send_error(router, 11)    # incorrect method.

	def PATCH(self, router):
		# get the url parameters.
		params = self.get_url_params(router.path)

		# get the requested file source.
		# validate that there was a method specified.
		if not params or "method" not in params or not params["method"]:
			self.send_error(router, 10)
			return

		file_origin = unquote("/" + "/".join(params[""]))

		# get the requested file destination.
		# validate that the request has a body.
		req_body = router.receive_body()
		if not req_body:
			self.send_error(router, 12)
			return

		# validate that the req_body is json.
		try:
			req_json = json.loads(req_body)
		except:
			self.send_error(router, 14)
			return

		if not req_json:
			self.send_error(router, 13)
			return
		# validate that the req_json contains the file destination.
		elif 'destination' not in req_json:
			self.send_error(router, 15)
			return

		file_destination = "/" + req_json['destination']

		# determine the patch method the user would like.
		# perform the copy method.
		if params["method"] == "copy":
			self.copy_file(router, file_origin, file_destination)
		# perform the move method.
		elif params["method"] == "move":
			self.move_file(router, file_origin, file_destination)
		# the specified method or parameter was invalid.
		else:
			self.send_error(router, 11)

	def OPTIONS(self, router):
		# send a CORS header for preflight requests.
		router.send(
		    {
		        "Access-Control-Allow-Methods":
		            "GET, POST, UPDATE, DELETE, OPTIONS",
		        "Access-Control-Allow-Headers":
		            "*",
		    },
		    b"",
		)
		return True


if __name__ == "__main__":
	server = WebServer(sys.argv[1], int(sys.argv[2]))
	server.add_module(FileServer("/files", '../share'))
	server.start()
