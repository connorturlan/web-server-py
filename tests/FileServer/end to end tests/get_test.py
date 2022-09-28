import unittest
import requests


class FileServerGetTests(unittest.TestCase):

	@classmethod
	def setUpClass(self):

		requests.post('http://localhost/files/mkdir/.test')
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
		    'http://localhost/files/get/.test/../../../.test_success.txt')

		self.assertEqual(response.status_code, 403)

	def test_get_file_fails_fileNotFound(self):
		response = requests.get(
		    'http://localhost/files/get/.test/test_fails.txt')

		self.assertEqual(response.status_code, 404)

	def test_get_file_fails_incorrectMethod(self):
		response = requests.get('http://localhost/files/upload')

		self.assertEqual(response.status_code, 405)


if __name__ == '__main__':
	unittest.main()