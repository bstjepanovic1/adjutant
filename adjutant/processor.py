import os
import re
import json
import glob
import hashlib
from fnmatch import fnmatch

from adjutant import config
from adjutant.template import render_template
from adjutant.utility import ensure_path, DotDict, write_file, read_file


class ProcessorContext:
	out_filename = None
	out_part = None

	def output(self, filename):
		self.out_filename = filename
		self.out_part = None
		return ''

	def output_part(self, filename):
		self.out_filename = filename
		self.out_part = True
		return ''

	def reset(self):
		self.out_filename = None
		self.out_part = None

class Processor:

	def __init__(self, source, dependency, output):
		self.context = ProcessorContext()
		self.source = source
		self.source_key = hashlib.md5(source.encode('utf8')).hexdigest()[:14]
		self.dependency = dependency
		self.content = read_file(source)
		self.output = output
		self.output_deps = dict()
		self.output_deps[output] = [self.source]
		self.generated_files = list()

		# same template called multiple times in one file
		self.template_d = dict()

	def _run_pattern(self, re_pattern, callback):
		for match in re_pattern.finditer(self.content):
			callback(self, match)

	def _template_output(self, template, content):
		if self.context.out_filename:
			part = self.context.out_part
			if part != None:
				parts_filename = config.get_build_path(self.context.out_filename + ".part")
				out_filename = os.path.join(parts_filename, self.source_key)
				self.output_deps[config.get_build_path(self.context.out_filename)] = [out_filename]

			else:
				out_filename = config.get_build_path(self.context.out_filename)

			write_file(out_filename, content)
			self.generated_files.append(out_filename)
			self.output_deps[out_filename] = [self.output]

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
			self._template_output(tpl, content)
			all_content += content
			self.output_deps[self.output].append(tpl)

		return all_content

	def build(self):
		# cleanup from previous build
		prev = read_file(self.output)
		if prev:
			prev = json.loads(prev)
			for f in prev.get('out_files'):
				if os.path.exists(f):
					os.remove(f)

		# run all applicable rules
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
		write_file(self.output, json.dumps({
			'source': self.source,
			'out_files': self.generated_files,
		}))
