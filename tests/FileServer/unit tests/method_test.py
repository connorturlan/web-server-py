import unittest
from src.file_server import FileServer
import os, shutil
from .common import DummyRouter, FileServerCommonTest


class FileServerGeneralUnitTests(FileServerCommonTest):
	# test get file tree
	def test_getFileTree_correct(self):
		test_tree = self.server.get_files_tree('\\')
		valid_tree = {
		    'folder': {
		        '.': ['file.txt'],
		        '..': ['/folder']
		    },
		    '.': ['test.txt'],
		    '..': ['/']
		}

		self.assertIsNotNone(test_tree)
		self.assertDictEqual(valid_tree, test_tree)

	# test get file branch
	def test_getFileBranch_correctRoot(self):
		test_tree = self.server.get_files_branch('\\')
		valid_tree = {'folder': {}, '.': ['test.txt'], '..': ['/']}

		self.assertIsNotNone(test_tree)
		self.assertDictEqual(valid_tree, test_tree)

	# test get file branch
	def test_getFileBranch_correctBranch(self):
		test_tree = self.server.get_files_branch('\\folder')
		valid_tree = {'.': ['file.txt'], '..': ['/folder']}

		self.assertIsNotNone(test_tree)
		self.assertDictEqual(valid_tree, test_tree)

	# test is child path true
	def test_isChildPath_valid(self):
		valid_path = self.server.isChildPath('.\\.safe harbour\\.testing\\')
		self.assertTrue(valid_path)

		valid_path = self.server.isChildPath(
		    '.\\.safe harbour\\.testing\\folder\\')
		self.assertTrue(valid_path)

	# test is child path false
	def test_isChildPath_invalid(self):
		valid_path = self.server.isChildPath('not a folder\\')
		self.assertFalse(valid_path)

	# test is child path within share directory
	def test_isChildPath_withinShare(self):
		valid_path = self.server.isChildPath(
		    '.\\.safe harbour\\.testing\\folder')
		self.assertTrue(valid_path)

	# test is child path outside share directory
	def test_isChildPath_outsideShare(self):
		valid_path = self.server.isChildPath('.\\.safe harbour\\.canary')
		self.assertFalse(valid_path)


if __name__ == '__main__':
	unittest.main()