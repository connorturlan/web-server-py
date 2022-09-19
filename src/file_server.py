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
		self.local_files_path = files_path

	def get_files_tree(self, this_dir):
		# generate a tree of the share folder structure.
		content = {
			d: self.get_files_tree(path.join(this_dir, d))
			for d in listdir(this_dir)
			if path.isdir(path.join(this_dir, d))
		}
		content["."] = [
			f for f in listdir(this_dir) if path.isfile(path.join(this_dir, f))
		]
		content[".."] = [this_dir.lstrip(self.local_files_path)]
		return content

	def get_files_branch(self, this_dir):
		# generate a tree of a single folder in the share folder structure.
		content = {
			d: {}
			for d in listdir(this_dir)
			if path.isdir(path.join(this_dir, d))
		}
		content["."] = [
			f for f in listdir(this_dir) if path.isfile(path.join(this_dir, f))
		]
		content[".."] = [this_dir.lstrip(self.local_files_path)]
		return content

	def isChildPath(self, child_path):
		parent = path.realpath(self.local_files_path)
		child = path.realpath(child_path)
		return Path(parent) in Path(child).parents

	def send_folders(self, router):
		# check auth
		pass

		# get the file structure
		tree = self.get_files_tree(self.local_files_path)

		# send the JSON tree
		router.send_json(json.dumps(tree))
		return True

	def send_folder(self, router, folder_path):
		# check auth
		pass

		# get the file structure
		local_path = self.local_files_path if not folder_path else self.local_files_path + "/" + folder_path
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

	def create_folder(self, router, folder_path):
		if os.path.exists(folder_path):
			router.send_error(400, "Folder already exists")
			return False

		# create the directory if it doesn't exist.
		os.mkdir(folder_path)

		router.send_simple("Folder created", 201)
		return True

	def receive_files(self, router, file_path):
		# validate that the request has a body.
		req_body = router.receive_body()
		if not req_body:
			router.send_error(400, "No request body specified")

			return True
  
		# check that the parent folder exists.
		folder_path = os.path.dirname(file_path)
		if not os.path.exists(folder_path):
			router.send_error(404, "Folder not found")

		# write the request body to the
		with open(file_path, "wb") as file:
			file.write(bytearray(req_body))

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

		if os.path.exists(local_path):
			print("removing:", local_path)
			if path.isdir(local_path):
				shutil.rmtree(local_path)
			elif path.isfile(local_path):
				os.remove(local_path)
			else:
				router.send_error(
					400, "Filepath refers to object that isn't folder nor file")
			router.send_simple("Deleted", 204)
		else:
			router.send_error(404, "File doesn't exist")

		return True

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
			file_path = unquote(self.local_files_path + "/" +
								"/".join(params[""]))
			self.receive_files(router, file_path)
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
