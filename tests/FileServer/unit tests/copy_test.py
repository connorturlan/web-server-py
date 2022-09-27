import unittest
from src.file_server import FileServer
import os, shutil
from .common import DummyRouter, FileServerCommonTest, mkdir


class FileServerCopyUnitTests(FileServerCommonTest):
	# setup the copy file test.
	def setUp(self):
		# create the folders.
		mkdir(self.files + 'src\\')
		mkdir(self.files + 'dst\\')
		mkdir(self.files + 'src\\copy\\')

		mkdir(self.root + '.canary\\copy\\')

		# create the files.
		with open(self.files + 'src\\copy.txt', 'w+') as file:
			file.write('hello, world!\n')
		with open(self.root + '.canary\\copy.txt', 'w+') as file:
			file.write('hello, world!\n')

	def tearDown(self):
		# remove the files.
		shutil.rmtree(self.files + 'src\\')
		shutil.rmtree(self.files + 'dst\\')

	# test file copy succeeds
	def test_file_copy_succeeds(self):
		success = self.server.copy_file(DummyRouter(), 'src/copy.txt',
		                                'dst/copy.txt')

		self.assertTrue(success)
		self.assertTrue(os.path.exists(self.files + 'src/copy.txt'))
		self.assertTrue(os.path.exists(self.files + 'dst/copy.txt'))

	# test file copy succeeds - rename
	def test_file_copy_succeeds_rename(self):
		success = self.server.copy_file(DummyRouter(), 'src/copy.txt',
		                                'src/renamed.txt')

		self.assertTrue(success)
		self.assertTrue(os.path.exists(self.files + 'src/copy.txt'))
		self.assertTrue(os.path.exists(self.files + 'src/renamed.txt'))

	# test file copy succeeds - new directory
	def test_file_copy_succeeds_newDirectory(self):
		success = self.server.copy_file(DummyRouter(), 'src/copy.txt',
		                                'dst/copy.txt')

		self.assertTrue(success)
		self.assertTrue(os.path.exists(self.files + 'src/copy.txt'))
		self.assertTrue(os.path.exists(self.files + 'dst/copy.txt'))

	# test file copy succeeds - new directory and rename
	def test_file_copy_succeeds_newDirectoryAndRename(self):
		success = self.server.copy_file(DummyRouter(), 'src/copy.txt',
		                                'dst/rename.txt')

		self.assertTrue(success)
		self.assertTrue(os.path.exists(self.files + 'src/copy.txt'))
		self.assertTrue(os.path.exists(self.files + 'dst/rename.txt'))

	# test file copy fails - same path
	def test_file_copy_fails_samePath(self):
		success = self.server.copy_file(DummyRouter(), 'src/copy.txt',
		                                'src/copy.txt')

		self.assertFalse(success)
		self.assertTrue(os.path.exists(self.files + 'src/copy.txt'))
		self.assertFalse(os.path.exists(self.files + 'dst/copy.txt'))

	# test file copy fails - file doesn't exist
	def test_file_copy_fails_fileDoesntExist(self):
		success = self.server.copy_file(DummyRouter(), 'src/source.txt',
		                                'dst/copy.txt')

		self.assertFalse(success)
		self.assertFalse(os.path.exists(self.files + 'src/source.txt'))
		self.assertTrue(os.path.exists(self.files + 'src/copy.txt'))
		self.assertFalse(os.path.exists(self.files + 'dst/copy.txt'))

	# test file copy fails - destination doesn't exist
	def test_file_copy_fails_destinationDoesntExist(self):
		success = self.server.copy_file(DummyRouter(), 'src/copy.txt',
		                                'destination/copy.txt')

		self.assertFalse(success)
		self.assertTrue(os.path.exists(self.files + 'src/copy.txt'))
		self.assertFalse(os.path.exists(self.files + 'dst/copy.txt'))
		self.assertFalse(os.path.exists(self.files + 'destination/copy.txt'))

	# test file copy fails - source not in share directory
	def test_file_copy_fails_sourceNotInShareDirectory(self):
		success = self.server.copy_file(DummyRouter(), '../.canary/copy.txt',
		                                'dst/copy.txt')

		self.assertFalse(success)
		self.assertTrue(os.path.exists(self.files + '../.canary/copy.txt'))
		self.assertFalse(os.path.exists(self.files + 'dst/copy.txt'))

	# test file copy fails - destination not in share directory
	def test_file_copy_fails_destinationNotInShareDirectory(self):
		success = self.server.copy_file(DummyRouter(), 'src/copy.txt',
		                                '../.canary/dest.txt')

		self.assertFalse(success)
		self.assertTrue(os.path.exists(self.files + 'src/copy.txt'))
		self.assertFalse(os.path.exists(self.files + '.canary/dest.txt'))

	# test folder copy succeeds
	def test_folder_copy_succeeds(self):
		success = self.server.copy_file(DummyRouter(), 'src/copy', 'dst/copy')

		self.assertTrue(success)
		self.assertTrue(os.path.exists(self.files + 'src/copy'))
		self.assertTrue(os.path.exists(self.files + 'dst/copy'))

	# test folder copy succeeds - rename
	def test_folder_copy_succeeds_rename(self):
		success = self.server.copy_file(DummyRouter(), 'src/copy',
		                                'src/renamed')

		self.assertTrue(success)
		self.assertTrue(os.path.exists(self.files + 'src/copy'))
		self.assertTrue(os.path.exists(self.files + 'src/renamed'))

	# test folder copy succeeds - new directory
	def test_folder_copy_succeeds_newDirectory(self):
		success = self.server.copy_file(DummyRouter(), 'src/copy', 'dst/copy')

		self.assertTrue(success)
		self.assertTrue(os.path.exists(self.files + 'src/copy'))
		self.assertTrue(os.path.exists(self.files + 'dst/copy'))

	# test folder copy succeeds - new directory and rename
	def test_folder_copy_succeeds_newDirectoryAndRename(self):
		success = self.server.copy_file(DummyRouter(), 'src/copy', 'dst/rename')

		self.assertTrue(success)
		self.assertTrue(os.path.exists(self.files + 'src/copy'))
		self.assertTrue(os.path.exists(self.files + 'dst/rename'))

	# test folder copy fails - same path
	def test_folder_copy_fails_samePath(self):
		success = self.server.copy_file(DummyRouter(), 'src/copy', 'src/copy')

		self.assertFalse(success)
		self.assertTrue(os.path.exists(self.files + 'src/copy'))
		self.assertFalse(os.path.exists(self.files + 'dst/copy'))

	# test folder copy fails - folder doesn't exist
	def test_folder_copy_fails_folderDoesntExist(self):
		success = self.server.copy_file(DummyRouter(), 'src/source', 'dst/copy')

		self.assertFalse(success)
		self.assertFalse(os.path.exists(self.files + 'src/source'))
		self.assertTrue(os.path.exists(self.files + 'src/copy'))
		self.assertFalse(os.path.exists(self.files + 'dst/copy'))

	# test folder copy fails - destination doesn't exist
	def test_folder_copy_fails_destinationDoesntExist(self):
		success = self.server.copy_file(DummyRouter(), 'src/copy',
		                                'destination/copy')

		self.assertFalse(success)
		self.assertTrue(os.path.exists(self.files + 'src/copy'))
		self.assertFalse(os.path.exists(self.files + 'dst/copy'))
		self.assertFalse(os.path.exists(self.files + 'destination/copy'))

	# test folder copy fails - source not in share directory
	def test_folder_copy_fails_sourceNotInShareDirectory(self):
		success = self.server.copy_file(DummyRouter(), '../.canary/copy',
		                                'dst/copy')

		self.assertFalse(success)
		self.assertTrue(os.path.exists(self.root + '.canary/copy'))
		self.assertFalse(os.path.exists(self.files + 'dst/copy'))

	# test folder copy fails - destination not in share directory
	def test_folder_copy_fails_destinationNotInShareDirectory(self):
		success = self.server.copy_file(DummyRouter(), 'src/copy',
		                                '../.canary/dest')

		self.assertFalse(success)
		self.assertTrue(os.path.exists(self.files + 'src/copy'))
		self.assertFalse(os.path.exists(self.files + '.canary/dest'))


if __name__ == '__main__':
	unittest.main()