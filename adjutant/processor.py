import os
import glob

from adjutant.utility import ensure_path, DotDict
from adjutant.template import Template


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
	loaded_templates = dict()

	def __init__(self, source_filename, out_path, tpl_path):
		self.source_filename = source_filename
		self.out_path = out_path
		self.tpl_path = tpl_path
		self.context = ProcessorContext()

	def load_template(self, name):
		loaded = self.loaded_templates.get(name)
		if loaded:
			return loaded
		tpl = Template(
			name, 
			os.path.join(self.tpl_path, '{0}.tpl'.format(name)),
			os.path.join(self.out_path, '__template__', '{0}.tpl.py'.format(name))
		)
		self.loaded_templates[name] = tpl
		return tpl

	def execute(self, action, data):
		actions = [action]
		for fn in glob.glob(os.path.join(self.tpl_path, "{0}.*.tpl".format(action))):
			actions.append(os.path.splitext(os.path.basename(fn))[0])
		for action in actions:
			self.execute_tpl(action, data)
	
	def execute_tpl(self, tpl_name, data):
		template = self.load_template(tpl_name)
		self.context.reset()
		content = template.render(self.context, data)
		if self.context.out_filename:
			if self.context.out_combine:
				out_filename = os.path.join(
					self.out_path, 
					"{0}.parts".format(self.context.out_filename), 
					self.source_filename.replace('/', '__')
				)
			else:
				out_filename = os.path.join(self.out_path, self.context.out_filename)
			ensure_path(os.path.dirname(out_filename))
			with open(out_filename, "w") as f:
				f.write(content)
