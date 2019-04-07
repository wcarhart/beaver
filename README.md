# beaver
*Beaver (n) - an animal that eats logs*

`beaver` parses log files based on a given date and time range, so you don't have to

### Quick Examples
Perhaps you'd like to see the logs for your project since the last time you pushed to production last Wednesday. This can be accomplished easily with `beaver`:
```
$ python3 beaver.py Wednesday to today
>> logfile1.log
2019-04-03 15:10:26,618 - simple_example - DEBUG - debug message
2019-04-03 15:12:45,124 - simple_example - DEBUG - debug message
...
```
All of the following examples will work:
```
python3 beaver.py 10:35 to 11:35
python3 beaver.py yesterday to today
python3 beaver.py Mar 2nd, 2012 to now
python3 beaver.py 2017-06-18 to May 3rd 2018 at 3:17pm
python3 beaver.py 1:23pm on August 15th 2017 to 10:35 PM on 2 April 2018
```
...and many more!

### Installation
More coming soon...

### Usage
```
usage: beaver.py [-h] [-f FILE] [-o OUTPUT] [-r] range [range ...]

Beaver (n) - an animal that eats logs

positional arguments:
  range                 the range for which to parse logs

optional arguments:
  -h, --help            show this help message and exit
  -f FILE, --file FILE  a specific log file to parse (default: )
  -o OUTPUT, --output OUTPUT
                        if included, the file to which output will be writen
                        (default: )
  -r, --recursive       if included, beaver will search for log files
                        recursively starting from the current directory
                        (default: False)
```
 * `range` is composed in the form of `START to END`, where START and END can be almost any valid datetime format. If `beaver` can't understand you, it will ask for clarification. 
   * Note that any datetime format that contains days, months, and years must either have days > months > years or years > months > days. The American format (06/18/1996 for June 18th, 1996) is not supported because it creates ambiguity.
 * `--file` - use this if you only want to parse a specific file, not all log files. By default, `beaver` searches the current directory for any files ending in `.log` or `.logs`
 * `--output` - write output to a file, rather than `stdout`
 * `--recursive` - look for log files recursively, starting in the current directory
 
 ### [( θ ϖ θ )](https://preview.redd.it/7wxghzo7vhc21.jpg?width=624&auto=webp&s=b6c863b2dec6f0c0d8746c4665bb29412ed4782f)
