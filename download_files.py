#!/usr/bin/env python

import os
import sys
import json
import pytz
import requests
from datetime import datetime, timedelta


bwauths = {
	'moria1' : {
		'type' : 'hourly',
		'dl_location' : 'data/moria1',
		'url' : 'https://www.freehaven.net/~arma/bwscan.V3BandwidthsFile',
		'file_minute' : '10',
		'tz' : 'UTC',
		},
	'maatuska' : {
		'type' : 'archived',
		'dl_location' : 'data/maatuska',
		'url' : 'https://bwauth.ritter.vg/bwauth/',
		'file_minute' : '45',
		'tz' : 'Canada/Central',
		'give_up_after' : 10
		},
	'maatuska2-vanilla' : {
		'type' : 'archived',
		'dl_location' : 'data/maatuska-vanilla',
		'url':  'https://bwauth.ritter.vg/bwauth-patches/',
		# We only support one currently active 'variant' from a source, so we will mark the 'before-date'
		# and if today > before-date this variant cannot be active and we continue to look
		# Additionally, we only place a 'before-date' value when we have rotated, so this can be human readable
		# and in the script we just check for its presence
		'before-date' : 'Thu, 26 Oct 2017 16:20:23 -0500',
		'file_minute' : '45',
		'tz' : 'Canada/Central',
		'give_up_after' : 10
		},
	'maatuska2-nodns' : {
		'type' : 'archived',
		'dl_location' : 'data/maatuska-nodns',
		'url':  'https://bwauth.ritter.vg/bwauth-patches/',
		'before-date' : 'Thu, 7 Nov 2017 23:46:00 -0500',
		'not-before' : datetime(year=2017, month=10, day=26, hour=17, tzinfo=pytz.timezone('Canada/Central')),
		'file_minute' : '45',
		'tz' : 'Canada/Central',
		'give_up_after' : 10
		},
	'maatuska2-nofasthop' : {
		'type' : 'archived',
		'dl_location' : 'data/maatuska-nofasthop',
		'url':  'https://bwauth.ritter.vg/bwauth-patches/',
		'before-date' : 'Thu, 8 Nov 2017 22:11:00 -0500',
		'not-before' : datetime(year=2017, month=11, day=7, hour=23, tzinfo=pytz.timezone('Canada/Central')),
		'file_minute' : '45',
		'tz' : 'Canada/Central',
		'give_up_after' : 10
		},
	'maatuska2-21697' : {
		'type' : 'archived',
		'dl_location' : 'data/maatuska-21697',
		'url':  'https://bwauth.ritter.vg/bwauth-patches/',
		'not-before' : datetime(year=2017, month=11, day=8, hour=22, tzinfo=pytz.timezone('Canada/Central')),
		'file_minute' : '45',
		'tz' : 'Canada/Central',
		'give_up_after' : 10
		},
	'bastet' : {
		'type' : 'vote',
		'dl_location' : 'data/bastet',
		'url' : 'https://collector.torproject.org/recent/relay-descriptors/votes/',
		'fingerprint' : '27102BC123E7AF1D4741AE047E160C91ADC76B21',
		'file_minute' : '00',
		'tz' : 'UTC',
		'give_up_after' : 5
		},
	'faravahar' : {
		'type' : 'vote',
		'dl_location' : 'data/faravahar',
		'url' : 'https://collector.torproject.org/recent/relay-descriptors/votes/',
		'fingerprint' : 'EFCBE720AB3A82B99F9E953CD5BF50F7EEFC7B97',
		'file_minute' : '00',
		'tz' : 'UTC',
		'give_up_after' : 5
		},
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

	if not os.path.isdir(base):
		os.mkdir(base)
	if not os.path.isdir(year_d):
		os.mkdir(year_d)
	if not os.path.exists(month_d):
		os.mkdir(month_d)

def current_filetime(bwauth):
	tz = pytz.timezone(bwauth['tz'])
	dt = datetime.now(tz)
	return datetime(dt.year, dt.month, dt.day, dt.hour, int(bwauth['file_minute']), 0, 0, tz)

def filetime_to_filename(bwauth, dt):
	if bwauth['type'] == 'archived':
		return dt.strftime('bwscan.%Y%m%d-%H') + bwauth['file_minute']
	elif bwauth['type'] == 'vote':
		return dt.strftime('%Y-%m-%d-%H-') + bwauth['file_minute'] + '-00-vote-' + bwauth['fingerprint']
	elif bwauth['type'] == 'hourly':
		return dt.strftime('%Y-%m-%d-%H-') + bwauth['file_minute'] + '-00'
	else:
		raise Exception("Do not know how to format filetime for " + bwauth['dl_location'])

def wget(url, destination):
	try:
		r = requests.get(url, stream=True)
		if r.status_code == 404:
			return False
		h = open(destination, "wb")
		for chunk in r.iter_content(chunk_size=512):
			if chunk:  # filter out keep-alive new chunks
				h.write(chunk)
		print "Downloading", url, "to", destination, ": Success"
		return True
	except Exception as e: 
		print e
		return False

def download_archived(name, bwauth):
	filenames = find_files(bwauth['dl_location'])
	current_time = current_filetime(bwauth)
	current_name = filetime_to_filename(bwauth, current_time)

	this_time = current_time
	num_missing_in_a_row = 0
	while num_missing_in_a_row < bwauth['give_up_after']:
		this_name = filetime_to_filename(bwauth, this_time)
		if this_name not in filenames:
			url = bwauth['url'] + this_name
			destination = os.path.join(bwauth['dl_location'], str(this_time.year), str(this_time.month), this_name)
			make_dir_structure(bwauth['dl_location'], this_time)

			if wget(url, destination):
				num_missing_in_a_row = 0
			else:
				num_missing_in_a_row += 1
		else:
			pass
			#print "Skipping", this_name
		this_time -= timedelta(hours=1)
		if 'not-before' in bwauth and bwauth['not-before'] > this_time:
			print "We reached the not-before time, stopping"
			break

def download_hourly(name, bwauth):
	filenames = find_files(bwauth['dl_location'])
	current_time = current_filetime(bwauth)
	current_name = filetime_to_filename(bwauth, current_time)

	url = bwauth['url']
	destination = os.path.join(bwauth['dl_location'], str(current_time.year), str(current_time.month), current_name)
	make_dir_structure(bwauth['dl_location'], current_time)

	wget(url, destination)

def download_vote(name, bwauth):
	def get_url(name_base):
		url = None
		for i in jindex['directories']:
			if i['path'] == 'recent':
				for j in i['directories']:
					if j['path'] == 'relay-descriptors':
						for k in j['directories']:
							if k['path'] == 'votes':
								for l in k['files']:
									if name_base in l['path']:
										url = bwauth['url'] + l['path']
		return url

	filenames = find_files(bwauth['dl_location'])
	current_time = current_filetime(bwauth)
	current_name = filetime_to_filename(bwauth, current_time)

	r = requests.get('https://collector.torproject.org/index/index.json')
	jindex = json.loads(r.text)

	this_time = current_time
	num_missing_in_a_row = 0
	while num_missing_in_a_row < bwauth['give_up_after']:
		this_name = filetime_to_filename(bwauth, this_time)
		if this_name not in filenames:
			url = get_url(this_name)
			destination = os.path.join(bwauth['dl_location'], str(this_time.year), str(this_time.month), this_name)
			make_dir_structure(bwauth['dl_location'], this_time)
			if url and wget(url, destination):
				num_missing_in_a_row = 0
			else:
				num_missing_in_a_row += 1
		else:
			pass
			#print "Skipping", this_name
		this_time -= timedelta(hours=1)

def download(name, bwauth):
	if bwauth['type'] == 'archived':
		download_archived(name, bwauth)
	elif bwauth['type'] == 'vote':
		download_vote(name, bwauth)
	elif bwauth['type'] == 'hourly':
		download_hourly(name, bwauth)
	else:
		raise Exception("Do not know how to download files from " + name)

def download_all():
	for k in bwauths:
		if 'before-date' in bwauths[k]:
			print "Skipping", k, "because we only download data from it before", bwauths[k]['before-date']
		else:
			print "Downloading", k
			download(k, bwauths[k])


if __name__ == "__main__":
	download_all()