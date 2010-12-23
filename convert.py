import sys
import getopt

def print_usage_text():
	print """
Usage: python convert.py [args] [sqldumpfile]

Options and arguments:
	--format [xml|json]	-f [xml|json]	: specify output format, can be either JSON or XML
	--help			-h		: this text
"""

try:
	optlist, args = getopt.getopt(sys.argv[1:], 'hf:', ['help', 'format='])

except getopt.GetoptError:
	print_usage_text()
	sys.exit(2)
		
for opt, arg in optlist:
	if opt in ('-h', '--help'):
		print_usage_text()
		sys.exit()
		
	elif opt in ('-f', '--format'):
		format = arg

		if format not in ['json', 'xml']:
			print_usage_text()
			sys.exit(2)
			
dumpfilename = sys.argv[-1]

try:
	dumpfile = open(dumpfilename, 'r')
except IOError:
	print "ERROR: File \"" + dumpfilename + "\" was not found."
	sys.exit(3)
	
for line in dumpfile:
	pass