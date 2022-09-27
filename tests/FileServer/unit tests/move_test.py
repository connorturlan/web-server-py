import unittest
from src.file_server import FileServer
import os, shutil
from .common import mkdir, DummyRouter, FileServerCommonTest


class FileServerMoveUnitTests(FileServerCommonTest):
	# setup the move file test.

	def setUp(self):
		# create the folders.
		mkdir(self.files + 'src\\')
		mkdir(self.files + 'dst\\')
		mkdir(self.files + 'src\\move\\')

		mkdir(self.root + '.canary\\move\\')

		# create the files.
		with open(self.files + 'src\\move.txt', 'w+') as file:
			file.write('hello, world!\n')
		with open(self.root + '.canary\\move.txt', 'w+') as file:
			file.write('hello, world!\n')

	def tearDown(self):
		# remove the files.
		shutil.rmtree(self.files + 'src\\')
		shutil.rmtree(self.files + 'dst\\')

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

	# test file move succeeds
	def test_file_move_succeeds(self):
		success = self.server.move_file(DummyRouter(), 'src/move.txt',
		                                'dst/move.txt')

		self.assertTrue(success)
		self.assertFalse(os.path.exists(self.files + 'src/move.txt'))
		self.assertTrue(os.path.exists(self.files + 'dst/move.txt'))

	# test file move succeeds - rename
	def test_file_move_succeeds_rename(self):
		success = self.server.move_file(DummyRouter(), 'src/move.txt',
		                                'src/renamed.txt')

		self.assertTrue(success)
		self.assertFalse(os.path.exists(self.files + 'src/move.txt'))
		self.assertTrue(os.path.exists(self.files + 'src/renamed.txt'))

	# test file move succeeds - new directory
	def test_file_move_succeeds_newDirectory(self):
		success = self.server.move_file(DummyRouter(), 'src/move.txt',
		                                'dst/move.txt')

		self.assertTrue(success)
		self.assertFalse(os.path.exists(self.files + 'src/move.txt'))
		self.assertTrue(os.path.exists(self.files + 'dst/move.txt'))

	# test file move succeeds - new directory and rename
	def test_file_move_succeeds_newDirectoryAndRename(self):
		success = self.server.move_file(DummyRouter(), 'src/move.txt',
		                                'dst/rename.txt')

		self.assertTrue(success)
		self.assertFalse(os.path.exists(self.files + 'src/move.txt'))
		self.assertTrue(os.path.exists(self.files + 'dst/rename.txt'))

	# test file move fails - same path
	def test_file_move_fails_samePath(self):
		success = self.server.move_file(DummyRouter(), 'src/move.txt',
		                                'src/move.txt')

		self.assertFalse(success)
		self.assertTrue(os.path.exists(self.files + 'src/move.txt'))
		self.assertFalse(os.path.exists(self.files + 'dst/move.txt'))

	# test file move fails - file doesn't exist
	def test_file_move_fails_fileDoesntExist(self):
		success = self.server.move_file(DummyRouter(), 'src/source.txt',
		                                'dst/move.txt')

		self.assertFalse(success)
		self.assertFalse(os.path.exists(self.files + 'src/source.txt'))
		self.assertTrue(os.path.exists(self.files + 'src/move.txt'))
		self.assertFalse(os.path.exists(self.files + 'dst/move.txt'))

	# test file move fails - destination doesn't exist
	def test_file_move_fails_destinationDoesntExist(self):
		success = self.server.move_file(DummyRouter(), 'src/move.txt',
		                                'destination/move.txt')

		self.assertFalse(success)
		self.assertTrue(os.path.exists(self.files + 'src/move.txt'))
		self.assertFalse(os.path.exists(self.files + 'dst/move.txt'))
		self.assertFalse(os.path.exists(self.files + 'destination/move.txt'))

	# test file move fails - source not in share directory
	def test_file_move_fails_sourceNotInShareDirectory(self):
		success = self.server.move_file(DummyRouter(), '../.canary/move.txt',
		                                'dst/move.txt')

		self.assertFalse(success)
		self.assertTrue(os.path.exists(self.files + '../.canary/move.txt'))
		self.assertFalse(os.path.exists(self.files + 'dst/move.txt'))

	# test file move fails - destination not in share directory
	def test_file_move_fails_destinationNotInShareDirectory(self):
		success = self.server.move_file(DummyRouter(), 'src/move.txt',
		                                '../.canary/dest.txt')

		self.assertFalse(success)
		self.assertTrue(os.path.exists(self.files + 'src/move.txt'))
		self.assertFalse(os.path.exists(self.files + '.canary/dest.txt'))

	# test folder move succeeds
	def test_folder_move_succeeds(self):
		success = self.server.move_file(DummyRouter(), 'src/move', 'dst/move')

		self.assertTrue(success)
		self.assertFalse(os.path.exists(self.files + 'src/move'))
		self.assertTrue(os.path.exists(self.files + 'dst/move'))

	# test folder move succeeds - rename
	def test_folder_move_succeeds_rename(self):
		success = self.server.move_file(DummyRouter(), 'src/move',
		                                'src/renamed')

		self.assertTrue(success)
		self.assertFalse(os.path.exists(self.files + 'src/move'))
		self.assertTrue(os.path.exists(self.files + 'src/renamed'))

	# test folder move succeeds - new directory
	def test_folder_move_succeeds_newDirectory(self):
		success = self.server.move_file(DummyRouter(), 'src/move', 'dst/move')

		self.assertTrue(success)
		self.assertFalse(os.path.exists(self.files + 'src/move'))
		self.assertTrue(os.path.exists(self.files + 'dst/move'))

	# test folder move succeeds - new directory and rename
	def test_folder_move_succeeds_newDirectoryAndRename(self):
		success = self.server.move_file(DummyRouter(), 'src/move', 'dst/rename')

		self.assertTrue(success)
		self.assertFalse(os.path.exists(self.files + 'src/move'))
		self.assertTrue(os.path.exists(self.files + 'dst/rename'))

	# test folder move fails - same path
	def test_folder_move_fails_samePath(self):
		success = self.server.move_file(DummyRouter(), 'src/move', 'src/move')

		self.assertFalse(success)
		self.assertTrue(os.path.exists(self.files + 'src/move'))
		self.assertFalse(os.path.exists(self.files + 'dst/move'))

	# test folder move fails - folder doesn't exist
	def test_folder_move_fails_folderDoesntExist(self):
		success = self.server.move_file(DummyRouter(), 'src/source', 'dst/move')

		self.assertFalse(success)
		self.assertFalse(os.path.exists(self.files + 'src/source'))
		self.assertTrue(os.path.exists(self.files + 'src/move'))
		self.assertFalse(os.path.exists(self.files + 'dst/move'))

	# test folder move fails - destination doesn't exist
	def test_folder_move_fails_destinationDoesntExist(self):
		success = self.server.move_file(DummyRouter(), 'src/move',
		                                'destination/move')

		self.assertFalse(success)
		self.assertTrue(os.path.exists(self.files + 'src/move'))
		self.assertFalse(os.path.exists(self.files + 'dst/move'))
		self.assertFalse(os.path.exists(self.files + 'destination/move'))

	# test folder move fails - source not in share directory
	def test_folder_move_fails_sourceNotInShareDirectory(self):
		success = self.server.move_file(DummyRouter(), '../.canary/move',
		                                'dst/move')

		self.assertFalse(success)
		self.assertTrue(os.path.exists(self.root + '.canary/move'))
		self.assertFalse(os.path.exists(self.files + 'dst/move'))

	# test folder move fails - destination not in share directory
	def test_folder_move_fails_destinationNotInShareDirectory(self):
		success = self.server.move_file(DummyRouter(), 'src/move',
		                                '../.canary/dest')

		self.assertFalse(success)
		self.assertTrue(os.path.exists(self.files + 'src/move'))
		self.assertFalse(os.path.exists(self.files + '.canary/dest'))


if __name__ == '__main__':
	unittest.main()