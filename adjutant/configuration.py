import re
import os

class Config:

	base_path = ''

	template_path = ''
	build_path = ''
	source_path = ''

	def __init__(self):
		self._rules = []

	def add_rule(self, file_patterns, text_pattern=None, callback=None, read_file=False):
		if text_pattern:
			text_pattern = re.compile(text_pattern, re.DOTALL | re.MULTILINE)
		self._rules.append((
			[file_patterns] if isinstance(file_patterns, str) else file_patterns, 
			text_pattern, callback, True if text_pattern else read_file
		))

	def get_path(self, p):
		return os.path.join(self.base_path, p)

	def get_build_path(self, p):
		return os.path.join(self.base_path, self.build_path, p)

	def get_template_script(self, template, exact=False):
		return os.path.join(
			self.base_path, self.build_path, '__tpl__', 
			template if exact else '{0}.tpl.py'.format(template)
		)
