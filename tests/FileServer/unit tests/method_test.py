import unittest
from src.file_server import FileServer
import os, shutil
from .common import DummyRouter, FileServerCommonTest


class FileServerGeneralUnitTests(FileServerCommonTest):
	# test get file tree
	def test_getFileTree_correct(self):
		pass

	# test get file branch
	def test_getFileBranch_correct(self):
		pass

	# test is child path true
	def test_isChildPath_valid(self):
		pass

	# test is child path false
	def test_isChildPath_invalid(self):
		pass

	# test is child path within share directory
	def test_isChildPath_withinShare(self):
		pass

	# test is child path outside share directory
	def test_isChildPath_outsideShare(self):
		pass


if __name__ == '__main__':
	unittest.main()