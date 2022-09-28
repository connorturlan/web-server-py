import unittest
import requests


class FileServerDeleteTests(unittest.TestCase):

	@classmethod
	def setUpClass(self):
		requests.post('http://localhost/files/mkdir/.test')
		requests.post('http://localhost/files/upload/.test/.test_success.txt',
		              'Hello, World!')

	@classmethod
	def tearDownClass(self):
		requests.delete('http://localhost/files/delete/.test')

	def test_delete_folder_succeeds(self):
		requests.post('http://localhost/files/mkdir/.test')
		response = requests.delete('http://localhost/files/delete/.test')

		self.assertEqual(response.status_code, 204)

	def test_delete_file_succeeds(self):
		requests.post('http://localhost/files/mkdir/.test')
		requests.post('http://localhost/files/upload/.test/.test_success.txt',
		              'Hello, World!')
		response = requests.delete(
		    'http://localhost/files/delete/.test/.test_success.txt')

		self.assertEqual(response.status_code, 204)

	def test_delete_file_fails_unspecifiedMethod(self):
		response = requests.delete('http://localhost/files')

		self.assertEqual(response.status_code, 400)

	def test_delete_file_fails_incorrectMethod(self):
		response = requests.delete('http://localhost/files/get')

		self.assertEqual(response.status_code, 405)

	def test_delete_file_fails_fileNotFound(self):
		response = requests.delete(
		    'http://localhost/files/delete/.test/.ghost.shell')

		self.assertEqual(response.status_code, 404)

	def test_delete_file_fails_unspecifiedFile(self):
		response = requests.delete('http://localhost/files')

		self.assertEqual(response.status_code, 400)


if __name__ == '__main__':
	unittest.main()