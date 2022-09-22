import unittest, os, shutil
from src.file_server import FileServer


def mkdir(path):
	if not os.path.exists(path):
		os.mkdir(path)


class DummyRouter(object):

	def noop(*args, **kwargs):
		pass

	def __getattr__(self, __name: str):
		return self.noop


class FileServerCommonTest(unittest.TestCase):

	@classmethod
	def setUpClass(self):
		self.root = os.path.join('./', '.safe harbour/')

		# create a testing dir, wrapped in a safe folder so we don't accidentally delete tests.
		mkdir(self.root)
		mkdir(self.root + '.canary')
		mkdir(self.root + '.testing')
		mkdir(self.root + '.testing/folder')

		# create a test file.
		with open(self.root + '.testing/test.txt', 'w') as file:
			file.write('hello, world!\n')
		with open(self.root + '.testing/folder/file.txt', 'w') as file:
			file.write('The quick brown fox jumps over the lazy dog.')

		self.server = FileServer('/files', self.root + '.testing')
		self.dummy_router = DummyRouter()

	@classmethod
	def tearDownClass(self):
		# remove the testing directories.
		""" shutil.rmtree('./.safe harbour')
		shutil.rmtree('./.canary') """


if __name__ == "__main__":
	print("common classes for unit tests must be imported for use.")