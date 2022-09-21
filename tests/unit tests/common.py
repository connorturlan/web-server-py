class DummyRouter(object):

	def noop(*args, **kwargs):
		pass

	def __getattr__(self, __name: str):
		return self.noop


if __name__ == "__main__":
	print("common classes for unit tests must be imported for use.")