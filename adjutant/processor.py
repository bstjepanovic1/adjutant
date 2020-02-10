import os
import glob

from adjutant import config
from adjutant.utility import ensure_path, DotDict


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
		with open(source, "r") as f:
			self.content = f.read()

	def build(self):
		print("Building!")
		for rule in config._rules:
			print(rule)
