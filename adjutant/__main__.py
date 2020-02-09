import re
import os
import sys
import json
import glob
import base64

current_dir = os.getcwd()
sys.path.append(current_dir)





def pp_error(text):
	print("Error:")
	print(text)

def main():
	args = pp_cli()

	preprocessor = Preprocessor(
		
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
