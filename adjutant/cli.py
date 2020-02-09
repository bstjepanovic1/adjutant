import os
import argparse

from adjutant.processor import Processor
from adjutant.template import compile_template
from adjutant.utility import import_file

def command_process(args):
	# read source file
	content = ""
	if not os.path.exists(args.source):
		raise ValueError('Source not found!')
		return
	with open(args.source, "r") as f:
		content = f.read()
	
	# execute processor
	processor = Processor(
		source_filename=args.source,
		out_path=args.output,
		tpl_path=args.template_dir
	)

def command_build(args):
	pass

def command_compile_template(args, config):
	compile_template(args.source, args.output)

def adjutant_cli_main():
	# load configuration
	config_filename = os.path.join(os.getcwd(), 'adjutant.py')
	if os.path.exists(config_filename):
		config = import_file(config_filename)

	# parse arguments
	main_parser = argparse.ArgumentParser()
	subparsers = main_parser.add_subparsers(dest='command')

	# Process command
	parser = subparsers.add_parser('process', help="""
		Preprocesses source code file and generates one or more deriveded files
		using templates.
	""")
	parser.add_argument("source")
	parser.add_argument("--output", "-o", help="""
		Output directory
	""")
	parser.add_argument('--template-dir', "-t", help="""
		Path to directory that contains templates
	""")
	parser.add_argument('--dependency', '-d', help="""
		Generate prerequisite file
	""")
	parser.add_argument("--force", "-f", action="store_true")

	# build command
	parser = subparsers.add_parser("build", help="""
		Build project
	""")

	# Compile template command
	parser = subparsers.add_parser("template:compile", help="""
		Compile template into python file.
	""")
	parser.add_argument("source")
	parser.add_argument("--output", "-o")

	# execute
	args = main_parser.parse_args()

	if args.command == 'process':
		command_process(args)
	if args.command == 'template:compile':
		command_compile_template(args, config)
