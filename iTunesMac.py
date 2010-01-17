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
import threading

from Foundation import *
from ScriptingBridge import *
from track import Track as TrackInterface

_ituneslock = threading.Lock()

def getall():
	"""Gets all tracks from the iTunes library"""
	iTunesInstance = SBApplication.applicationWithBundleIdentifier_("com.apple.iTunes")
	return [Track(t) for t in iTunesInstance.sources()[0].playlists()[0].tracks()]

def getselected():
	"""Gets the selected tracks from the iTunes library"""
	iTunesInstance = SBApplication.applicationWithBundleIdentifier_("com.apple.iTunes")
	return [Track(t) for t in iTunesInstance.selection().get()]

def getplaylist(playlistName):
	"""Gets the tracks from a playlist in the iTunes library"""
	iTunesInstance = SBApplication.applicationWithBundleIdentifier_("com.apple.iTunes")
	for playlist in iTunesInstance.sources()[0].playlists():
		if playlist.name() == playlistName:
			return [Track(t) for t in playlist.tracks()]
	return None

class Track(TrackInterface):
	"""iTunes-Mac specific track"""
	
	def __init__(self, track):
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
	
	def save(self):
		"""Writes the changes to the iTunes library"""
		_ituneslock.acquire()
		try:
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
		finally:
			_ituneslock.release()
	
	@property
	def uid(self):
		"""Returns the iTunes database id of the track, which is both unique and persistent"""
		return self.track.databaseID()
