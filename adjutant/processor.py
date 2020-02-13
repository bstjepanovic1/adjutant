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

	def __init__(self, source, dependency, output):
		self.context = ProcessorContext()
		self.source = source
		self.dependency = dependency
		self.content = read_file(source)
		self.output = output
		self.output_deps = dict()
		self.output_deps[output] = [self.source]

	def _run_pattern(self, re_pattern, callback):
		for match in re_pattern.finditer(self.content):
			callback(self, match)

	def template(self, template_name, data):
		self.context.reset()

		# find all sub-templates
		templates = [config.get_template_script(template_name)]
		tpl_filename = config.get_template_script('{0}.*'.format(template_name))
		for tpl in glob.glob(tpl_filename):
			templates.append(tpl)

		all_content = ""
		for tpl in templates:
			content = render_template(tpl, data, self.context)
			if self.context.out_filename:
				out_filename = config.get_build_path(self.context.out_filename)
				write_file(out_filename, content)
				self.output_deps[out_filename] = [self.output]
				self.output_deps[self.output].append(tpl)
			all_content += content

		return all_content

	def build(self):
		for rule in config._rules:
			file_patterns, re_pattern, callback = rule
			for pat in file_patterns:
				full = os.path.join(config.base_path, pat)
				if fnmatch(self.source, full):
					self._run_pattern(re_pattern, callback)
	
		# write dependency file
		ensure_path(os.path.dirname(self.dependency))
		depcontent = render_template(
			config.get_template_script('__dep.py', exact=True), self.output_deps)
		write_file(self.dependency, depcontent)

		# write output file
		write_file(self.output, "")
