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
		self.root = '.\\.safe harbour\\'
		self.files = self.root + '.testing\\'

		# create a testing dir, wrapped in a safe folder so we don't accidentally delete tests.
		mkdir('.\\.canary\\')
		mkdir(self.root)
		mkdir(self.root + '.not in testing\\')
		mkdir(self.files)
		mkdir(self.files + 'folder\\')
		# mkdir(os.path.join(self.root, '.testing', 'folder2'))

		# create a test file.
		with open(self.files + 'test.txt', 'w+') as file:
			file.write('hello, world!\n')
		with open(self.files + 'folder\\file.txt', 'w+') as file:
			file.write('The quick brown fox jumps over the lazy dog.')

		self.server = FileServer('/files', self.files)
		self.dummy_router = DummyRouter()

	@classmethod
	def tearDownClass(self):
		# remove the testing directories.
		shutil.rmtree(self.root)
		shutil.rmtree('.\\.canary')


if __name__ == "__main__":
	print("common classes for unit tests must be imported for use.")