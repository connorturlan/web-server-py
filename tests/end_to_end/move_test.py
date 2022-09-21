import json
import unittest
import requests
""" from dotenv import dotenv_values
config = dotenv_values("../.env")
print(config) """


def send_patch(url, body=''):
	return requests.patch(url, json.dumps(body))


class FileServerMoveTests(unittest.TestCase):

	@classmethod
	def setUpClass(self):
		requests.post('http://localhost/files/mkdir/.test')
		requests.post('http://localhost/files/mkdir/.test/.subdir')
		requests.post('http://localhost/files/mkdir/.test_dest')
		requests.post('http://localhost/files/upload/.test/.file.txt',
		              'Weeeeeeeeeeeee!')

	@classmethod
	def tearDownClass(self):
		requests.delete('http://localhost/files/delete/.test')
		requests.delete('http://localhost/files/delete/.test_dest')

	# folder move success tests.

	def test_move_file_succeeds(self):
		requests.post('http://localhost/files/upload/.test/.file.txt',
		              'Weeeeeeeeeeeee!')
		response = send_patch('http://localhost/files/move/.test/.file.txt',
		                      {"destination": ".test_dest/.file.txt"})

		self.assertEqual(response.status_code, 202)

	def test_move_file_fails_sameSource(self):
		response = send_patch('http://localhost/files/move/.test/.file.txt',
		                      {"destination": ".test/.file.txt"})

		self.assertEqual(response.status_code, 400)

	def test_move_file_renamingSucceeds(self):
		response = send_patch('http://localhost/files/move/.test/.file.txt',
		                      {"destination": ".test/.same_file.txt"})

		self.assertEqual(response.status_code, 202)

	# folder move success tests.

	def test_move_folder_succeeds(self):
		requests.post('http://localhost/files/mkdir/.test')
		response = send_patch('http://localhost/files/move/.test',
		                      {"destination": '.test_dest/.subdir'})

		self.assertEqual(response.status_code, 202)

	def test_move_folder_fails_sameSource(self):
		response = send_patch('http://localhost/files/move/.test',
		                      {"destination": '.test'})

		self.assertEqual(response.status_code, 400)

	def test_move_folder_renamingSucceeds(self):
		response = send_patch('http://localhost/files/move/.test/.subdir',
		                      {"destination": '.test_dest/.same_subdir'})

		self.assertEqual(response.status_code, 202)

	# file move failing tests.

	def test_delete_file_fails_unspecifiedMethod(self):
		response = send_patch('http://localhost/files')

		self.assertEqual(response.status_code, 400)

	def test_delete_file_fails_incorrectMethod(self):
		response = send_patch('http://localhost/files/get')

		self.assertEqual(response.status_code, 400)

	def test_delete_file_fails_fileNotFound(self):
		response = send_patch('http://localhost/files/move/.test/.ghost.shell',
		                      {"destination": "./test/.ghost.shell"})

		self.assertEqual(response.status_code, 404)

	def test_delete_file_fails_unspecifiedFile(self):
		response = send_patch('http://localhost/files/move')

		self.assertEqual(response.status_code, 400)

	def test_delete_file_fails_missingBody(self):
		response = send_patch('http://localhost/files/move/.test/.file.txt')

		self.assertEqual(response.status_code, 400)

	def test_delete_file_fails_invalidBody(self):
		response = send_patch('http://localhost/files',
		                      {"to": ".test_dest/file.txt"})

		self.assertEqual(response.status_code, 400)

	def test_delete_file_fails_destinationFolderDoesntExist(self):
		response = send_patch('http://localhost/files/move/.test/.file.txt',
		                      {"destination": "./ghost/.file.txt"})

		self.assertEqual(response.status_code, 404)


if __name__ == '__main__':
	unittest.main()