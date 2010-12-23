# -*- coding: utf-8 -*-

import sys
import getopt
import re
import simplejson
import yaml

def print_usage_text():
	print """
Usage: python convert.py [args] [sqldumpfile] > [outputfile]

Options and arguments:
	--format [json|yaml]	-f [json|yaml]	: specify output format, can be either JSON or YAML
	--pretty-print		-p 		: indents output for eye-candy
	--help			-h		: this text
"""

pretty_print = False

try:
	optlist, args = getopt.getopt(sys.argv[1:], 'hpf:', ['help', 'pretty-print', 'format='])

except getopt.GetoptError:
	print_usage_text()
	sys.exit(2)
		
for opt, arg in optlist:
	if opt in ('-h', '--help'):
		print_usage_text()
		sys.exit()
		
	elif opt in ('-f', '--format'):
		format = arg

		if format not in ['json', 'yaml']:
			print_usage_text()
			sys.exit(2)

	elif opt in ('-p', '--pretty-print'):
		pretty_print = True
			
dumpfilename = sys.argv[-1]

try:
	dumpfile = open(dumpfilename, 'r')
except IOError:
	print "ERROR: File \"" + dumpfilename + "\" was not found."
	sys.exit(3)

# we only need the INSERTs as information
regex = re.compile(r"INSERT INTO [`'\"](?P<table>\w+)[`'\"] \((?P<columns>.+)\) VALUES\((?P<values>.+)\)")
rows = []

for line in dumpfile:
	match = regex.match(line)
	
	# non-INSERTS will be ignored
	if match:
 		table = match.group('table')

		# split parameters and remove their leading and trailing `-tags and whitespaces
		keys = map(lambda w: w.strip(" `'\""), match.group('columns').split(','))
		values = map(lambda w: w.strip(" `'\""), match.group('values').split(','))
	
		# convert data to dictionary and append to results
		rows.append(dict(map(lambda k,v: (k,v), keys, values)))
		if len(rows) == 10:
			break

if format == 'json':
	print simplejson.dumps(rows, indent="\t" if pretty_print else None)
elif format == 'yaml':
	print yaml.dump(rows, indent=4 if pretty_print else None)
