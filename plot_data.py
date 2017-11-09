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

def plot_data(datafiles, filename, dohundred=False):
	x = []
	maatuska_vanilla_all = []
	maatuska_vanilla_hundred = []
	maatuska_nodns_all = []
	maatuska_nodns_hundred = []
	maatuska_bastet_all = []
	maatuska_bastet_hundred = []
	maatuska_faravahar_all = []
	maatuska_faravahar_hundred = []
	maatuska_moria_all = []
	maatuska_moria_hundred = []

	# Read the data
	for l in datafiles[0]:
		l = l.replace("\"", "").strip()
		p = l.split(",")
		x.append(datetime.fromtimestamp(int(p[0])))
		#x.append(int(p[0]))

		if p[1] != "\\N":
			maatuska_vanilla_all.append(float(p[1]))
		else:
			maatuska_vanilla_all.append(None)

		if dohundred:
			if p[2] != "\\N":
				maatuska_vanilla_hundred.append(float(p[2]))
			else:
				maatuska_vanilla_hundred.append(None)

		if p[3] != "\\N":
			maatuska_nodns_all.append(float(p[3]))
		else:
			maatuska_nodns_all.append(None)

		if dohundred:
			if p[4] != "\\N":
				maatuska_nodns_hundred.append(float(p[4]))
			else:
				maatuska_nodns_hundred.append(None)

		if p[5] != "\\N":
			maatuska_bastet_all.append(float(p[5]))
		else:
			maatuska_bastet_all.append(None)

		if dohundred:
			if p[6] != "\\N":
				maatuska_bastet_hundred.append(float(p[6]))
			else:
				maatuska_bastet_hundred.append(None)

		if p[7] != "\\N":
			maatuska_faravahar_all.append(float(p[7]))
		else:
			maatuska_faravahar_all.append(None)

		if dohundred:
			if p[8] != "\\N":
				maatuska_faravahar_hundred.append(float(p[8]))
			else:
				maatuska_faravahar_hundred.append(None)

		if p[9] != "\\N":
			maatuska_moria_all.append(float(p[9]))
		else:
			maatuska_moria_all.append(None)

		if dohundred:
			if p[10] != "\\N":
				maatuska_moria_hundred.append(float(p[10]))
			else:
				maatuska_moria_hundred.append(None)

	# Trim the data
	series = [maatuska_vanilla_all, maatuska_nodns_all, maatuska_bastet_all, maatuska_faravahar_all, maatuska_moria_all]
	#series = [maatuska_bastet_all]
	index_of_min = index_of_nth_min(series, 0)
	index_of_max = index_of_nth_max(series, 0)

	x = x[index_of_min : index_of_max+1]
	maatuska_vanilla_all = maatuska_vanilla_all[index_of_min : index_of_max+1]
	maatuska_nodns_all = maatuska_nodns_all[index_of_min : index_of_max+1]
	maatuska_bastet_all = maatuska_bastet_all[index_of_min : index_of_max+1]
	maatuska_faravahar_all = maatuska_faravahar_all[index_of_min : index_of_max+1]
	maatuska_moria_all = maatuska_moria_all[index_of_min : index_of_max+1]
	if dohundred:
		maatuska_vanilla_hundred = maatuska_vanilla_hundred[index_of_min : index_of_max+1]
		maatuska_nodns_hundred = maatuska_nodns_hundred[index_of_min : index_of_max+1]
		maatuska_bastet_hundred = maatuska_bastet_hundred[index_of_min : index_of_max+1]
		maatuska_faravahar_hundred = maatuska_faravahar_hundred[index_of_min : index_of_max+1]
		maatuska_moria_hundred = maatuska_moria_hundred[index_of_min : index_of_max+1]


	# Plot
	plt.figure(figsize=(16,12))
	plt.xlabel("Consensus Time")
	plt.ylabel("% Difference")
	
	plt.ylim(20, 60)
	
	x_axis_formatter = md.DateFormatter('%Y-%m-%d %H:%M')
	axes=plt.gca()
	axes.xaxis.set_major_formatter(x_axis_formatter)
	axes.xaxis.set_major_locator(ticker.MultipleLocator(1.6))
	plt.gcf().autofmt_xdate()

	x=md.date2num(x)

	plt.plot(x, maatuska_vanilla_all, label='comp to maatuska-vanilla all')
	if dohundred: plt.plot(x, maatuska_vanilla_hundred, label='comp to maatuska-vanilla >100')
	plt.plot(x, maatuska_nodns_all, label='comp to maatuska-nodns all')
	if dohundred: plt.plot(x, maatuska_nodns_hundred, label='comp to maatuska-nodns >100')
	plt.plot(x, maatuska_bastet_all, label='comp to bastet all')
	if dohundred: plt.plot(x, maatuska_bastet_hundred, label='comp to bastet >100')
	plt.plot(x, maatuska_faravahar_all, label='comp to faravahar all')
	if dohundred: plt.plot(x, maatuska_faravahar_hundred, label='comp to faravahar >100')
	plt.plot(x, maatuska_moria_all, label='comp to moria all')
	if dohundred: plt.plot(x, maatuska_moria_hundred, label='comp to moria >100')
	
	plt.legend(loc='upper left')
	
	plt.savefig(filename)

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument('-i', dest='input_files', type=argparse.FileType('r'), action="append", required=True, 
		help="Provide the source datafiles (query output) to read. (Currently only the first is used")
	parser.add_argument('-o', dest='output_file', action="store", required=True, 
		help="Provide the destination filepath for the graph")
	args = parser.parse_args()

	#plot_number_of_datapoints_per_line()
	#plot_test_data(args.output_file)
	plot_data(args.input_files, args.output_file, False)