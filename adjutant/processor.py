import os
import re
import glob
from fnmatch import fnmatch

from adjutant import config
from adjutant.template import render_template
from adjutant.utility import ensure_path, DotDict, write_file, read_file


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
		self.content = read_file(source)

	def _run_pattern(self, re_pattern, callback):
		for match in re_pattern.finditer(self.content):
			callback(self, match)

	def template(self, template_name, data):
		self.context.reset()
		content = render_template(config.get_template_script(template_name), data, self.context)
		if self.context.out_filename:
			write_file(config.get_build_path(self.context.out_filename), content)
		return content

	def build(self):
		for rule in config._rules:
			file_patterns, re_pattern, callback = rule
			for pat in file_patterns:
				full = os.path.join(config.base_path, pat)
				if fnmatch(self.source, full):
					self._run_pattern(re_pattern, callback)
		ensure_path(os.path.dirname(self.dependency))
		#with open(self.dependency, "w") as f:
		#	f.write("Test")
