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

	# test folder delete succeeds
	# test folder delete fails - folder doesn't exist
	# test folder delete fails - folder not in share directory

	# test file delete succeeds
	# test file delete fails - file doesn't exist
	# test file delete fails - file not in share directory


if __name__ == '__main__':
	unittest.main()