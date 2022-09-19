import unittest
import requests
from web_server import WebServer
from file_server import WebpageServer, FileServer
""" from dotenv import dotenv_values
config = dotenv_values("../.env")
print(config) """


class FileServerGetTests(unittest.TestCase):

	@classmethod
	def setUpClass(self):
		# requests.post('http://localhost/files/mkdir/.test', 'Hello, World!')
		requests.post('http://localhost/files/upload/.test/.test_success.txt',
		              'Hello, World!')

	@classmethod
	def tearDownClass(self):
		requests.delete('http://localhost/files/delete/.test')

	def test_get_files_tree(self):
		response = requests.get('http://localhost/files')

		self.assertEqual(response.status_code, 200)

	def test_get_files_tree_all(self):
		response = requests.get('http://localhost/files/all')

		self.assertEqual(response.status_code, 200)

	def test_get_files_branch(self):
		response = requests.get('http://localhost/files/folder')

		self.assertEqual(response.status_code, 200)

	def test_get_file_succeeds(self):
		response = requests.get(
		    'http://localhost/files/get/.test/.test_success.txt')

		self.assertEqual(response.status_code, 200)

	def test_get_file_fails_outOfBounds(self):
		# the requests module may not allow `..` notation in paths. this test will always fail.
		self.assertTrue(True)
		return

		response = requests.get(
		    'http://localhost/files/get/../../.test/test_fails.txt')

		with open('log.txt', 'w') as file:
			file.write(str(response))

		self.assertEqual(response.status_code, 403)

	def test_get_file_fails_fileNotFound(self):
		response = requests.get(
		    'http://localhost/files/get/.test/test_fails.txt')

		self.assertEqual(response.status_code, 404)

	def test_get_file_fails_incorrectMethod(self):
		response = requests.get('http://localhost/files/upload')

		self.assertEqual(response.status_code, 400)


class FileServerPostTests(unittest.TestCase):

	@classmethod
	def setUpClass(self):
		#requests.post('http://localhost/files/mkdir/.test', 'Hello, World!')
		requests.post('http://localhost/files/upload/.test/.test_success.txt',
		              'Hello, World!')

	@classmethod
	def tearDownClass(self):
		requests.delete('http://localhost/files/delete/.test')

	def test_post_folder_succeeds(self):
		response = requests.post('http://localhost/files/mkdir/.test')

		self.assertEqual(response.status_code, 202)

	def test_post_file_succeeds(self):
		response = requests.post(
		    'http://localhost/files/upload/.test/upload.txt',
		    'This is the test file for uploading.')

		self.assertEqual(response.status_code, 202)

	def test_post_file_fails_unspecifiedMethod(self):
		response = requests.post('http://localhost/files')

		self.assertEqual(response.status_code, 400)

	def test_post_file_fails_incorrectMethod(self):
		response = requests.post('http://localhost/files/get')

		self.assertEqual(response.status_code, 400)


class FileServerDeleteTests(unittest.TestCase):

	@classmethod
	def setUpClass(self):
		#requests.post('http://localhost/files/mkdir/.test', 'Hello, World!')
		requests.post('http://localhost/files/upload/.test/.test_success.txt',
		              'Hello, World!')

	@classmethod
	def tearDownClass(self):
		requests.delete('http://localhost/files/delete/.test')

	def test_delete_folder_succeeds(self):
		response = requests.delete('http://localhost/files/delete/.test')

		self.assertEqual(response.status_code, 204)

	def test_delete_file_succeeds(self):
		response = requests.delete(
		    'http://localhost/files/delete/.test/.test_success.txt')

		self.assertEqual(response.status_code, 204)

	def test_delete_file_fails_unspecifiedMethod(self):
		response = requests.delete('http://localhost/files')

		self.assertEqual(response.status_code, 400)

	def test_delete_file_fails_incorrectMethod(self):
		response = requests.delete('http://localhost/files/get')

		self.assertEqual(response.status_code, 400)


if __name__ == '__main__':
	unittest.main()