from threading import local
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

	def get_files_tree(self, this_dir='\\'):
		# get the specific path
		dir_path = self.local_files_path + this_dir
		# generate a tree of the share folder structure.
		content = {
		    d: self.get_files_tree(path.join(this_dir, d))
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

	def get_files_branch(self, this_dir='\\'):
		# get the specific path
		dir_path = self.local_files_path + this_dir
		# generate a tree of the share folder structure.
		content = {
		    d: {}
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
		local_path = folder_path
		tree = self.get_files_branch(local_path)

		# send the JSON tree
		router.send_json(json.dumps(tree))
		return True

	def send_file(self, router, file_path):
		# check auth
		pass

		local_path = self.local_files_path if not file_path else self.local_files_path + "/" + file_path

		# check is subdir of files, i.e. not outside the safe share folder.
		if not self.isChildPath(local_path):
			print("access beyond bounds.")
			router.send_error(403, "File unavailable")

			return False

		# try and safely open the file, give feedback if not.
		try:
			file = open(local_path, "rb")
		except IOError:
			print("error retrieving file.")
			router.send_error(404, "File not found")

			return False
		else:
			# get the filetype and send to the user.
			mimetype = mimetypes.guess_type(local_path)
			router.send({"Content-Type": mimetype}, file.read())
			return True

	def create_unit(self, item_path, isDir=True, item_data=''):
		# create the full item path.
		local_path = self.local_files_path + item_path

		# check that the path exists in the share directory.
		if not self.isChildPath(local_path):
			return False, 403

		# check that the item doesn't already exist.
		if os.path.exists(local_path):
			return False, 400

		# check that the parent folder does exist.
		if not os.path.exists(os.path.dirname(local_path)):
			return False, 404

		# create the directory if it doesn't exist.
		if isDir:
			os.mkdir(local_path)
		# write the request body to the file
		else:
			with open(local_path, "wb") as file:
				file.write(bytearray(item_data))

		# send a successful status code.
		return True, 201

	def create_folder(self, router, folder_path):
		# create the file.
		success, status = self.create_unit(folder_path)
		# respond to the request.
		if success:
			# send a successful status code.
			router.send_simple("Folder created", 201)
			return True
		else:
			if status == 400:
				router.send_error(404, "Parent folder not found")
			elif status == 403:
				router.send_error(403, "Folder unavailable")
			elif status == 404:
				router.send_error(400, "Folder already exists")
			return False

		local_path = self.local_files_path + folder_path
		if os.path.exists(local_path):
			router.send_error(400, "Folder already exists")
			return False

		if not os.path.exists(os.path.dirname(local_path)):
			router.send_error(404, "Folder not found")
			return False

		# create the directory if it doesn't exist.
		os.mkdir(local_path)

		# send a successful status code.
		router.send_simple("Folder created", 201)
		return True

	def create_file(self, router, file_path, file_body):
		# create the file.
		success, status = self.create_unit(file_path, False, file_body)
		# respond to the request.
		if success:
			# send a successful status code.
			router.send_simple("File created", 201)
			return True
		else:
			if status == 400:
				router.send_error(404, "Parent folder not found")
			elif status == 403:
				router.send_error(403, "Folder unavailable")
			elif status == 404:
				router.send_error(400, "File already exists")
			return False

		# check that the parent folder exists.
		folder_path = os.path.dirname(file_path)
		if not os.path.exists(folder_path):
			router.send_error(404, "Folder not found")
			return False

		# write the request body to the
		with open(file_path, "wb") as file:
			file.write(bytearray(file_body))

		# send a successful status code.
		router.send_simple("File created", 201)
		return True

	def delete_file(self, router, file_path):
		# check auth
		pass

		local_path = self.local_files_path if not file_path else self.local_files_path + "/" + file_path

		# check is subdir of files, i.e. not outside the safe share folder.
		if not self.isChildPath(local_path):
			print("access beyond bounds.")
			router.send_error(403, "File unavailable")

			return False

		# check that the file exists.
		if not os.path.exists(local_path):
			router.send_error(404, "File doesn't exist")

		# remove the directory.
		if path.isdir(local_path):
			shutil.rmtree(local_path)
		# remote the file.
		elif path.isfile(local_path):
			os.remove(local_path)
		# the file is neither a file or folder send an error.
		else:
			router.send_error(
			    400, "Filepath refers to object that isn't folder nor file")
			return False

		# send a successful status code.
		router.send_simple("Deleted", 204)
		return True

	def shuttle_file(self, router, origin, destination, doCopy=True):
		# check auth
		pass

		local_origin = self.local_files_path if not origin else self.local_files_path + "/" + origin
		local_destination = self.local_files_path if not destination else self.local_files_path + "/" + destination

		# check is subdir of files, i.e. not outside the safe share folder.
		if not self.isChildPath(local_origin) or not self.isChildPath(
		    local_destination):
			print("access beyond bounds.")
			router.send_error(403, "File unavailable")
			return False

		# check that the destination parent folder exists.
		if not os.path.exists(os.path.dirname(local_destination)):
			router.send_error(404, "Source not found")
			return False

		# check that the origin and destination are different.
		if local_origin == local_destination:
			router.send_error(400, "Source and destination must be different")
			return False

		# ensure the origin exists.
		if os.path.exists(local_origin):
			if doCopy:
				if path.isdir(local_origin):
					shutil.copytree(local_origin, local_destination)
				elif path.isfile(local_origin):
					shutil.copyfile(local_origin, local_destination)
				else:
					router.send_error(
					    400,
					    "Filepath refers to object that isn't folder nor file")

				router.send_simple("Copied", 201)
			else:
				shutil.move(local_origin, local_destination)
				router.send_simple("Moved", 202)
		else:
			router.send_error(404, "File doesn't exist")

		return True

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
			return True
		# return the get-all request.
		elif params["method"] == "all":
			self.send_folders(router)
			return True
		# return the request for a specific folder tree.
		elif params["method"] == "folder":
			file_path = unquote("/".join(params[""]))
			self.send_folder(router, file_path)
			return True
		# return the file specified in the request body.
		elif params["method"] == "get":
			file_path = unquote("/".join(params[""]))

			# send the file, if it exists.
			self.send_file(router, file_path)
			return True
		# the specified method or parameter was invalid.
		else:
			router.send_error(400, "Incorrect method")

			return True

	def POST(self, router):
		# get the url parameters.
		params = self.get_url_params(router.path)

		# validate that there were params to check, otherwise it's just a simple upload request.
		if not params or "method" not in params or not params["method"]:
			router.send_error(400, "Unspecified method")

			return True
		#
		elif params["method"] == "mkdir":
			folder_path = unquote(self.local_files_path + "/" +
			                      "/".join(params[""]))
			self.create_folder(router, folder_path)
			return True
		#
		elif params["method"] == "upload":
			# validate that the request has a body.
			file_body = router.receive_body()
			if not file_body:
				router.send_error(400, "No request body specified")
				return True

			# get the file_path.
			file_path = unquote(self.local_files_path + "/" +
			                    "/".join(params[""]))
			self.create_file(router, file_path, file_body)
			return True
		# the specified method or parameter was invalid.
		else:
			router.send_error(400, "Incorrect method")
			return True

	def DELETE(self, router):
		# get the url parameters.
		params = self.get_url_params(router.path)

		# validate that there was a method specified.
		if not params or "method" not in params or not params["method"]:
			router.send_error(400, "Unspecified method")

			return True
		# return the get-all request.
		elif params["method"] == "delete":
			file_path = unquote("/".join(params[""]))
			self.delete_file(router, file_path)
			return True
		# the specified method or parameter was invalid.
		else:
			router.send_error(400, "Incorrect method")

			return True

	def PATCH(self, router):
		# get the url parameters.
		params = self.get_url_params(router.path)

		# get the requested file source.
		# validate that there was a method specified.
		if not params or "method" not in params or not params["method"]:
			router.send_error(400, "Unspecified method")
			return True

		file_origin = unquote("/".join(params[""]))

		# get the requested file destination.
		# validate that the request has a body.
		req_body = router.receive_body()
		if not req_body:
			router.send_error(400, "No request body specified")
			return True

		# validate that the req_body is json.
		req_json = json.loads(req_body)
		if not req_json:
			router.send_error(400, "No request body specified (json)")
			return True
		# validate that the req_json contains the file destination.
		elif 'destination' not in req_json:
			router.send_error(400, "Invalid request body")
			return True

		file_destination = req_json['destination']

		# determine the patch method the user would like.
		# perform the copy method.
		if params["method"] == "copy":
			self.copy_file(router, file_origin, file_destination)
			return True
		# perform the move method.
		elif params["method"] == "move":
			self.move_file(router, file_origin, file_destination)
			return True
		# the specified method or parameter was invalid.
		else:
			router.send_error(400, "Incorrect method")
			return True

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
