import unittest
from src.file_server import FileServer
import os, shutil


class DummyRouter(object):

	def noop(*args, **kwargs):
		pass

	def __getattr__(self, __name: str):
		return self.noop


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
		shutil.rmtree('./.testing')

	def test_folder_creation_success(self):
		success = self.server.create_folder(self.dummy_router,
		                                    '.testing/create')
		self.assertTrue(success)
		self.assertTrue(os.path.exists('./.testing/create'))

	def test(self):
		self.assertTrue(False)

	# test get file tree
	# test get file branch

	# test is child path true
	# test is child path false
	# test is child path within share directory
	# test is child path outside share directory

	# test folder create succeeds
	# test folder create fails - folder exists
	# test folder create fails - directory doesn't exist
	# test folder create fails - file not in share directory

	# test file creation succeeds
	# test file creation fails - file exists
	# test file creation fails - directory doesn't exist
	# test file create fails - file not in share directory

	# test folder delete succeeds
	# test folder delete fails - folder doesn't exist
	# test folder delete fails - folder not in share directory

	# test file delete succeeds
	# test file delete fails - file doesn't exist
	# test file delete fails - file not in share directory

	# test file copy succeeds
	# test file copy succeeds - rename
	# test file copy succeeds - new directory
	# test file copy succeeds - new directory and rename
	# test file copy fails - same path
	# test file copy fails - file doesn't exist
	# test file copy fails - destination doesn't exist
	# test file copy fails - source not in share directory
	# test file copy fails - destination not in share directory

	# test folder copy succeeds
	# test folder copy succeeds - rename
	# test folder copy succeeds - new directory
	# test folder copy succeeds - new directory and rename
	# test folder copy fails - same path
	# test folder copy fails - folder doesn't exist
	# test folder copy fails - destination doesn't exist
	# test folder copy fails - source not in share directory
	# test folder copy fails - destination not in share directory

	# test file move succeeds
	# test file move succeeds - rename
	# test file move succeeds - new directory
	# test file move succeeds - new directory and rename
	# test file move fails - same path
	# test file move fails - file doesn't exist
	# test file move fails - destination doesn't exist
	# test file move fails - source not in share directory
	# test file move fails - destination not in share directory

	# test folder move succeeds
	# test folder move succeeds - rename
	# test folder move succeeds - new directory
	# test folder move succeeds - new directory and rename
	# test folder move fails - same path
	# test folder move fails - folder doesn't exist
	# test folder move fails - destination doesn't exist
	# test folder move fails - source not in share directory
	# test folder move fails - destination not in share directory


if __name__ == '__main__':
	unittest.main()