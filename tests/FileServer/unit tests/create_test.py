import unittest
from src.file_server import FileServer
import os, shutil
from .common import DummyRouter, FileServerCommonTest


class FileServerCreateUnitTests(FileServerCommonTest):

	# test folder create succeeds
	def test_folder_creation_success(self):
		success = self.server.create_folder(DummyRouter(), '.testing/create')
		self.assertTrue(success)
		self.assertTrue(os.path.exists(self.root + '.testing/create'))

	# test folder create fails - folder exists
	def test_folder_creation_fails_folderExists(self):
		success = self.server.create_folder(DummyRouter(), '.testing/folder')
		self.assertFalse(success)
		self.assertTrue(os.path.exists(self.root + '.testing/create'))

	# test folder create fails - directory doesn't exist
	def test_folder_create_fails_parentDirectoryDoesntExist(self):
		success = self.server.create_folder(DummyRouter(), '.failing/create')
		self.assertFalse(success)
		self.assertFalse(os.path.exists(self.root + '.failing/create'))

	# test folder create fails - file not in share directory
	def test_folder_create_fails_fileNotInShareDirectory(self):
		success = self.server.create_folder(DummyRouter(), '../')
		self.assertFalse(success)
		self.assertFalse(os.path.exists(self.root + '.testing/create'))

	# test file creation succeeds
	def test_file_create_succeeds(self):
		pass

	# test file creation fails - file exists
	def test_file_create_fails_fileExists(self):
		pass

	# test file creation fails - directory doesn't exist
	def test_file_create_fails_parentDirectoryDoesntExist(self):
		pass

	# test file create fails - file not in share directory
	def test_file_create_fails_fileNotInShareDirectory(self):
		pass


if __name__ == '__main__':
	unittest.main()