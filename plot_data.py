#!/usr/bin/env python
import matplotlib.pyplot as plt

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

def plot_test_data():
	x = [1,2,3,4,5]
	y1 = [10,11,12,13,14]
	y2 = [11,12,None,14, 15]
	plt.figure(figsize=(12,10))
	plt.plot(x, y1, label="y1")
	plt.plot(x, y2, label="y2")
	plt.legend(loc='center left')
	plt.savefig('data-test.png')

def plot_data():
	x = []
	maatuska_all = []
	maatuska_hundred = []	
	maatuska_longclaw_all = []
	maatuska_longclaw_hundred = []
	maatuska_faravahar_all = []
	maatuska_faravahar_hundred = []
	maatuska_moria_all = []
	maatuska_moria_hundred = []

	datafile = "/var/lib/mysql-files/non-blank-lines.csv"
	f = open(datafile)
	for l in f:
		l = l.replace("\"", "").strip()
		p = l.split(",")
		x.append(int(p[0]))

		if p[1] != "\\N":
			maatuska_all.append(float(p[1]))
		else:
			maatuska_all.append(None)

		if p[2] != "\\N":
			maatuska_hundred .append(float(p[2]))
		else:
			maatuska_hundred .append(None)

		if p[3] != "\\N":
			maatuska_longclaw_all.append(float(p[3]))
		else:
			maatuska_longclaw_all.append(None)

		if p[4] != "\\N":
			maatuska_longclaw_hundred.append(float(p[4]))
		else:
			maatuska_longclaw_hundred.append(None)

		if p[5] != "\\N":
			maatuska_faravahar_all.append(float(p[5]))
		else:
			maatuska_faravahar_all.append(None)

		if p[6] != "\\N":
			maatuska_faravahar_hundred.append(float(p[6]))
		else:
			maatuska_faravahar_hundred.append(None)

		if p[7] != "\\N":
			maatuska_moria_all.append(float(p[7]))
		else:
			maatuska_moria_all.append(None)

		if p[8] != "\\N":
			maatuska_moria_hundred.append(float(p[8]))
		else:
			maatuska_moria_hundred.append(None)

	plt.figure(figsize=(16,12))
	plt.plot(x, maatuska_all, label='comp to maatuska2 all')
	plt.plot(x, maatuska_hundred, label='comp to maatuska2 >100')
	plt.plot(x, maatuska_longclaw_all, label='comp to longclaw all')
	plt.plot(x, maatuska_longclaw_hundred, label='comp to longclaw >100')
	plt.plot(x, maatuska_faravahar_all, label='comp to faravahar all')
	plt.plot(x, maatuska_faravahar_hundred, label='comp to faravahar >100')
	plt.plot(x, maatuska_moria_all, label='comp to moria all')
	plt.plot(x, maatuska_moria_hundred, label='comp to moria >100')
	plt.legend(loc='center left')


	plt.savefig('data.png')

if __name__ == "__main__":
	#plot_number_of_datapoints_per_line()
	plot_test_data()
	plot_data()