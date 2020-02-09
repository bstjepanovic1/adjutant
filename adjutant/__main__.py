import re
import os
import sys
import json
import glob
import base64

from utemplate import Compiler

current_dir = os.getcwd()
sys.path.append(current_dir)

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

class Template:
	def __init__(self, name, src, compiled, force=False):
		if True or not os.path.exists(compiled) or force:
			if not os.path.exists(src):
				raise ValueError("Missing template source `{0}`!".format(src))
			src_f = open(src, "r")
			ensure_path(os.path.dirname(compiled))
			dest_f = open(compiled, "w")
			compiler = Compiler(src_f, dest_f, loader=self)
			compiler.args = 'PP, data, **kwargs'
			compiler.compile()
			src_f.close()
			dest_f.close()
		self.tpl = import_file(compiled, name)
		self.invalid = False

	def render(self, context, data):
		data = DotDict(data)
		content = ""
		for line in self.tpl.render(context, data):
			content += line
		return content

class PreprocessorContext:
	out_filename = None
	out_combine = False

	def output(self, filename, combine=False):
		self.out_filename = filename
		self.out_combine = combine
		return ''

	def reset(self):
		self.out_filename = None
		self.out_combine = False

class Preprocessor:
	loaded_templates = dict()

	def __init__(self, source_filename, out_path, tpl_path):
		self.source_filename = source_filename
		self.out_path = out_path
		self.tpl_path = tpl_path
		self.context = PreprocessorContext()

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


def pp_error(text):
	print("Error:")
	print(text)

def main():
	args = pp_cli()

	preprocessor = Preprocessor(
		source_filename=args.source,
		out_path=args.output,
		tpl_path=args.template_dir
	)

	loaded_tpls = dict()

	# process source, match all potential comments
	matches = re.findall(r'\/\*\*\s+(.*?)\{(.*)\}\s+\*\/', content, re.MULTILINE | re.DOTALL)
	for m in matches:
		key, content = m
		try:
			data = json.loads("{" + content + "}")
		except:
			raise

		# match all functions
		for tpl in re.findall(r'\@(.*?)\s', key):
			preprocessor.execute(tpl, data)
	
	# merge parts, cleanup

main()
