#!/usr/bin/env python
# encoding: utf-8
"""
AutoTag.py

Created by Max Johnson on 2009-08-15.
Copyright (c) 2009 __MyCompanyName__. All rights reserved.
"""

import sys
import os
import unittest
import re

from iTunesMac import *
from TrackTrie import TrackTrie
import iTMS
from backup import BackupDB

backup = BackupDB("./backup.plist")

def run():
	tracks = getSelected()
	for track in tracks:
		candidates = TrackTrie()
		for permutation in PermutationGenerator(track.lookupInfo):
			for candidate in iTMS.search(permutation):
				if abs(candidate["duration"] - track["duration"]) <= 3:
					candidates.add(candidate)
			if len(candidates) != 0: break
		if len(candidates) == 0: continue
		best = candidates.pick(track)
		backup.store(track)
		track.replace(best)
		track.save()
	backup.write()

def undo():
	tracks = getSelected()
	for track in tracks:
		try:
			orig = backup.fetch(track)
		except: continue
		track.replace(orig)
		track.save()

def refine():
	tracks = getSelected()
	track = tracks[0]
	candidates = TrackTrie()
	for permutation in PermutationGenerator(track.lookupInfo):
		for candidate in iTMS.search(permutation):
			candidates.add(candidate)
	return candidates

def PermutationGenerator(searchInfo):
	"""
	takes a searchInfo (3-tuple of track, artist, duration) and generates permutations
	should be iterated over, i.e. for permutation in PermutationGenerator(searchInfo):
	"""
	#first, yield the parameter. With any luck, it will be found and we don't have to do any more generation
	generated = [(searchInfo[0].strip(), searchInfo[1].strip())]
	yield generated[0]
	
	#try spell checking things
	"""permutation = Google.spellCheck(searchInfo)
	if permutation != None:
		yield return permutation
		generated.append(permutation)"""
	
	#split by hyphens in name
	#the counting is to ensure we only permutate the trackinfos generated earlier
	counter = 0
	maxCount = len(generated)
	for info in generated:
		if counter == maxCount: break
		splitted = info[0].split('-')
		for name in splitted:
			for artist in splitted:
				if name == artist: continue;
				permutation = (name.strip(), artist.strip())
				if permutation[0] != "" and permutation[1] != "":
					yield permutation
					generated.append(permutation)
		counter += 1
	
	#remove "featuring" and variants first from name, throw them into artists
	reg = re.compile("\\s*[\\(\\[]?(feat|ft|featuring)(\\.|:|\\s)", re.I);
	counter = 0
	maxCount = len(generated)
	for info in generated:
		if counter == maxCount: break
		m = reg.search(info[0])
		if m != None:
			permutation = (info[0][:m.start()], (info[1]+info[0][m.start():]).strip())
			if permutation[0] != "" and permutation[1] != "":
				yield permutation
				generated.append(permutation)
		counter += 1
	
	#check for multiple artists
	reg = re.compile("(?:\\s*[\\]\\(]?(?:and|w[\\\\/]|with|feat|ft|featuring)(?:\\.|:|\\s))|[&,]", re.I)
	counter = 0
	maxCount = len(generated)
	for info in generated:
		if counter == maxCount: break
		splits = reg.split(info[1])
		if len(splits) < 2: continue;
		for artist in splits:
			permutation = (info[0], artist.strip())
			if permutation[0] != "" and permutation[1] != "":
				yield permutation
				generated.append(permutation)
		counter += 1
	
	#check for () or [] in name, remove. for now just cuts after '(', it seems to work fine
	counter = 0
	maxCount = len(generated)
	for info in generated:
		if counter == maxCount: break
		try:
			permutation = (info[0][:info[0].index('(')].strip(), info[1])
			if permutation[0] != "" and permutation[1] != "":
				yield permutation
				generated.append(permutation)
		except ValueError: pass
		try:
			permutation = (info[0][:info[0].index('[')].strip(), info[1])
			if permutation[0] != "" and permutation[1] != "":
				yield permutation
				generated.append(permutation)
		except ValueError: pass
		counter += 1


class AutoTagTests(unittest.TestCase):
	#plug some bogus track info and assert that the permutation generator fixes it
	def setUp(self):
		pass


if __name__ == '__main__':
	#unittest.main()
	undo()
