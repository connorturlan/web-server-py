import unittest
from src.file_server import FileServer
import os, shutil
from .common import DummyRouter, FileServerCommonTest


class FileServerMoveUnitTests(FileServerCommonTest):

	def test(self):
		self.assertTrue(False)

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


if __name__ == '__main__':
	unittest.main()