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
	# test is child path false
	# test is child path within share directory
	# test is child path outside share directory


if __name__ == '__main__':
	unittest.main()