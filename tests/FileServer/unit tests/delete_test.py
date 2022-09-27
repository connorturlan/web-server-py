import unittest
from src.file_server import FileServer
import os, shutil
from .common import DummyRouter, FileServerCommonTest, mkdir


class FileServerDeleteUnitTests(FileServerCommonTest):

	def setUp(self):
		# create folders to delete.
		mkdir(self.files + 'delete\\')
		mkdir(self.files + 'delete\\folder')
		mkdir(self.root + '.canary\\delete')

		# create files to delete.
		with open(self.files + 'delete\\delete_file.txt', 'w+') as file:
			file.write('Goodbye cruel world!')
		with open(self.root + '.canary\\delete\\delete_file.txt', 'w+') as file:
			file.write('Goodbye cruel world!')

	def tearDown(self):
		# delete the temp file.
		shutil.rmtree(self.files + 'delete\\')
		shutil.rmtree(self.root + '.canary\\delete')

	# test folder delete succeeds
	def test_folder_delete_succeeds(self):
		success = self.server.delete_file(DummyRouter(), 'delete/folder')

		self.assertTrue(success)
		self.assertFalse(os.path.exists(self.files + 'delete/folder'))

	# test folder delete fails - folder doesn't exist
	def test_folder_delete_fails_folderDoesntExist(self):
		success = self.server.delete_file(DummyRouter(),
		                                  'delete/folder_to_delete')

		self.assertFalse(success)
		self.assertTrue(os.path.exists(self.files + 'delete/folder'))
		self.assertFalse(os.path.exists(self.files + 'delete/folder_to_delete'))

	# test folder delete fails - folder not in share directory
	def test_folder_delete_fails_folderNotInShareDirectory(self):
		success = self.server.delete_file(DummyRouter(), '../.canary/delete')

		self.assertFalse(success)
		self.assertTrue(os.path.exists(self.files + 'delete/folder'))
		self.assertTrue(os.path.exists(self.root + '.canary/delete'))

	# test file delete succeeds
	def test_file_delete_succeeds(self):
		success = self.server.delete_file(DummyRouter(),
		                                  'delete/delete_file.txt')

		self.assertTrue(success)
		self.assertFalse(os.path.exists(self.files + 'delete/delete_file.txt'))

	# test file delete fails - file doesn't exist
	def test_file_delete_fails_fileDoesntExist(self):
		success = self.server.delete_file(DummyRouter(),
		                                  'delete/to_delete_file.txt')

		self.assertFalse(success)
		self.assertTrue(os.path.exists(self.files + 'delete/delete_file.txt'))
		self.assertFalse(
		    os.path.exists(self.files + 'delete/to_delete_file.txt'))

	# test file delete fails - file not in share directory

	def test_file_delete_fails_fileNotInShareDirectory(self):
		success = self.server.delete_file(DummyRouter(),
		                                  '../.canary/delete/delete_file.txt')

		self.assertFalse(success)
		self.assertTrue(os.path.exists(self.files + 'delete/delete_file.txt'))
		self.assertTrue(
		    os.path.exists(self.root + '.canary/delete/delete_file.txt'))


if __name__ == '__main__':
	unittest.main()