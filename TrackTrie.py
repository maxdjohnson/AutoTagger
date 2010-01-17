#!/usr/bin/env python
# encoding: utf-8
"""
TrackTrie.py

Created by Max Johnson on 2009-08-16.
Copyright (c) 2009 __MyCompanyName__. All rights reserved.
"""

import sys, unittest
from editdist import distance
		
class TrackTrie(dict):
	"""Creates a Trie (Dictionary of dictionaries) of tracks for the purpose 
	of organizing them so a 'best' can be picked
	"""
	
	def __init__(self):
		super(TrackTrie, self).__init__()
		self.count = 0
		
	def add(self, track):
		"""Add a track to the Trie, keyed by artist, name, then year"""
		self.addRecurse(track, [track["artist"], track["name"], track["year"]])
	
	def addRecurse(self, track, info):
		if len(info) == 1:
			if info[0] not in self:
				self[info[0]] = track
				add = 1
			else:
				self[info[0]].merge(track)
				add = 0
		else:
			if info[0] not in self:
				self[info[0]] = TrackTrie()
			add = self[info[0]].addRecurse(track, info[1:])
		self.count += add
		return add
	
	def pick(self, track):
		"""Pick the best track from the trie by walking down the trie based on 
		levenshtein. Ties are broken by taking the earliest year
		"""
		return self.pickRecurse(track, [track["artist"], track["name"]])
	
	def pickRecurse(self, track, info):
		if len(info) == 0: #if this is the last level in the trie, find the earliest year
			closest = min(self)
			return self[closest]
		else: #if not, find the key with the closest distance
			closest = min([(distance(x, info[0]), x) for x in self])[1]
			return self[closest].pickRecurse(track, info[1:])
	
	def __str__(self):
		ret = ""
		for k in self:
			ret += str(k) + ":\n"
			for c in str(self[k]).split("\n"):
				ret += "-" + c + "\n"
		return ret
	
	def __len__(self):
		return self.count
	
class TrackTrieTests(unittest.TestCase):
	def setUp(self):
		pass
	
	def testKeys(self):
		from track import Track
		track = Track()
		track["name"] = "trackName"
		track["artist"] = "trackArtist"
		track["year"] = 2000
		trie = TrackTrie()
		trie.add(track)
		self.assertEqual(trie["trackArtist"]["trackName"][2000], track)
		self.assertEqual(len(trie), 1)
		trie.add(track)
		self.assertEqual(len(trie), 1)


#if __name__ == '__main__':
#	unittest.main()