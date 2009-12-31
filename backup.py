#!/usr/bin/env python
# encoding: utf-8
"""
backup.py

Created by Max Johnson on 2009-08-17.
Copyright (c) 2009 __MyCompanyName__. All rights reserved.
"""

import sys
import os
import unittest
import plistlib
from iTunesMac import *

class BackupDB(object):
	def __init__(self, path):
		self.path = path
		try:
			self.pl = plistlib.readPlist(path)
		except:
			self.pl = dict()
	
	def store(self, track):
		s = Track()
		s.replace(track)
		self.pl[str(track.track.databaseID())] = s
	
	def fetch(self, track):
		return self.pl[str(track.track.databaseID())]
	
	def write(self):
		plistlib.writePlist(self.pl, self.path)
		

class backupTests(unittest.TestCase):
	def setUp(self):
		pass


if __name__ == '__main__':
	unittest.main()