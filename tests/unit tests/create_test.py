import unittest
from src.file_server import FileServer
import os, shutil
from .common import DummyRouter


class FileServerCreateUnitTests(unittest.TestCase):

	@classmethod
	def setUpClass(self):
		self.root = './.safe harbour/'

		# create a testing dir, wrapped in a safe folder so we don't accidentally delete tests.
		os.mkdir(self.root)
		os.mkdir(self.root + '.testing')
		os.mkdir(self.root + '.canary')

		self.server = FileServer('/files', self.root + '.testing')
		self.dummy_router = DummyRouter()

	@classmethod
	def tearDownClass(self):
		# remove the testing directories.
		shutil.rmtree('./.safe harbour')
		shutil.rmtree('./.canary')

	def test(self):
		self.assertTrue(False)

	# test folder create succeeds
	# test folder create fails - folder exists
	# test folder create fails - directory doesn't exist
	# test folder create fails - file not in share directory

	# test file creation succeeds
	# test file creation fails - file exists
	# test file creation fails - directory doesn't exist
	# test file create fails - file not in share directory


if __name__ == '__main__':
	unittest.main()