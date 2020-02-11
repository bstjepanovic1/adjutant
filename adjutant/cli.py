import os
import argparse

from adjutant import config
from adjutant.processor import Processor
from adjutant.builder import Builder
from adjutant.template import compile_template, render_system_template
from adjutant.utility import import_file

def command_init(args):
	print("INIT")
	render_system_template('adjutant.tpl', os.path.join(args.path, 'adjutant.py'), {})

def command_build_file(args):
	proc = Processor(args.source, args.dependency)
	proc.build()

def command_build(args):
	builder = Builder()
	builder.build()

def command_compile_template(args):
	compile_template(args.source, args.output)

def adjutant_cli_main():
	# parse arguments
	main_parser = argparse.ArgumentParser()
	main_parser.add_argument('--path', '-p', default=os.getcwd())
	subparsers = main_parser.add_subparsers(dest='command')

	# init command
	parser = subparsers.add_parser("init", help="""
		Start new project.
	""")

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

	# load configuration
	config.base_path = args.path
	config_filename = os.path.join(config.base_path, 'adjutant.py')
	if os.path.exists(config_filename):
		import_file(config_filename)

	if args.command == 'init':
		command_init(args)
	elif args.command == 'build:file':
		command_build_file(args)
	elif args.command == 'build':
		command_build(args)
	elif args.command == 'template:compile':
		command_compile_template(args)
