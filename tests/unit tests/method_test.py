import unittest
from src.file_server import FileServer
import os, shutil
from .common import DummyRouter


class FileServerServerSideTests(unittest.TestCase):

	@classmethod
	def setUpClass(self):
		# create a testing dir, wrapped in a safe folder so we don't accidentally delete tests.
		os.mkdir('./.safe harbour/.testing')
		os.mkdir('./.canary')

		self.server = FileServer('/files', './.safe harbour/.testing')
		self.dummy_router = DummyRouter()

	@classmethod
	def tearDownClass(self):
		# remove the testing directories.
		shutil.rmtree('./.safe harbour')
		shutil.rmtree('./.canary')

	def test_folder_creation_success(self):
		success = self.server.create_folder(self.dummy_router,
		                                    '.testing/create')
		self.assertTrue(success)
		self.assertTrue(os.path.exists('./.testing/create'))

	# test get file tree
	# test get file branch

	# test is child path true
	# test is child path false
	# test is child path within share directory
	# test is child path outside share directory


if __name__ == '__main__':
	unittest.main()