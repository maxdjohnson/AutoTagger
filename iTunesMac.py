#!/usr/bin/env python
# encoding: utf-8
"""
iTunesMac.py

Created by Max Johnson on 2009-08-15.
Copyright (c) 2009 __MyCompanyName__. All rights reserved.
"""

import sys
import os
import unittest

from Foundation import *
from ScriptingBridge import *

def getAll():
	iTunesInstance = SBApplication.applicationWithBundleIdentifier_("com.apple.iTunes")
	return TrackList(iTunesInstance.sources()[0].playlists()[0].tracks())

def getSelected():
	iTunesInstance = SBApplication.applicationWithBundleIdentifier_("com.apple.iTunes")
	return TrackList(iTunesInstance.selection().get())

def getPlaylist(playlistName):
	iTunesInstance = SBApplication.applicationWithBundleIdentifier_("com.apple.iTunes")
	for playlist in iTunesInstance.sources()[0].playlists():
		if playlist.name() == playlistName:
			return TrackList(playlist.tracks())
	return None

class TrackList(list):
	def __init__(self, tracks):
		super(TrackList, self).__init__()
		for track in tracks:
			super(TrackList, self).append(Track(track))

class Track(dict):
	def __init__(self, track = None):
		if (track == None):
			self.track = None
			self["name"] = ""
			self["artist"] = ""
			self["album"] = ""
			self["composer"] = ""
			self["genre"] = ""
			self["discCount"] = 0
			self["discNum"] = 0
			self["trackNum"] = 0
			self["trackCount"] = 0
			self["year"] = 0
			self["duration"] = 0
		else:
			self.track = track
			self["name"] = track.name().strip()
			self["artist"] = track.artist().strip()
			self["album"] = track.album().strip()
			self["composer"] = track.composer().strip()
			self["genre"] = track.genre().strip()
			self["discCount"] = track.discCount()
			self["discNum"] = track.discNumber()
			self["trackNum"] = track.trackNumber()
			self["trackCount"] = track.trackCount()
			self["year"] = track.year()
			self["duration"] = track.duration()
	
	def merge(self, track):
		#don't really know what we should do here...
		pass
	
	def replace(self, track):
		for k in track:
			self[k] = track[k]
	
	def backup(self):
		self.track.setComment_(str(self))
	
	def restore(self):
		self.replace(eval(self.track.comment()))
		self.track.setComment_("")
		self.save()
	
	def save(self):
		if self.track != None:
			self.track.setName_(self["name"])
			self.track.setArtist_(self["artist"])
			self.track.setAlbum_(self["album"])
			self.track.setComposer_(self["composer"])
			self.track.setGenre_(self["genre"])
			self.track.setDiscCount_(self["discCount"])
			self.track.setDiscNumber_(self["discNum"])
			self.track.setTrackNumber_(self["trackNum"])
			self.track.setTrackCount_(self["trackCount"])
			self.track.setYear_(self["year"])
	
	def getLookup(self):
		return (self["name"], self["artist"])
	
	lookupInfo = property(getLookup)
	
