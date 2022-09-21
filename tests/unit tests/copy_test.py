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

	def test(self):
		self.assertTrue(False)

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


if __name__ == '__main__':
	unittest.main()