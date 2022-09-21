import unittest
from src.file_server import FileServer
import os, shutil
from .common import DummyRouter, FileServerCommonTest


class FileServerCreateUnitTests(FileServerCommonTest):

	# test folder create succeeds
	def test_folder_creation_success(self):
		success = self.server.create_folder(self.dummy_router,
		                                    self.root + '.testing/create')
		self.assertTrue(success)
		self.assertTrue(os.path.exists(self.root + '.testing/create'))

	# test folder create fails - folder exists
	# test folder create fails - directory doesn't exist
	# test folder create fails - file not in share directory

	# test file creation succeeds
	# test file creation fails - file exists
	# test file creation fails - directory doesn't exist
	# test file create fails - file not in share directory


if __name__ == '__main__':
	unittest.main()