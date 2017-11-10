#!/usr/bin/env python
import argparse
from datetime import datetime

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument('-i', dest='input_file', type=argparse.FileType('r'), action="store", required=True, 
		help="Provide the source loop times datafile to read.")

	args = parser.parse_args()
	file = args.input_file

	scanner = 0
	timestamp = None
	prev_timestamp = None
	for l in file:
		l = l.strip()
		if l[:7] == "Scanner":
			scanner = int(l[-1])
			prev_timestamp = None
			print "Scanner", scanner, "======================="
		else:
			date = l.split("]")[0].replace("NOTICE[", "").strip()
			timestamp = datetime.strptime(date, "%a %b %d %H:%M:%S %Y")
			if prev_timestamp != None:
				print (timestamp - prev_timestamp).seconds / 3600.0
			prev_timestamp = timestamp