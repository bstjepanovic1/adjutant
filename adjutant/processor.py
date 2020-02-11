import os
import re
import glob
from fnmatch import fnmatch

from adjutant import config
from adjutant.utility import ensure_path, DotDict


class ProcessorContext:
	out_filename = None
	out_combine = False

	def output(self, filename, combine=False):
		self.out_filename = filename
		self.out_combine = combine
		return ''

	def reset(self):
		self.out_filename = None
		self.out_combine = False

class Processor:

	def __init__(self, source, dependency):
		self.context = ProcessorContext()
		self.source = source
		self.dependency = dependency
		with open(source, "r") as f:
			self.content = f.read()

	def run_pattern(self, re_pattern, callback):
		for match in re_pattern.finditer(self.content):
			print(match.group('template'))

	def build(self):
		for rule in config._rules:
			file_patterns, re_pattern, callback = rule
			for pat in file_patterns:
				full = os.path.join(config.base_path, pat)
				if fnmatch(self.source, full):
					self.run_pattern(re_pattern, callback)
		ensure_path(os.path.dirname(self.dependency))
		with open(self.dependency, "w") as f:
			f.write("Test")
