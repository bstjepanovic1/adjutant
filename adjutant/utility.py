import os

def ensure_path(path):
	if not os.path.exists(path):
		os.makedirs(path)

def import_file(filename, name=None):
	import importlib.util
	spec = importlib.util.spec_from_file_location(name or filename, filename)
	mod = importlib.util.module_from_spec(spec)
	spec.loader.exec_module(mod)
	return mod

class DotDict(dict):
	__getattr__ = dict.get
	def __init__(self, iterable, **kwargs):
		for key in iterable:
			p = iterable[key]
			if isinstance(p, dict):
				self[key] = DotDict(p)
			else:
				self[key] = p
		dict.__init__(self)
