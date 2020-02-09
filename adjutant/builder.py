import os
from adjutant.template import compile_template, render_template
from adjutant.utility import ensure_path

class Builder:
	def __init__(self, basepath, config):
		self.config = config
		self.build_path = os.path.join(basepath, config.BUILD_PATH)
		ensure_path(self.build_path)

		self.template_src_path = os.path.join(basepath, config.TEMPLATE_PATH)

		self.template_path = os.path.join(self.build_path, '__template__')

		# build core templates
		self.coretpl_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'template')
		makefile_tpl_filename = os.path.join(self.template_path, '__Makefile.py')
		if True or not os.path.exists(makefile_tpl_filename):
			compile_template(
				os.path.join(self.coretpl_path, 'Makefile.tpl'), makefile_tpl_filename)

		self.create_makefile()
	
	def _get_tpl_py_filename(self, n):
		pass

	def create_makefile(self):
		makefile = os.path.join(self.build_path, "Makefile")
		if False and os.path.exists(makefile):
			return
		makefile_tpl = os.path.join(self.template_path, '__Makefile.py')
		content = render_template(makefile_tpl, {
			"BUILD_PATH": self.build_path,
			"TEMPLATE_PATH": self.template_src_path,
		})
		with open(makefile, "w") as f:
			f.write(content)

	def build(self):
		os.system("make -C {0}".format(self.build_path))
