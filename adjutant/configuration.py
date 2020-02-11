import re
import os

class Config:

	base_path = ''

	template_path = ''
	build_path = ''
	source_path = ''

	def __init__(self):
		self._rules = []

	def add_rule(self, file_patterns, re_pattern, callback=None):
		if re_pattern:
			re_pattern = re.compile(re_pattern, re.DOTALL | re.MULTILINE)
		self._rules.append((file_patterns, re_pattern, callback))

	def get_path(self, p):
		return os.path.join(self.base_path, p)
