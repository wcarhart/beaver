import argparse
import calendar
import dateutil.parser
import datetime
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
		print(red("Invalid format for range"))
		sys.exit(1)

	start, end = string.split(' to ')[0], string.split(' to ')[1]

	start_datetime = validate_datetime(start)
	end_datetime = validate_datetime(end)
	validate_range(start_datetime, end_datetime)

	return start, end

def validate_date(date):
	"""
	Validate string as a date format
		:date: (str) the date to validate
	"""
	days = {
		'monday': 0,
		'tuesday': 1,
		'wednesday': 2,
		'thursday': 3,
		'friday': 4,
		'saturday': 5,
		'sunday': 6
	}
	months = {
		'january': 0, 'jan': 0,
		'february': 1, 'feb': 1,
		'march': 2, 'mar': 2,
		'april': 3, 'apr': 3,
		'may': 4,
		'june': 5, 'jun': 5,
		'july': 6, 'jul': 6,
		'august': 7, 'aug': 7,
		'september': 8, 'sept': 8, 'sep': 8,
		'october': 9, 'oct': 9,
		'november': 10, 'nov': 10,
		'december': 11, 'dec': 11
	}
	today = datetime.date.today()
	day = today.day
	month = today.month
	year = today.year

	if date in days:
		# name of day
		day_delta = today.weekday() - days[date]
		day_delta += 7 if day_delta < 0 else 0
		new_date = datetime.datetime.now() - datetime.timedelta(days=day_delta)
	elif not len(set(date.split()).intersection(set(months))) == 0:
		# name of month in format
		elements = date.split()
		if len(elements) == 1:
			# just month
			month_delta = today.month - 1 - months[date]
			temp_year = today.year
			if month_delta < 0:
				month_delta += 12
				temp_year -= 1

			new_date = datetime.datetime(day=1, month=months[date]+1, year=temp_year)
		elif len(elements) == 2:
			# month + day
			temp_month = elements[0] if elements[0].isalpha() else elements[1]
			elements.remove(temp_month)
			temp_day = elements[0]
			temp_day = ''.join(char for char in temp_day if char.isdigit())

			month_delta = today.month - 1 - months[temp_month]
			temp_year = today.year
			if month_delta < 0:
				month_delta += 12
				temp_year -= 1

			new_date = datetime.datetime(day=int(temp_day), month=int(months[temp_month]+1), year=int(temp_year))
		elif len(elements) == 3:
			# month + day + year
			temp_month = [e for e in elements if e.isalpha()][0]
			elements.remove(temp_month)
			elements = [''.join([char for char in e if char.isdigit()]) for e in elements]
			temp_day = elements[0] if len(elements[0]) < len(elements[1]) else elements[1]
			elements.remove(temp_day)
			temp_year = elements[0]
			new_date = datetime.datetime(day=int(temp_day), month=int(months[temp_month]+1), year=int(temp_year))
		else:
			# invalid
			print(red("Could not determine date format"))
			sys.exit(1)
	elif '/' in date:
		# day, month, year separated by /
		elements = date.split('/')
		if len(elements) == 2:
			new_date = datetime.datetime(day=int(elements[1]), month=int(elements[0]), year=today.year)
			if datetime.datetime.now() < new_date:
				new_date = datetime.datetime(day=new_date.day, month=new_date.month, year=today.year-1)
		else:
			new_date = dateutil.parser.parse(date)
	elif '\'' in date:
		# day, month, year separated by \
		elements = date.split('\'')
		if len(elements) == 2:
			new_date = datetime.datetime(day=int(elements[1]), month=int(elements[0]), year=today.year)
			if datetime.datetime.now() < new_date:
				new_date = datetime.datetime(day=new_date.day, month=new_date.month, year=today.year-1)
		else:
			new_date = dateutil.parser.parse(date)
	elif '-' in date:
		# day, month, year separated by -
		elements = date.split('-')
		if len(elements) == 2:
			new_date = datetime.datetime(day=int(elements[1]), month=int(elements[0]), year=today.year)
			if datetime.datetime.now() < new_date:
				new_date = datetime.datetime(day=new_date.day, month=new_date.month, year=today.year-1)
		else:
			new_date = dateutil.parser.parse(date)
	else:
		print(red("Could not determine date format"))
		sys.exit(1)

	day = new_date.day
	month = new_date.month
	year = new_date.year

	return year, month, day

def validate_time(time):
	"""
	Validate string as a time format
		:time: (str) the time to validate
	"""

	if time == '':
		hours = '0'
		minutes = '0'
		seconds = '0'
	else:
		if ':' in time:
			hours, minutes, seconds = tuple(time.split(':') if len(time.split(':')) == 3 else time.split(':')+['0'])
		else:
			hours = time
			minutes = seconds = '0'

		if 'am' in hours or 'am' in minutes or 'am' in seconds:
			is_am = True
			is_24 = False
			hours = hours.replace('am', '')
			minutes = minutes.replace('am', '')
			seconds = seconds.replace('am', '')
		elif 'pm' in hours or 'pm' in minutes or 'pm' in seconds:
			is_am = False
			is_24 = False
			hours = hours.replace('pm', '')
			minutes = minutes.replace('pm', '')
			seconds = seconds.replace('pm', '')
		else:
			is_24 = True

		if not is_24:
			if not is_am:
				hours = str(int(hours) + 12)

	if not hours.isdigit() or not minutes.isdigit() or not seconds.isdigit():
		print(hours, minutes, seconds)
		print(red("Could not determine time format"))
		sys.exit(1)

	return int(hours), int(minutes), int(seconds)

def validate_datetime(string):
	"""
	Validate datetime given in range

	Follows these steps:
		0. Shortcuts
		1. Parse by keywords (on, at), or check if contains date and/or time
		2. Parse time
		3. Parse date
	"""
	# Shortcuts
	shortcuts = ['today', 'yesterday', 'now']
	if string in shortcuts:
		if string == 'today' or string == 'now':
			return datetime.datetime.today()
		elif string == 'yesterday':
			return datetime.datetime.now() - datetime.timedelta(days=1)

	time = date = ''

	# Parse by keywords (on, at)
	if ' on ' in string:
		# `time` on `date`
		time, date = string.split(' on ')[0], string.split(' on ')[1]
	elif ' at ' in string:
		# `date` at `time`
		time, date = string.split(' at ')[1], string.split(' at ')[0]
	else:
		if ':' in string:
			# contains time
			time_index = [index for index, s in enumerate(string.split()) if ':' in s][0]
			time = string[time_index:]
			date = string[:time_index]
		elif len(string.split()) == 1 and ('am' in string.lower() or 'pm' in string.lower()):
			# contains only time
			time = string
		else:
			# does not contain time
			date = string

	time = time.strip()
	date = date.strip()
	time = ''.join([t.lower() for t in time])
	date = ''.join([d.lower() for d in date])

	# Parse time
	hours, minutes, seconds = validate_time(time)

	# Parse date
	year, month, day = validate_date(date)

	return datetime.datetime(year=year, month=month, day=day, hour=hours, minute=minutes, second=seconds)

def validate_range(start, end):
	"""
	Validate the range of two datetimes
		:start: (datetime) the start of the range
		:end: (datetime) the end of the range
	"""
	if start > end:
		print(red("End of range occurs before start of range"))
		sys.exit(1)

	if end > datetime.datetime.now():
		print(red("End of range hasn't happened yet"))
		sys.exit(1)

def acquire_log_files():
	"""
	Get all files ending in .log or .logs
	"""
	return get_by_filetype(['log', 'logs'])

def get_by_filetype(filetypes):
	"""
	Get all files in the current directory that are a specific filetype
		:filetypes: (list) list of filetypes
	"""
	if not isinstance(filetypes, list):
		print(red("filetypes must be a list"))
		sys.exit(1)

	files = []
	for filetype in filetypes:
		files += [file for file in os.listdir() if file.split('.')[-1] == filetype]
	return files

def red(string):
	"""
	Convert a string to red text
		:string: the string to convert to red text
	"""
	return f'\033[91m{string}\033[0m'

def main():
	parser = build_parser()
	args = parser.parse_args()

	actual_range = ' '.join(args.range)
	start,end = parse_range(actual_range)

	if args.file:
		if os.path.isfile(args.file):
			files = args.file
		else:
			print(red(f"Could not file file {args.file}"))
	else:
		files = acquire_log_files()

if __name__ == '__main__':
	main()
