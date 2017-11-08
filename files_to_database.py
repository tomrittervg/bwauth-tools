#!/usr/bin/env python

import os
import sys
import json
import pytz
import base64
import MySQLdb
import requests
import binascii
from datetime import datetime, timedelta, time

from database_creds import *

TYPE_BWAUTH_VOTE = 1
TYPE_DIRAUTH_VOTE = 2

def from_unixtime(t):
	x = datetime.utcfromtimestamp(t)
	return x - timedelta(seconds=(x.minute*60) + x.second)
def to_unixtime(dt):
	return (dt - datetime.utcfromtimestamp(0)).total_seconds()

class bwauth_relay_data:
	line_type = None
	bwauth_id = None
	bwauth_name = None
	timestamp = None
	fingerprint = None
	bw = None
	measured_bw = None
	measured_at = None
	updated_at = None
	scanner = None

	def _parse_bwauth_vote(self, l):
		self.line_type = TYPE_BWAUTH_VOTE
		parts = l.split(' ')
		for p in parts:
			if p.startswith('node_id='):
				self.fingerprint = binascii.unhexlify(p.split('=')[1].replace("$", ""))
				self.fingerprint_print = binascii.hexlify(self.fingerprint)
			elif p.startswith('bw='):
				self.bw = int(p.split('=')[1])
			elif p.startswith('measured_at='):
				self.measured_at = int(p.split('=')[1])
			elif p.startswith('updated_at='):
				self.updated_at = int(p.split('=')[1])
			elif p.startswith('scanner='):
				self.scanner = int(p.split('=')[1][9])
	def _parse_dirauth_vote(self, data):
		self.line_type = TYPE_DIRAUTH_VOTE
		self.fingerprint = data['fingerprint']
		self.fingerprint_print = binascii.hexlify(data['fingerprint'])
		self.bw = int(data['bw'])
		if 'measured' in data:
			self.measured_bw = int(data['measured'])

	def __init__(self, line_type, bwauth, timestamp, data):
		self.bwauth_name = bwauth[0]
		self.bwauth_id = int(bwauth[1])
		self.timestamp = int(to_unixtime(timestamp))
		if line_type == TYPE_BWAUTH_VOTE:
			self._parse_bwauth_vote(data)
		elif line_type == TYPE_DIRAUTH_VOTE:
			self._parse_dirauth_vote(data)
		else:
			raise Exception("Do not know how to parse this line type")

	def valid(self):
		if self.line_type == TYPE_BWAUTH_VOTE:
			fields = (self.fingerprint, self.bw, self.measured_at, self.updated_at, self.scanner)
		elif self.line_type == TYPE_DIRAUTH_VOTE:
			fields = (self.fingerprint, self.bw)
		else:
			raise Exception("Do not know how to parse this line type") 
		return 0 == len(filter(lambda a : a is None, fields))
	def save(self):
		global db
		c = db.cursor()

		if self.line_type == TYPE_BWAUTH_VOTE:
			cols = "timestamp, fingerprint, bwauth, bw, measured_at, updated_at, scanner"
			vals = "%s, _binary %s, %s, %s, %s, %s, %s"
			data = (self.timestamp, self.fingerprint, self.bwauth_id, self.bw, self.measured_at, self.updated_at, self.scanner)
		elif self.line_type == TYPE_DIRAUTH_VOTE:
			cols = "timestamp, fingerprint, bwauth, bw, measured_bw"
			vals = "%s, _binary %s, %s, %s, %s"
			data = (self.timestamp, self.fingerprint, self.bwauth_id, self.bw, self.measured_bw)
		else:
			raise Exception("Error saving unknown type") 

		c.execute("INSERT INTO relays("+cols+") VALUES("+vals+")", data)

	def __str__(self):
		s = self.bwauth_name + "(" + str(self.bwauth_id) + " " + str(self.timestamp) + ") " + self.fingerprint_print + " : " + str(self.bw)
		if self.line_type == TYPE_BWAUTH_VOTE:
			s += "  m:" + str(self.measured_at) + ", u:" + str(self.updated_at) + ", scanner:" + str(self.scanner)
		elif self.line_type == TYPE_DIRAUTH_VOTE:
			s += "  mbw:" + str(self.measured_bw)
		return s

##########################################
bwauths = None
def bwauth_from_filename(filename):
	global db, bwauths
	if not bwauths:
		bwauths = {}
		c = db.cursor()
		c.execute("SELECT * FROM bwauths")
		for row in c:
			bwauths[row[1]] = row[0]

	b = filename.split("/")[1]
	if b not in bwauths:
		raise Exception("The bwauth " + b + " is not present in the bwauth table")
	return b, bwauths[b]

def find_files(location):
	filenames = []
	for root, dirs, files in os.walk(location):
		for f in files:
			filenames.append(os.path.join(root, f))
	return filenames

def parse_file_raw_bwauth_vote(filename):
	f = open(filename)

	bwauth = bwauth_from_filename(filename)
	timestamp = None
	for l in f.readlines():
		l = l.strip()

		if not timestamp:
			timestamp = from_unixtime(int(l))
			continue

		line = bwauth_relay_data(TYPE_BWAUTH_VOTE, bwauth, timestamp, l)
		if not line.valid():
			raise Exception("bwauth vote line was invalid: " + l)
		line.save()

def parse_file_dirauth_vote(filename):
	f = open(filename)
	
	# State Machine
	MODE_TIMETAMP = 0
	MODE_RELAY = 1
	MODE_BANDWIDTH = 2
	MODE_PROCESS = 3
	mode = MODE_TIMETAMP

	bwauth = bwauth_from_filename(filename)
	timestamp = None
	for l in f.readlines():
		l = l.strip()
		if mode == MODE_TIMETAMP and l.startswith('valid-after'):
			l = l.replace("valid-after ", "")
			timestamp = datetime.strptime(l, "%Y-%m-%d %H:%M:%S")
			mode = MODE_RELAY
		elif mode == MODE_RELAY and l.startswith('r '):
			parts = l.split(" ")
			data = {}

			data['nickname'] = parts[1]
			# fun trick: you can add as much padding as you like so add enough to cover all possible missing padding
			data['fingerprint'] = base64.b64decode(parts[2] + "====")
			mode = MODE_BANDWIDTH
		elif mode == MODE_BANDWIDTH and l.startswith('w '):
			parts = l.split(' ')
			data['bw'] = int(parts[1].split('=')[1])
			if len(parts) > 2:
				data['measured'] = int(parts[2].split('=')[1])
			mode = MODE_PROCESS
		elif mode == MODE_BANDWIDTH and l.startswith('r '):
			raise Exception("Error, found a new relay line while I was looking for a bandwidth line for " + nickname)

		if mode == MODE_PROCESS:
			line = bwauth_relay_data(TYPE_DIRAUTH_VOTE, bwauth, timestamp, data)
			if not line.valid():
				raise Exception("dirauth relay was invalid: " + data['nickname'])
			line.save()
			mode = MODE_RELAY

# See if we already processed this file
def should_parse_file(filename):
	global db
	c = db.cursor()
	c.execute("SELECT * FROM files WHERE name = %s", (filename,))
	if c.fetchone():
		return False
	return True
def record_file(filename):
	global db
	c = db.cursor()
	c.execute("INSERT INTO files(name) VALUES(%s)", (filename,))
	db.commit()

def parse_file(filename):
	if not should_parse_file(filename):
		print "Already processed", filename
		return
	print "Processing ", filename

	if 'moria' in filename or 'bwscan.' in filename:
		parse_file_raw_bwauth_vote(filename)
	elif '-vote-' in filename:
		parse_file_dirauth_vote(filename)
	else:
		raise Exception("Don't know how to parse " + filename)
	record_file(filename)


db = None
if __name__ == "__main__":
	for ts in [3600, 2030400, 16513200]:
		c = to_unixtime(from_unixtime(ts))
		if c != ts:
			raise Exception("Timetsamp conversion is wrong: " + str(ts) + " " + str(c))

	db = MySQLdb.connect(host=database_host, user=database_user, passwd=database_pass, db=database_name)

	filenames = find_files('data/')
	for f in filenames:
		parse_file(f)