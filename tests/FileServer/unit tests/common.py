import unittest, os, shutil
from src.file_server import FileServer


class DummyRouter(object):

	def noop(*args, **kwargs):
		pass

	def __getattr__(self, __name: str):
		return self.noop


class FileServerCommonTest(unittest.TestCase):

	@classmethod
	def setUpClass(self):
		self.root = './.safe harbour/'

		# create a testing dir, wrapped in a safe folder so we don't accidentally delete tests.
		os.mkdir(self.root)
		os.mkdir(self.root + '.testing')
		os.mkdir(self.root + '.canary')

		# create a test file.
		os.write(self.root + '.testing/test.txt',
		         bytes('hello, world!\n', 'utf-8'))

		self.server = FileServer('/files', self.root + '.testing')
		self.dummy_router = DummyRouter()

	@classmethod
	def tearDownClass(self):
		# remove the testing directories.
		shutil.rmtree('./.safe harbour')
		shutil.rmtree('./.canary')


if __name__ == "__main__":
	print("common classes for unit tests must be imported for use.")