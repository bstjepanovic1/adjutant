import os
import argparse


def adjutant_cli_main():
	parser = argparse.ArgumentParser(description="""
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

	args = parser.parse_args()

	# read source file
	content = ""
	if not os.path.exists(args.source):
		raise ValueError('Source not found!')
		return
	with open(args.source, "r") as f:
		content = f.read()
	
	# execute processor
