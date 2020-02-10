import os
import argparse

from adjutant import config
from adjutant.processor import Processor
from adjutant.builder import Builder
from adjutant.template import compile_template
from adjutant.utility import import_file

def command_build_file(args):
	proc = Processor(args.source, args.dependency)
	proc.build()

def command_build(args, basepath):
	builder = Builder(basepath)
	builder.build()

def command_compile_template(args):
	compile_template(args.source, args.output)

def adjutant_cli_main():
	# load configuration
	basepath = os.getcwd()
	config.base_path = basepath
	config_filename = os.path.join(basepath, 'adjutant.py')
	if os.path.exists(config_filename):
		import_file(config_filename)

	# parse arguments
	main_parser = argparse.ArgumentParser()
	subparsers = main_parser.add_subparsers(dest='command')

	# build command
	parser = subparsers.add_parser("build", help="""
		Build entire project.
	""")

	# Process command
	parser = subparsers.add_parser('build:file', help="""
		Preprocesses source code file and generates one or more deriveded files.
	""")
	parser.add_argument("source")
	parser.add_argument('--dependency', '-d')

	# Compile template command
	parser = subparsers.add_parser("template:compile", help="""
		Compile template into python file. Note that `adjutant build` will
		manage templates automaticaly.
	""")
	parser.add_argument("source")
	parser.add_argument("--output", "-o")

	# execute
	args = main_parser.parse_args()

	if args.command == 'build:file':
		command_build_file(args)
	elif args.command == 'build':
		command_build(args, basepath)
	elif args.command == 'template:compile':
		command_compile_template(args)
