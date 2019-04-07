import argparse
import dateutil.parser
import os
import sys

def build_parser():
	"""Build CLI parser"""
	parser = argparse.ArgumentParser(description=__doc__, formatter_class = argparse.ArgumentDefaultsHelpFormatter)
	parser.add_argument('range', nargs="+", help="the range for which to parse logs")
	parser.add_argument('-f', '--file', type=str, default="", required=False, help="a specific log file to parse")
	return parser

def parse_range(string):
	"""
	Parse the range given in the CLI
		:string: (str) desired range of logging
	"""
	if not ' to ' in string:
		errprint('Invalid format for range')
		sys.exit(1)

	start, end = string.split(' to ')[0], string.split(' to ')[1]
	if not is_date(start, fuzzy=False):
		errprint('Invalid format for start of range')
		sys.exit(1)
	if not is_date(end, fuzzy=False):
		errprint('Invalid format for end of range')
		sys.exit(1)
	return start, end

def is_date(date, fuzzy=False):
	"""
	Return whether the string can be interpreted as a date
		:string: (str) string to check for date
		:fuzzy: (bool) ignore unknown tokens in string if True
	"""
	try:
		dateutil.parser.parse(date, fuzzy=fuzzy)
		return True
	except ValueError:
		if date.lower() in ['today', 'yesterday']:
			return True
		return False

def acquire_log_files():
	return get_by_filetype(['log', 'logs'])

def get_by_filetype(filetypes):
	"""
	Get all files in the current directory that are a specific filetype
		:filetypes: (list) list of filetypes
	"""
	if not isinstance(filetypes, list):
		errprint("filetypes must be a list")
		sys.exit(1)

	files = []
	for filetype in filetypes:
		files += [file for file in os.listdir() if file.split('.')[-1] == filetype]
	return files

def errprint(*args, **kwargs):
	"""Print to stderr"""
	print(*args, file=sys.stderr, **kwargs)

def main():
	parser = build_parser()
	args = parser.parse_args()

	actual_range = ' '.join(args.range)
	parse_range(actual_range)

if __name__ == '__main__':
	main()
