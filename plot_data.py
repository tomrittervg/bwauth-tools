#!/usr/bin/env python
import argparse
from datetime import datetime

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.dates as md
import matplotlib.ticker as ticker


def index_of_nth_min(series, n):
	mins = []
	for s in series:
		for i in range(len(s)):
			if s[i] != None:
				mins.append(i)
				break
	mins.sort()
	return mins[n]

def index_of_nth_max(series, n):
	maxes = []
	for s in series:
		for i in range(len(s)-1, 0, -1):
			if s[i] != None:
				maxes.append(i)
				break
	maxes.sort()
	maxes.reverse()
	return maxes[n]

def plot_number_of_datapoints_per_line():
	x = []
	y = []
	datafile = "/var/lib/mysql-files/data-per-line.txt"
	f = open(datafile)
	for l in f:
		p = l.split(" ")
		x.append(int(p[0]))
		y.append(int(p[1]))

	plt.plot(x, y)
	plt.savefig('data-per-line.png')

def plot_test_data(filename):
	x = [datetime.fromtimestamp(1),datetime.fromtimestamp(60),datetime.fromtimestamp(120),datetime.fromtimestamp(180),datetime.fromtimestamp(240)]
	y1 = [10,11,12,13,14]
	y2 = [11,12,None,14, 15]
	plt.figure(figsize=(12,10))
	plt.plot(x, y1, label="y1")
	plt.plot(x, y2, label="y2")
	plt.legend(loc='center left')
	plt.savefig(filename)

def plot_data(datafiles, filename, plot):
	global indexes
	x = []
	data = {}
	for i in indexes:
		data[i] = []

	# Read the data
	for l in datafiles[0]:
		l = l.replace("\"", "").strip()
		p = l.split(",")
		x.append(datetime.fromtimestamp(int(p[0])))
		#x.append(int(p[0]))

		for s in plot:
			if p[indexes[s]] != "\\N":
				data[s].append(float(p[indexes[s]]))
			else:
				data[s].append(None)


	# Trim the data
	series = []
	for s in plot:
		series.append(data[s])
	index_of_min = index_of_nth_min(series, 0)
	index_of_max = index_of_nth_max(series, 0)
	x = x[index_of_min : index_of_max+1]
	for s in plot:
		data[s] = data[s][index_of_min : index_of_max+1]

	# Plot
	plt.figure(figsize=(16,12))
	plt.xlabel("Consensus Time")
	plt.ylabel("% Difference")
	
	plt.ylim(30, 80)
	
	x_axis_formatter = md.DateFormatter('%Y-%m-%d %H:%M')
	axes=plt.gca()
	axes.xaxis.set_major_formatter(x_axis_formatter)
	axes.xaxis.set_major_locator(ticker.MultipleLocator(4))
	plt.gcf().autofmt_xdate()

	x=md.date2num(x)

	for s in plot:
		plt.plot(x, data[s], label='comp to ' + s)
	
	plt.legend(loc='upper left')
	
	plt.savefig(filename)

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument('-i', dest='input_files', type=argparse.FileType('r'), action="append", required=True, 
		help="Provide the source datafiles (query output) to read. (Currently only the first is used")
	parser.add_argument('-o', dest='output_file', action="store", required=True, 
		help="Provide the destination filepath for the graph")
	args = parser.parse_args()

	# This lines up with the order of the columns in the select query
	indexes = {
		'maatuska_vanilla_all' : 1,
		'maatuska_vanilla_hundred' : 2,
		'maatuska_nodns_all' : 3,
		'maatuska_nodns_hundred' : 4,
		'maatuska_21697_all' : 5,
		'maatuska_21697_hundred' : 6,
		'maatuska_fastly_all' : 7,
		'maatuska_fastly_hundred' : 8,
		'maatuska_bastet_all' : 9,
		'maatuska_bastet_hundred' : 10,
		'maatuska_faravahar_all' : 11,
		'maatuska_faravahar_hundred' : 12,
		'maatuska_moria_all' : 13,
		'maatuska_moria_hundred' : 14,
		'maatuska_gabelmoo_all' : 15,
		'maatuska_gabelmoo_hundred' : 16,
	}

	toplot = ['maatuska_gabelmoo_all', 'maatuska_gabelmoo_hundred']

	#plot_number_of_datapoints_per_line()
	#plot_test_data(args.output_file)
	plot_data(args.input_files, args.output_file, toplot)


