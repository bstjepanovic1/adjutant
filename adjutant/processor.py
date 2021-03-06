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

	def output_part(self, filename, order=None):
		self.out_filename = filename
		self.out_part = { 'order': 'Z' if order == None else order }
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
		self.content = None
		self.output = output
		self.output_deps = dict()
		self.output_deps[output] = [self.source]
		self.generated_files = list()

		self.template_d = dict()

	def _template_output(self, template, content):
		tpl_d = self.template_d.get(template, dict())

		if self.context.out_filename:
			part = self.context.out_part
			if part != None:
				occurence = tpl_d.get('occurence', 0) + 1
				tpl_d['occurence'] = occurence
				order = part.get('order')
				parts_filename = config.get_build_path(self.context.out_filename + ".part")
				out_filename = os.path.join(parts_filename, '{0}_{1}_{2}'.format(order, self.source_key, occurence))
				self.output_deps[config.get_build_path(self.context.out_filename)] = [out_filename]

			else:
				out_filename = config.get_build_path(self.context.out_filename)

			write_file(out_filename, content)
			self.generated_files.append(out_filename)
			self.output_deps[out_filename] = [self.output]
		
		self.template_d[template] = tpl_d

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

	def _run_pattern(self, re_pattern, callback):
		if not re_pattern:
			callback(self)
			return
		for match in re_pattern.finditer(self.content):
			callback(self, match)

	def build(self):
		# cleanup from previous build
		prev = read_file(self.output, empty_content=None)
		if prev:
			prev = json.loads(prev)
			for f in prev.get('out_files'):
				if os.path.exists(f):
					os.remove(f)

		# run all applicable rules
		for rule in config._rules:
			file_patterns, re_pattern, callback, read_content = rule
			for pat in file_patterns:
				full = os.path.join(config.base_path, pat)
				if fnmatch(self.source, full):
					if read_content and not self.content:
						self.content = read_file(self.source)
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
