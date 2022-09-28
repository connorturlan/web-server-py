import unittest
import requests


class FileServerPostTests(unittest.TestCase):

	@classmethod
	def setUpClass(self):
		requests.post('http://localhost/files/mkdir/.test')
		requests.post('http://localhost/files/upload/.test/.test_success.txt',
		              'Hello, World!')

	@classmethod
	def tearDownClass(self):
		requests.delete('http://localhost/files/delete/.test')
		requests.delete('http://localhost/files/delete/.upload')

	def test_post_folder_succeeds(self):
		response = requests.post('http://localhost/files/mkdir/.test/.upload')

		self.assertEqual(response.status_code, 201)

	def test_post_file_succeeds(self):
		response = requests.post(
		    'http://localhost/files/upload/.test/upload.txt',
		    'This is the test file for uploading.')

		self.assertEqual(response.status_code, 201)

	def test_post_file_fails_unspecifiedMethod(self):
		response = requests.post('http://localhost/files')

		self.assertEqual(response.status_code, 400)

	def test_post_file_fails_incorrectMethod(self):
		response = requests.post('http://localhost/files/get')

		self.assertEqual(response.status_code, 405)


if __name__ == '__main__':
	unittest.main()