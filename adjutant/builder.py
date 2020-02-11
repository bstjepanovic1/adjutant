import os

from adjutant import config
from adjutant.template import compile_template, render_template, get_system_template
from adjutant.utility import ensure_path


class Builder:

	def __init__(self):
		self.build_path = os.path.join(config.base_path, config.build_path)
		ensure_path(self.build_path)

		self.template_src_path = os.path.join(config.base_path, config.template_path)
		self.template_path = os.path.join(self.build_path, '__tpl__')

		# build core coretpl
		makefile_tpl_filename = os.path.join(self.template_path, '__Makefile.py')
		if True or not os.path.exists(makefile_tpl_filename):
			compile_template(
				get_system_template('Makefile.tpl'), makefile_tpl_filename)

		self.create_makefile()
	
	def _get_tpl_py_filename(self, n):
		pass

	def create_makefile(self):
		makefile = os.path.join(self.build_path, "Makefile")
		if False and os.path.exists(makefile):
			return
		
		makefile_tpl = os.path.join(self.template_path, '__Makefile.py')
		content = render_template(makefile_tpl, {})

		with open(makefile, "w") as f:
			f.write(content)

	def build(self):
		os.system("make -C {0}".format(self.build_path))
