#!/usr/bin/env python

import os
import pytz
import urllib
from datetime import datetime, timedelta

bwauths = {
	'maatuska' : {
		'url' : 'https://bwauth.ritter.vg/bwauth/',
		'dl_location' : 'data/maatuska',
		'file_minute' : '45',
		'tz' : 'Canada/Central',
		'give_up_after' : 10
		}
}

def find_files(location):
	filenames = []
	for root, dirs, files in os.walk(location):
		for f in files:
			filenames.append(f)
	return filenames

def make_dir_structure(base, dt):
	year = str(dt.year)
	year_d = os.path.join(base, year)
	month = str(dt.month)
	month_d = os.path.join(year_d, month)

	if not os.path.isdir(year_d):
		os.mkdir(year_d)
	if not os.path.exists(month_d):
		os.mkdir(month_d)

def current_filetime(bwauth):
	tz = pytz.timezone(bwauth['tz'])
	dt = datetime.now(tz)
	return datetime(dt.year, dt.month, dt.day, dt.hour, int(bwauth['file_minute']), 0, 0, tz)

def filetime_to_filename(bwauth, dt):
	return dt.strftime('bwscan.%Y%m%d-%H') + bwauth['file_minute']	

def wget(bwauth, filetime):
	filename = filetime_to_filename(bwauth, filetime)
	url = bwauth['url'] + filename
	destination = os.path.join(bwauth['dl_location'], str(filetime.year), str(filetime.month), filename)
	
	make_dir_structure(bwauth['dl_location'], filetime)
	f = urllib.URLopener()
	try:
		filename, headers = f.retrieve(url, destination)
		print "Downloading", url, "to", destination, ": Success"
		return True
	except: 
		print "Downloading", url, "to", destination, ": 404"
		return False


def download(name, bwauth):
	filenames = find_files(bwauth['dl_location'])
	current_time = current_filetime(bwauth)
	current_name = filetime_to_filename(bwauth, current_time)

	this_time = current_time
	num_missing_in_a_row = 0
	while num_missing_in_a_row < bwauth['give_up_after']:
		this_name = filetime_to_filename(bwauth, this_time)
		if this_name not in filenames:
			if wget(bwauth, this_time):
				num_missing_in_a_row = 0
			else:
				num_missing_in_a_row += 1
		else:
			print "Skipping", this_name
		this_time -= timedelta(hours=1)


def download_all():
	for k in bwauths:
		download(k, bwauths[k])


if __name__ == "__main__":
	download_all()