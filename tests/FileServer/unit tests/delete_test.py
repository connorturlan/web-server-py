import unittest
from src.file_server import FileServer
import os, shutil
from .common import DummyRouter, FileServerCommonTest


class FileServerDeleteUnitTests(FileServerCommonTest):

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