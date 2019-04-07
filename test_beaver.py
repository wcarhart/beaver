import unittest
from beaver import *

class TestBeaver(unittest.TestCase):
	def test_parse_range_happy_path(self):
		happy_ranges = [
			'8:30am to 10:30pm',
			'8:30 am to 10:30 pm',
			'8:30am to 10:30pm PDT',
			'8:30am to 10:30 pm PST',
			'12:30 to 15:30',
			'May 1st 16:30 to May 1st 16:45',
			'2019-04-06 8:15am to 2019-04-06 8:20am PDT',
			'yesterday to today',
			'4/6 to 4/7'
			'Monday to Thursday'
			'monday to friday'
		]

		for happy_range in happy_ranges:
			_, _ = parse_range(happy_range)

	def test_parse_range_sad_path(self):
		sad_ranges = [
			'',
			'hello',
			' to ',
			'a to b',
			'am8:30 am to 10:30 pm',
			'tomorrow to today',
			'May 82nd 16:30 to May 1st 16:45',
		]

		for sad_range in sad_ranges:
			with self.assertRaises(SystemExit) as e:
				start, end = parse_range(sad_range)
				print(start, end)
			self.assertEqual(e.exception.code, 1)

if __name__ == '__main__':
	unittest.main()
